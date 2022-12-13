# -*- coding: utf-8 -*-
"""
Created on Sun Dec 11 22:15:01 2022

@author: viswateja
"""

import subprocess
import jenkins
import time
import json
import yaml

kube={"apiVersion":"apps/v1","kind":"Deployment","metadata":{"name":"signin"},"spec":{"replicas":2,"selector":{"matchLabels":{"app":"signin"}},"template":{"metadata":{"labels":{"app":"signin"}},"spec":{"containers":[{"name":"signin","image":"assetsmanagement/asset_login_signup_5020","resources":{"requests":{"memory":"2048Mi","cpu":"1024m"},"limits":{"memory":"4096Mi","cpu":"2048m"}},"ports":[{"containerPort":5020}]}]}}}}

def get_latest_build_info():
    server = jenkins.Jenkins('http://localhost:8080/', username='viswateja',
                             password='Computers.3')
    build_num = server.get_job_info('mlops1')['nextBuildNumber']
    print("build info",build_num)
    return build_num-1

def build_image(build_num):
    img_name = "test:"+str(build_num)
    print("Image name", img_name)
    build_cmd = "docker build  -t " +img_name+ " -f C:\\ProgramData\\Jenkins\\.jenkins\\workspace\\mlops1\\Dockerfile ." 
    print("Running docker command ", build_cmd)
    log_file_name="D:\MLOPs\code\mlops\logs" + "/" + str(build_num)+".log"
    print("log File name",log_file_name)
    with open(log_file_name, "a") as output:
        print(output)
        subprocess.call(build_cmd, shell=True, stdout=output, stderr=output)
        

    return img_name,log_file_name

def tag_push_image(img_name,log_file_name):
    tag_cmd="docker tag " +img_name+ " viswabhanu/"+img_name
    print("Docker command for re tagging",tag_cmd)
    with open(log_file_name, "a") as output:
        subprocess.call(tag_cmd, shell=True, stdout=output, stderr=output)
    
    push_cmd = "docker push viswabhanu/"+img_name
    print("Docker command for pushing",push_cmd)
    time.sleep(20)
    with open(log_file_name, "a") as output:
        subprocess.call(push_cmd, shell=True, stdout=output, stderr=output)

def generate_kube_file():
    with open(r"D:\MLOPs\mlops_code\config.json","r") as con:
        res=json.loads(con.read())
    kube['metadata']['name']=res['app_name']
    kube['spec']['replicas']=res['instance_cnt']
    kube['spec']['selector']['matchLabels']['app']=res['app_name']
    kube['spec']['template']['metadata']['labels']['app']=res['app_name']
    kube['spec']['template']['spec']['containers'][0]['name']=res['app_name']
    kube['spec']['template']['spec']['containers'][0]['image']="viswabhanu/test:59"
    kube['spec']['template']['spec']['containers'][0]['resources']['requests']['memory']=res['ram']
    kube['spec']['template']['spec']['containers'][0]['resources']['requests']['cpu']=res['cpu']
    kube['spec']['template']['spec']['containers'][0]['resources']['limits']['memory']=res['ram_limit']
    kube['spec']['template']['spec']['containers'][0]['resources']['limits']['cpu']=res['cpu_limit']

    with open(res['app_name']+".yaml", 'w') as outfile:
        yaml.dump(kube, outfile, default_flow_style=False)
    
def main_process():
    build_num=get_latest_build_info()
    img_name,log_file_name=build_image(build_num)
    tag_push_image(img_name,log_file_name)
    generate_kube_file()
    with open(log_file_name, "r", errors="ignore") as output:
        print(output.read())
    
    return "Success"
    
if __name__ == "__main__":
    main_process()