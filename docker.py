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
from kubernetes import client, config, utils
from kubernetes.config import load_config

kube={"apiVersion":"apps/v1","kind":"Deployment","metadata":{"name":"signin"},"spec":{"replicas":2,"selector":{"matchLabels":{"app":"signin"}},"template":{"metadata":{"labels":{"app":"signin"}},"spec":{"containers":[{"name":"signin","image":"assetsmanagement/asset_login_signup_5020","resources":{"requests":{"memory":"2048Mi","cpu":"1024m"},"limits":{"memory":"4096Mi","cpu":"2048m"}},"ports":[{"containerPort":5020}]}]}}}}
services={"apiVersion":"v1","kind":"Service","metadata":{"name":"iris"},"spec":{"type":"NodePort","ports":[{"port":9999,"targetPort":9999}],"selector":{"app":"iris"}}}
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
    print("log File name::",log_file_name)
    with open(log_file_name, "a") as output:
        print(output)
        subprocess.call(build_cmd, shell=True, stdout=output, stderr=output)

    return img_name,log_file_name

def tag_push_image(img_name,log_file_name):
    tag_cmd="docker tag " +img_name+ " viswabhanu/"+img_name
    print("Docker command for re tagging::",tag_cmd)
    with open(log_file_name, "a") as output:
        subprocess.call(tag_cmd, shell=True, stdout=output, stderr=output)
    
    push_cmd = "docker push viswabhanu/"+img_name
    print("Docker command for pushing::",push_cmd)
    time.sleep(20)
    with open(log_file_name, "a") as output:
        subprocess.call(push_cmd, shell=True, stdout=output, stderr=output)
    
    print("Docker push completed")
    return "viswabhanu/"+img_name
    
def generate_kube_file(img_name):
    with open(r"D:\MLOPs\mlops_code\config.json","r") as con:
        res=json.loads(con.read())
    kube['metadata']['name']=str(res['app_name'])
    kube['spec']['replicas']=res['instance_cnt']
    kube['spec']['selector']['matchLabels']['app']=str(res['app_name'])
    kube['spec']['template']['metadata']['labels']['app']=str(res['app_name'])
    kube['spec']['template']['spec']['containers'][0]['name']=str(res['app_name'])
    kube['spec']['template']['spec']['containers'][0]['image']=img_name
    kube['spec']['template']['spec']['containers'][0]['resources']['requests']['memory']=str(res['ram'])
    kube['spec']['template']['spec']['containers'][0]['resources']['requests']['cpu']=str(res['cpu'])
    kube['spec']['template']['spec']['containers'][0]['resources']['limits']['memory']=str(res['ram_limit'])
    kube['spec']['template']['spec']['containers'][0]['resources']['limits']['cpu']=str(res['cpu_limit'])

    file_name_kube="C:\\ProgramData\\Jenkins\\.jenkins\\workspace\\mlops1\\"+res['app_name']+".yaml"
    file_name_svc="C:\\ProgramData\\Jenkins\\.jenkins\\workspace\\mlops1\\"+res['app_name']+"_service"+".yaml"
    with open(file_name_kube, 'w') as outfile:
        yaml.dump(kube, outfile, default_flow_style=False)
        
    with open(file_name_svc, 'w') as outfile:
            yaml.dump(services, outfile, default_flow_style=False)
    
    print("Kuberneties files written in:: ",file_name_kube)
    return file_name_kube,file_name_svc

def deploy_ml(kube_file,svc_file):
    config.load_kube_config(config_file='C:\\Users\\viswa\\.kube\\config')
    k8s_client = client.ApiClient()
    print("Deploying the Image")
    utils.create_from_yaml(k8s_client, kube_file)
    print("Creating a Service")
    utils.create_from_yaml(k8s_client, svc_file)
    print("Deployed Model in Kuberneties cluster")
    return "success"

def main_process():
    # Getting Jenkins latest build number
    build_num=get_latest_build_info()
    
    # Building docker Image
    img_name,log_file_name=build_image(build_num)
    
    # Tagging docker image and pushing to Docker hub
    tagged_image=tag_push_image(img_name,log_file_name)
    
    #Generating Kubernetes Yaml file from the config file
    kube_file=generate_kube_file(tagged_image)
    
    # Deploying the Docker image in kubernetes cluster
    deploy_ml(kube_file[0],kube_file[1])

    return "Success"
    
if __name__ == "__main__":
    main_process()
