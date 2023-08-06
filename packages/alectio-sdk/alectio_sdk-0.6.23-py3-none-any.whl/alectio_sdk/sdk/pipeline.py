import numpy as np
import json
import os
import time
import boto3
from scipy.special import softmax
from copy import deepcopy
from .s3_client import S3Client
from .api_client import APIClient
from alectio_sdk.metrics.object_detection import Metrics, batch_to_numpy
from alectio_sdk.metrics.classification import ClassificationMetrics
from alectio_sdk.metrics.object_segmentation import segmentation_metrics
from alectio_sdk.metrics.multilabel_classification import (
    MultiLabelClassificationMetrics,
)
from alectio_sdk.metrics.object_segmentation import SegMetrics
from rich.progress import track
from alectio_sdk.sdk.sql_client import create_connection
import logging
from .console import MainConsole


class Pipeline(object):
    r"""
    A wrapper for your `train`, `test`, and `infer` function. The arguments for your functions should be specifed
    separately and passed to your pipeline object during creation.

    Args:
        name (str): experiment name
        train_fn (function): function to be executed in the train cycle of the experiment.
        test_fn (function): function to be executed in the test cycle of the experiment.
        infer_fn (function): function to be executed in the inference cycle of the experiment.
        getstate_fn (function): function specifying a mapping between indices and file names.


    """

    def __init__(self, name, train_fn, test_fn, infer_fn, getstate_fn, args, token):
        """
        sentry_sdk.init(
            dsn="https://4eedcc29fa7844828397dca4afc2db32@o409542.ingest.sentry.io/5282336",
            integrations=[FlaskIntegration()]
        )
        """

        self.console = MainConsole()
        self.train_fn = train_fn
        self.test_fn = test_fn
        self.infer_fn = infer_fn
        self.getstate_fn = getstate_fn
        self.args = args
        self.client = S3Client()
        self.api_client = APIClient()
        dir_path = os.path.dirname(os.path.realpath(__file__))
        with open(os.path.join(dir_path, "config.json"), "r") as f:
            self.config = json.load(f)

        self.client_token = token
        self.labeled = []
        self._testUploaded = False
        self._uploaded_infer_index = []

    def notify_sdk_status(self, logdir):
        logging.basicConfig(
            filename=os.path.join(logdir, "Appstatus.log"), level=logging.INFO
        )
        self.console.success("SDK Alectio initialized successfully")
        self.console.message(
            "Training checkpoints and other logs for current experiment will be written into the folder {}".format(
                logdir
            )
        )
        self.console.message("Press CTRL + C to exit")

    def _checkdirs(self, dir_):
        if not os.path.exists(dir_):
            os.makedirs(dir_, exist_ok=True)

    def check_model_activations(self, model_outputs):
        supported_activations = {"pre_softmax", "softmax", "sigmoid", "logits"}
        activation_set = set()
        for k, v in model_outputs.items():
            if isinstance(v, dict):
                activation_set.update(set(v.keys()).intersection(supported_activations))
            if len(activation_set) == 0:
                raise TypeError("Incorrect logit output format encountered")

        return activation_set

    def _estimate_exp_time(self, last_time):
        """
        Estimates the compute time remaining for the experiment

        Args:
            train_times (list): training_times noted down so far
            n_loop (int): total number of loops
        """

        def convert(seconds):
            seconds = seconds % (24 * 3600)
            hour = seconds // 3600
            seconds %= 3600
            minutes = seconds // 60
            seconds %= 60

            return "%d:%02d:%02d" % (hour, minutes, seconds)

        loops_completed = self.cur_loop + 1
        time_left = convert(last_time * (self.n_loop - loops_completed))
        self.console.message(
            "Estimated time left for the experiment: {}".format(time_left)
        )
        return time_left

    def one_loop(self, request):

        # Get payload args

        self.console.message("Extracting payload arguments from Alectio")

        payload = {
            "experiment_id": request["experiment_id"],
            "project_id": request["project_id"],
            "cur_loop": request["cur_loop"],
            "user_id": request["user_id"],
            "bucket_name": request["bucket_name"],
            "type": request["type"],
            "n_rec": request["n_rec"],
            "n_loop": request["n_loop"],
        }

        self.logdir = payload["experiment_id"]
        self._checkdirs(self.logdir)

        self.notify_sdk_status(self.logdir)

        self.console.success("Valid payload arguments extracted")
        self.console.message("Initializing process to train and optimize your model")
        returned_payload = self.run_loop(payload, self.args)
        self.console.success("Optimization process complete !")
        self.console.info(
            "Results of the loop will be available in Alectio Platform soon"
        )
        headers = {"Authorization": "Bearer " + self.client_token}
        _, respnse = self.api_client.POST_REQUEST(
            end_point="/end_of_task", payload=returned_payload, headers=headers
        )
        if respnse.status_code == 200:
            self.console.message(
                "Experiment {} running".format(payload["experiment_id"])
            )
            return {"Message": "Loop Started - 200 status returned"}
        else:
            return {"Message": "Loop Failed - non 200 status returned"}

    def run_loop(self, payload, args):
        r"""
        Executes one loop of active learning. Returns the read `payload` back to the user.

        Args:
           args: a dict with the key `sample_payload` (required path) and any arguments needed by the `train`, `test`
           and infer functions.
        Example::

            args = {sample_payload: 'sample_payload.json', EXPT_DIR : "./log", exp_name: "test", \
                                                                 train_epochs: 1, batch_size: 8}


        """
        self.experiment_id = payload["experiment_id"]
        self.project_id = payload["project_id"]

        self.console.info("Extracting essential experiment params")

        # read selected indices upto this loop
        payload["cur_loop"] = int(payload["cur_loop"])
        self.cur_loop = payload["cur_loop"]
        self.bucket_name = payload["bucket_name"]
        self.n_loop = payload["n_loop"]

        # type of the ML problem

        self.type = payload["type"]
        self.type = self.type.lower()
        print("Task type: {}".format(self.type))
        # dir for expt log in S3
        # expt_dir = [payload["user_id"], payload["project_id"], payload["experiment_id"]]

        if self.bucket_name == self.config["sandbox_bucket"]:
            # shared S3 bucket for sandbox user
            self.expt_dir = os.path.join(
                payload["user_id"], payload["project_id"], payload["experiment_id"]
            )

            self.project_dir = os.path.join(payload["user_id"], payload["project_id"])

        else:
            # dedicated S3 bucket for paid user
            self.expt_dir = os.path.join(
                payload["project_id"], payload["experiment_id"]
            )

            self.project_dir = os.path.join(payload["project_id"])

        self.console.success("Essential experiment params have been extracted")

        self.console.info("Verifying the meta.json that was uploaded by the user")
        key = os.path.join(self.project_dir, "meta.json")
        bucket = boto3.resource("s3").Bucket(self.bucket_name)

        json_load_s3 = lambda f: json.load(bucket.Object(key=f).get()["Body"])
        self.meta_data = json_load_s3(key)
        self.console.info(
            "SDK Retrieved file: {} from bucket : {}".format(key, self.bucket_name)
        )

        self.labeled = []
        self.console.info("Reading indices to train on")

        for i in range(self.cur_loop + 1):
            object_key = os.path.join(
                self.expt_dir, "selected_indices_{}.pkl".format(i)
            )
            selected_indices = self.client.read(
                bucket=self.bucket_name, key=object_key, format="pickle"
            )
            self.labeled.extend(selected_indices)

        if self.cur_loop == 0:

            self.resume_from = None
            self.console.info(
                "Extracting indices for our reference, this may take time ... Please be patient"
            )
            self.state_json = self.getstate_fn(args)
            object_key = os.path.join(self.expt_dir, "data_map.pkl")
            self.console.success("Extraction complete !!!")
            self.console.message(
                "Creating index to records data reference for the current experiment"
            )
            self.client.upload_object(
                obj=self.state_json,
                bucket=self.bucket_name,
                key=object_key,
                format="pickle",
            )
            self.console.success("Reference creation complete")

        else:

            self.console.info("Resuming from a checkpoint from a previous loop ")
            # two dag approach needs to refer to the previous checkpoint
            self.resume_from = "ckpt_{}".format(self.cur_loop - 1)

        self.ckpt_file = "ckpt_{}".format(self.cur_loop)
        self.console.message("Initializing training of your model")

        self.train(args)
        self.console.success("Training finished !")
        self.console.message("Initializing testing of your model !")
        self.test(args)
        self.console.success("Testing finished !")
        self.console.message("Assessing current best model")
        self.infer(args)
        self.console.success("Assessment complete ")
        self.console.info(
            "Time to check what records to train on next loop , visit our front end for more details"
        )

        # Drop unwanted payload values
        del payload["type"]
        del payload["cur_loop"]
        del payload["bucket_name"]
        return payload

    def train(self, args):
        r"""
        A wrapper for your `train` function. Returns `None`.

        Args:
        args: a dict whose keys include all of the arguments needed for your `train` function which is defined in `processes.py`.

        """
        meta_data_list = []

        def save_meta_func(start, end, epoch, data_size, loss):

            meta_info = {
                "train_start": start,
                "train_end": end,
                "epoch": epoch,
                "data_size": data_size,
                "loss": loss,
                # "hyperparameters": hyperparameters
            }
            meta_data_list.append(meta_info)

        start = time.time()

        if self.labeled is not None and len(self.labeled) == 0:
            raise ValueError("Labeled indices from backend are empty or None")

        self.console.info("Labeled records are ready to be trained")
        self.labeled.sort()  # Maintain increasing order

        # if len(self.labeled) > len(set(self.labeled)):
        #     raise ValueError("There exist repeated records.")
        from collections import Counter

        all_labeled = dict(Counter(self.labeled))
        duplicates = []
        for k, v in all_labeled.items():
            if v == 2:
                duplicates.append(k)

        self.labeled = list(set(self.labeled))

        train_op = self.train_fn(
            args,
            labeled=deepcopy(self.labeled),
            resume_from=self.resume_from,
            ckpt_file=self.ckpt_file,
            save_meta_func=save_meta_func,
        )

        if train_op is not None:
            labels = train_op["labels"]
            unique, counts = np.unique(labels, return_counts=True)
            num_queried_per_class = {u: c for u, c in zip(unique, counts)}

        end = time.time()

        # @TODO compute insights from labels
        if train_op is not None:
            insights = {
                "train_time": end - start,
                "num_queried_per_class": num_queried_per_class,
            }
        else:
            insights = {"train_time": end - start}

        self._estimate_exp_time(insights["train_time"])
        object_key = os.path.join(
            self.expt_dir, "insights_{}.pkl".format(self.cur_loop)
        )

        self.client.upload_object(insights, self.bucket_name, object_key, "pickle")
        object_key = os.path.join(
            self.expt_dir, "meta_temp_{}.json".format(self.cur_loop)
        )
        self.client.upload_object(meta_data_list, self.bucket_name, object_key, "json")

        return

    def test(self, args):
        r"""
        A wrapper for your `test` function which writes predictions and ground truth to the specified S3 bucket. Returns `None`.

        Args:
        args: a dict whose keys include all of the arguments needed for your `test` function which is defined in `processes.py`.

        """
        self.console.info("Extracting test results ")

        # TODO: UPLOAD TEST DATA (IT IS OPTIONAL)
        """
            1. TAKE IMAGE/TEXT AS INPUT AND RETURN FROM TEST FUNCTION
            2. UPLOAD THE LABEL DATA
                I. IF TEXT DATA PUT IT INTO .PKL/ES
                II. IF IMAGE DATA, PUT IT TO S3 
            3. TEST DATA MAPPING
            4. SET IS_TESTUPLOAD TO TRUE(FOR EACH INITIAL CALL OF PIPELINE, IS_UPLOADTEST IS FALSE)
        
        """

        # res = self.test_fn(args, ckpt_file=self.ckpt_file,upload=not self._testUploaded)
        res = self.test_fn(args, ckpt_file=self.ckpt_file)

        if self.type == "3d_segmentation":
            if "rangebased" in res:
                (
                    _3D_predictions,
                    _3D_labels,
                    _2D_predictions,
                    _2D_labels,
                    range_filtered,
                    range_default,
                    input_data,
                ) = (
                    res["3Dpredictions"],
                    res["3Dlabels"],
                    res["2Dpredictions"],
                    res["2Dlabels"],
                    res["rangebased"],
                    res["default"],
                    res["input_data"] if "input_data" in res else [],
                )
            else:
                (
                    _3D_predictions,
                    _3D_labels,
                    _2D_predictions,
                    _2D_labels,
                    range_filtered,
                    range_default,
                    input_data,
                ) = (
                    res["3Dpredictions"],
                    res["3Dlabels"],
                    res["2Dpredictions"],
                    res["2Dlabels"],
                    None,
                    None,
                    res["input_data"] if "input_data" in res else [],
                )
        else:
            predictions, ground_truth, input_data = (
                res["predictions"],
                res["labels"],
                res["input_data"] if "input_data" in res else [],
            )
        self.console.message("Writing test results to S3")

        # UPLOAD LABEL DATA TO S3
        """
        IF TEXT DATA:
            MAKE A DICTIONARY TO SAVE INDEX AND TEXT IN A .PKL FILE
        IF IMAGE DATA:
            MAKE A DICTIONARY TO SAVE INDEX AND IMAGE S3 KEY IN A .PKL FILE
        """
        # upload datamap to es
        def es_upload_datmap(datamap):
            # es storing
            error, response = self.api_client.POST_REQUEST(
                end_point="/api/v0/store_test_datamap",
                payload={"exp_token": self.client_token, "data_map": data_map},
            )
            print(f"Test Data Upload: {response.json()['status']}")

        if self._testUploaded == False:
            msg = (
                "ℹ️  "
                + "Test data will be uploaded whenever you will start one experiment. \nYou can stop it from your code(Recommended to pass test data for better understanding)"
                + "\n"
            )

            self.console.message(msg)
            if "image" in self.type:
                data_map = []
                for i, image_array in enumerate(
                    track(input_data, description="Uploading test data...")
                ):
                    image_key = os.path.join(self.expt_dir, "test", str(i) + ".png")
                    data_map.append(
                        {
                            "index": i,
                            "s3_image_path": image_key,
                            "project_id": self.project_id,
                            "experiment_id": self.experiment_id,
                            "datamap_type": "test_datamap",
                        }
                    )
                    self.client.upload_object(image_array, self.bucket_name, image_key)

                # backup
                object_key = os.path.join(
                    self.expt_dir, "test_datamap.pkl".format(self.cur_loop)
                )
                self.client.upload_object(
                    data_map, self.bucket_name, object_key, "pickle"
                )
                self._testUploaded = True
                # ES storing
                # Feature will be released in v2 with lake
                #es_upload_datmap(datamap=data_map)

            if "text" in self.type:
                data_map = []
                for i, label in enumerate(input_data):
                    data_map.append(
                        {
                            "index": i,
                            "text": label,
                            "project_id": self.project_id,
                            "experiment_id": self.experiment_id,
                            "datamap_type": "test_datamap",
                        }
                    )

                # backup data
                object_key = os.path.join(
                    self.expt_dir, "test_datamap.pkl".format(self.cur_loop)
                )
                self.client.upload_object(
                    predictions, self.bucket_name, object_key, "pickle"
                )
                # ES storing
                # Feature will be released in V2 with lake
                #es_upload_datmap(datamap=data_map)
                self._testUploaded = True

        # write predictions and labels to S3
        object_key = os.path.join(
            self.expt_dir, "test_predictions_{}.pkl".format(self.cur_loop)
        )
        self.client.upload_object(predictions, self.bucket_name, object_key, "pickle")

        if self.cur_loop == 0:
            # write ground truth to S3
            object_key = os.path.join(
                self.expt_dir, "test_ground_truth.pkl".format(self.cur_loop)
            )
            self.client.upload_object(
                ground_truth, self.bucket_name, object_key, "pickle"
            )

        if "3D" in self.type:
            self.compute3D_metrics(
                _3D_predictions, _3D_labels, _2D_predictions, _2D_labels, range_filtered
            )
        else:
            self.compute_metrics(predictions, ground_truth)
        return

    def compute3D_metrics(
        self,
        pclpredictions,
        pcllabels,
        imgpredictions,
        imglabels,
        range_filtered,
        range_default,
    ):
        metrics = {}
        if self.type == "3d_object_detection":
            raise NotImplementedError(
                "3D object detection evaluation has not been implemented yet"
            )

        elif self.type == "3d_segmentation":
            m = SegMetrics(
                n_classes=len(self.meta_data["class_labels"]),
                labels=self.meta_data["class_labels"],
                return_2D=True,
                return_3D=True,
                rangenet=True,
                default_ranges=range_default,
                include_ranges=True,
                range_labels=range_filtered,
            )

            m.evaluate3D(pcllabels, pclpredictions, rangelabels=range_filtered)
            m.evaluate2D(imglabels, imgpredictions)
            metrics = {
                "3DCM": m.get3DCM(),
                "3DrangeCM": m.get3DrangeCM(),
                "3DmIOU": m.get3DmIOU(),
                "3DrangemIOU": m.get3DrangemIOU(),
                "3DIOU": m.get3DIOU(),
                "3Drange3DIOU": m.get3DrangeIOU(),
                "3DDICE": m.get3DDICE(),
                "3DmDICE": m.get3DmDICE(),
                "3DrangeDICE": m.get3DrangeDICE(),
                "3DrangemDICE": m.get3DrangemDICE(),
                "3DAcc": m.get3Dacc(),
                "3DmAcc": m.get3Dmacc(),
                "3DrangeAcc": m.get3Drangeacc(),
                "3DrangemAcc": m.get3Drangemacc(),
                "class_labels": self.meta_data["class_labels"],
            }

    def compute_metrics(self, predictions, ground_truth):
        metrics = {}
        if self.type == "2d_object_detection":
            det_boxes, det_labels, det_scores, true_boxes, true_labels = batch_to_numpy(
                predictions, ground_truth
            )

            m = Metrics(
                det_boxes=det_boxes,
                det_labels=det_labels,
                det_scores=det_scores,
                true_boxes=true_boxes,
                true_labels=true_labels,
                num_classes=len(self.meta_data["class_labels"]),
            )

            metrics = {
                "mAP": m.getmAP(),
                "AP": m.getAP(),
                "precision": m.getprecision(),
                "recall": m.getrecall(),
                "confusion_matrix": m.getCM().tolist(),
                "class_labels": self.meta_data["class_labels"],
            }

        elif (
            self.type == "text_classification"
            or self.type == "image_classification"
            or self.type == "numeric_classification"
        ):

            m = ClassificationMetrics(predictions, ground_truth)

            metrics = {
                "accuracy": m.get_accuracy(),
                "f1_score_per_class": m.get_f1_score_per_class(),
                "f1_score": m.get_f1_score(),
                "precision_per_class": m.get_precision_per_class(),
                "precision": m.get_precision(),
                "recall_per_class": m.get_recall_per_class(),
                "recall": m.get_recall(),
                "confusion_matrix": m.get_confusion_matrix(),
                "acc_per_class": m.get_acc_per_class(),
                "label_disagreement": m.get_label_disagreement(),
            }

        elif self.type == "2d_segmentation":

            metrics = segmentation_metrics(
                ground_truth, predictions, n_classes=len(self.meta_data["class_labels"])
            )

        elif (
            self.type == "multilabel_text_classification"
            or self.type == "multi_label_text_classification"
        ):

            m = MultiLabelClassificationMetrics(predictions, ground_truth)

            metrics = {
                "accuracy": m.get_accuracy(),
                "micro_f1": m.get_f1_score_micro(),
                "macro_f1": m.get_f1_score_macro(),
                "micro_precision": m.get_precision_micro(),
                "macro_precision": m.get_precision_macro(),
                "micro_recall": m.get_recall_micro(),
                "macro_recall": m.get_recall_macro(),
                "multilabel_confusion_matrix": m.get_confusion_matrix(),
                "hamming_loss": m.get_hamming_loss(),
            }

        else:
            raise ValueError(
                "The selected task type is currently not supported, received type : {}".format(
                    self.type
                )
            )

        # save metrics to S3
        object_key = os.path.join(self.expt_dir, "metrics_{}.pkl".format(self.cur_loop))
        self.client.upload_object(metrics, self.bucket_name, object_key, "pickle")

        return

    def infer(self, args):
        r"""
        A wrapper for your `infer` function which writes outputs to the specified S3 bucket. Returns `None`.

        Args:
            args: a dict whose keys include all of the arguments needed for your `infer` function which is defined in `processes.py`.

        """
        self.console.message(
            "Getting insights on currently unused/unlabelled train data"
        )
        self.console.message("This may take some time. Please be patient ............")

        ts = range(self.meta_data["train_size"])
        self.unlabeled = sorted(list(set(ts) - set(self.labeled)))
        args["cur_loop"] = self.cur_loop
        outputs = self.infer_fn(
            args, unlabeled=deepcopy(self.unlabeled), ckpt_file=self.ckpt_file
        )
        local_db = os.path.join(
            self.args["EXPT_DIR"], "infer_outputs_{}.db".format(self.cur_loop)
        )

        if os.path.exists(local_db) or outputs is not None:
            self.console.info(
                "Sending assessments on unlabelled train set to Alectio team"
            )
            if "classification" in self.type:
                outputs = outputs["outputs"]
                # finds correct activation as key i.e. 'sigmoid' or 'logits'
                activation = self.check_model_activations(outputs)

                # Remap to absolute indices
                logits_dict = {}
                remap_dict = {}
                confidence_vals = []
                for key in outputs.keys():
                    remap_dict[key] = self.unlabeled.pop(0)

                while len(outputs) > 0:
                    for orig_ix, correct_ix in track(
                        remap_dict.items(), description="uploading infer data..."
                    ):
                        val = outputs.pop(orig_ix)
                        logits_dict[correct_ix] = {}
                        for a in activation:
                            logits_dict[correct_ix][a] = val[a]
                            if (
                                "input_data" in val
                                or correct_ix in self._uploaded_infer_index
                            ):
                                image_key = os.path.join(
                                    self.expt_dir, "infer", str(correct_ix) + ".png"
                                )
                                if correct_ix not in self._uploaded_infer_index:
                                    self.client.upload_object(
                                        val["input_data"], self.bucket_name, image_key
                                    )
                                    self._uploaded_infer_index.append(correct_ix)
                            else:
                                image_key = None
                            confidence_vals.append(
                                {
                                    "index": correct_ix,
                                    "prediction": val["prediction"],
                                    "confidence": round(
                                        softmax(val[a])[val["prediction"]], 2
                                    ),
                                    "current_loop": self.cur_loop + 1,
                                    "datamap_type": "infer_datamap",
                                    "s3_image_path": image_key,
                                    "project_id": self.project_id,
                                    "experiment_id": self.experiment_id,
                                }
                            )

                # upload confidence to ES
                error, response = self.api_client.POST_REQUEST(
                    end_point="/api/v0/store_infer_confidence",
                    payload={
                        "exp_token": self.client_token,
                        "confidence_vals": confidence_vals,
                    },
                )
                if error:
                    print(f"TEST DATA STORING NOT SUCCESSFUL")
                else:
                    print(f"TEST DATA STORING SUCCESSFUL")

                object_key = os.path.join(
                    self.expt_dir, "logits_{}.pkl".format(self.cur_loop)
                )
                self.client.upload_object(
                    logits_dict, self.bucket_name, object_key, "pickle"
                )
            elif "object_detection" or "semantic" in self.type:
                object_key = os.path.join(
                    self.expt_dir, "infer_outputs_{}.db".format(self.cur_loop)
                )
                logits_conn = create_connection(local_db)

                if logits_conn is not None:
                    logits_cur = logits_conn.cursor()
                    sql = """
                            UPDATE indexes
                            SET row_id = ?
                            WHERE id = ?
                    """
                    for index, correct_ix in enumerate(self.unlabeled):
                        logits_cur.execute(sql, (correct_ix, index))

                    logits_conn.close()
                else:
                    raise ConnectionError("Cannot connect to softmax database")

                # upload sqlite db
                self.client.upload_file(
                    local_db, self.bucket_name, object_key
                )
                # delete local version
                os.remove(local_db)
            else:
                raise ValueError("Use case not found")
        else:
            raise ValueError(
                "Infer outputs not returned. You must return outputs from the implemented infer() "
                "function. Please refer to the README on the Alectio SDK repository."
            )

        return

    def __call__(self):
        _, response = self.api_client.POST_REQUEST(
            end_point="/api/v0/start_experiment_response",
            payload={"exp_token": self.client_token},
        )
        print(response.json()["message"])
        if response.json()["message"] == "Started":
            count = 0
            while True:
                _, response = self.api_client.POST_REQUEST(
                    end_point="/api/v0/get_sdk_response",
                    payload={"exp_token": self.client_token},
                )
                if response.json()["status"] == "Fetched":
                    print("\n")
                    one_loop_response = self.one_loop(response.json())
                    print("\n")
                    print(one_loop_response)
                    count = 0

                if response.json()["status"] == "Finished":
                    print("\n")
                    print("Experiment complete")
                    os.environ["AWS_ACCESS_KEY_ID"] = " "
                    os.environ["AWS_SECRET_ACCESS_KEY"] = " "
                    break
                if response.json()["status"] == "Paused":
                    print("\n")
                    print(response.json()["message"])
                    os.environ["AWS_ACCESS_KEY_ID"] = " "
                    os.environ["AWS_SECRET_ACCESS_KEY"] = " "
                    break
                if response.json()["status"] == "Failed":
                    if count == 0:
                        print("\n")

                        self.console.warning("Waiting for server.")
                        count += 1
                        time.sleep(10)
                    else:
                        time.sleep(10)
                        print(".", end="", flush=True)
