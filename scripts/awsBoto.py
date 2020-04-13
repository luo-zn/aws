#!/bin/env/python
#Created By lzn

import os
import boto3
from functools import wraps

def try_catch(f):
    @wraps(f)
    def wrapFunc(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            print(getattr("__name__"), " Except: ", str(e))
            return None
    return wrapFunc

class Lambda:
    def __init__(self):
        self.client = boto3.client('lambda') 
    
    @try_catch
    def get_function(self, **kwargs):
        kw={"FunctionName":kwargs["FunctionName"]}
        if "Qualifier" in kwargs:
            kw["Qualifier"] = kwargs["Qualifier"]
        return self.client.get_function(**kw)

    def read_zip_code(self, path):
        fct = ""
        with open(path, 'rb') as f:
            fct = f.read()
        return fct

    def change_zipfile_2byte(self, kwargs):
        zipfile = kwargs.get("Code",{}).get("ZipFile")
        fct = self.read_zip_code(zipfile)
        kwargs["Code"]["ZipFile"] = fct
        return kwargs
        
    @try_catch
    def get_alias(self, **kwargs):
        return self.client.get_alias(**kwargs)

    def publish_version_with_alias(self, **kwargs):
        alias_name = kwargs.pop("Name")
        print("*"*10, "Publishing a version!", "*"*10) 
        publish_ver = self.client.publish_version(**kwargs)
        print("version=", publish_ver["Version"])
        kwargs["FunctionVersion"] = publish_ver["Version"]     
        kwargs["Name"] = alias_name
        if self.get_alias(FunctionName=kwargs.get("FunctionName"), Name=alias_name):
            res = self.client.update_alias(**kwargs)
        else:
            res = self.client.create_alias(**kwargs)
        print("Alias", res)

    def deploy(self, **kwargs):  
        print("*"*10, "Deploying Lambda!", "*"*10)      
        versionAlias = kwargs.pop("versionAlias",{})
        versionAlias["FunctionName"] = kwargs["FunctionName"]
        kwargs = self.change_zipfile_2byte(kwargs)
        if self.get_function(**kwargs):
            print("Updating  code!")
            resp = self.client.update_function_code(FunctionName=kwargs["FunctionName"], ZipFile=kwargs["Code"]["ZipFile"])
        else:
            print("Creating lamda ", kwargs.get("FunctionName"))            
            resp = self.client.create_function(**kwargs)
        print(resp)
        self.publish_version_with_alias(**versionAlias)
        print("*"*10, "Finished Lambda Deploying!", "*"*10)

class GitlabAws:
    def __init__(self):
        pass 

    def read_env(self):
        env = os.environ
        branch = env["CI_COMMIT_REF_NAME"]
        name = branch.capitalize()
        if branch == "master":
            name = "Prod"
        return {"FunctionName":env["CI_PROJECT_NAME"], "Runtime": "go1.x", "Role":env["AWS_ROLE"], 
        "Handler":env["GO_BIN"],"Code": {"ZipFile":env["CODE_ZIP"]},
        "versionAlias":{"Description":"%s branch code!" % branch, "Name":name}
        }

    def main(self):
        # lda = {"FunctionName":"myFunction", "Runtime": "go1.x", "Role":"arn:aws:iam::xxxxxxxxx:role/gitlab-ci", "Handler":"myFunction-main",
        # "Code": {"ZipFile":"/data/lzn-test-myFunction-main.zip"},
        # "versionAlias":{"Description":"Test", "Name":"Test"}
        # }
        Lambda().deploy(**self.read_env())

if __name__ == "__main__":
  GitlabAws().main()


# https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html