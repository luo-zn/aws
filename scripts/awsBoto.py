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
            print(f.__name__, " Except: ", str(e))
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

    @try_catch
    def update_function_configuration(self,**kwargs):
        print("*"*10, "Updating function configuration!", "*"*10)
        kwargs.pop("Code")
        print(self.client.update_function_configuration(**kwargs))

    def deploy(self, **kwargs):  
        print("*"*10, "Deploying Lambda!", "*"*10)      
        versionAlias = kwargs.pop("versionAlias",{})
        versionAlias["FunctionName"] = kwargs["FunctionName"]
        kwargs = self.change_zipfile_2byte(kwargs)
        if self.get_function(**kwargs):
            print("Updating  code!")
            print(self.client.update_function_code(FunctionName=kwargs["FunctionName"], ZipFile=kwargs["Code"]["ZipFile"]))
            self.update_function_configuration(**kwargs)
        else:
            print("Creating lamda ", kwargs.get("FunctionName"))            
            print(self.client.create_function(**kwargs))
        self.publish_version_with_alias(**versionAlias)
        print("*"*10, "Finished Lambda Deploying!", "*"*10)

class GitlabAws:
    def __init__(self):
        self.env = os.environ
    
    def get_lambda_env(self):
        # In gitlab web add env,  project -> settings -> CI/CD -> Variables
        # variables format 1: LAMBDA_[ENV NAME] = VALUE        
        # variables format 2: [REF NAME with capitalize]_LAMBDA_[ENV NAME] = VALUE        
        lambda_env, env_prefix, ref_name = {}, "LAMBDA_", self.env.get("CI_COMMIT_REF_NAME","")
        b_env_prefix = "%s_%s"%(ref_name.capitalize(),env_prefix)
        for key in self.env.keys():          
            if str(key).startswith(env_prefix):
                lambda_env[key.split(env_prefix)[-1]] = self.env[key]
            if str(key).startswith(b_env_prefix):
                lambda_env[key.split(b_env_prefix)[-1]] = self.env[key]
        return lambda_env

    def read_env(self):
        branch = self.env["CI_COMMIT_REF_NAME"]
        name = branch.capitalize()
        if branch == "master":
            name = "Prod"
        return {"FunctionName":self.env["CI_PROJECT_NAME"], "Runtime": "go1.x", "Role":self.env["AWS_ROLE"], 
        "Handler":self.env["GO_BIN"],"Code": {"ZipFile":self.env["CODE_ZIP"]},"Environment":{'Variables':  self.get_lambda_env()},
        "versionAlias":{"Description":"%s branch code!" % branch, "Name":name}
        }

    def main(self):
        # lda = {"FunctionName":"myFunction", "Runtime": "go1.x", "Role":"arn:aws:iam::xxxxxxx:role/gitlab-ci", "Handler":"myFunction-main",
        # "Code": {"ZipFile":"/data/lzn-test-myFunction-main.zip"}, "Environment":{'Variables':  self.get_lambda_env()},
        # "versionAlias":{"Description":"Test", "Name":"Test"}
        # }
        Lambda().deploy(**self.read_env())
        # Lambda().deploy(**lda)

if __name__ == "__main__":
  GitlabAws().main()


# https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html