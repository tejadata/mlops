# -*- coding: utf-8 -*-
"""
Created on Sun Dec 11 21:15:01 2022

@author: viswa
"""




import subprocess
import jenkins
import time

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
    
def main_process():
    build_num=get_latest_build_info()
    img_name,log_file_name=build_image(build_num)
    tag_push_image(img_name,log_file_name)
    with open(log_file_name, "r", errors="ignore") as output:
        print(output.read())
    
    return "Success"
    
if __name__ == "__main__":
    main_process()