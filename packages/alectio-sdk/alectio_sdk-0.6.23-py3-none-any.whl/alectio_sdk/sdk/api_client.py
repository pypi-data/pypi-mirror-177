import os
import json
from pickle import FALSE, NONE
import boto3
import requests

class APIClient:
    r"""
    A wrapper of python reqeusts module
    It is to handle all GET,POST,PUT,DELETE requests

    Functions:
        * GET_REQUEST - for all get request
            - INPUT PARAMERTERS
                end_point: str

                payload:   dict(optional)

                auth:      dict(optional)
            - RETURN
                error:     bool
                
                response:  dict



        * POST_REQUEST - for all get request
            - INPUT PARAMERTERS
                end_point: str

                payload:   dict(optional)

                auth:      dict(optional)
            - RETURN
                error:     bool

                response:  dict



    """
    def __init__(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        with open(os.path.join(dir_path, "config.json"), "r") as f:
            self.config = json.load(f)
        self.backend_url = "http://"+self.config['backend_ip']
   
    
    def GET_REQUEST(self,end_point:str,payload:dict={},auth:dict={}):
        api_url = self.backend_url+end_point
        response = requests.get(api_url, json=payload,auth=auth)
        if response.status_code not in [200,201,202,203,204,2005,206]:
            return True,None
        else:
            return False,response


    def POST_REQUEST(self,end_point:str,payload:dict,auth:dict={},headers:dict={}):
        api_url = self.backend_url+end_point
        response = requests.post(url=api_url, json=payload,auth=auth,headers=headers)
        if response.status_code not in [200,201,202,203,204,2005,206]:
            return True,None
        else:
            return False,response