# mlops
Cloud agnostic solution for deploying Machine Learning models in docker and kubernetes 

## docker.py

In this python code we are getting the latest build number from jenkins that is used to build and tag our docker image and then pushing the image to docker hub and then deploying Docker Image in to Kubernetes cluster

## Jenkinsfile

In this jenkins pipeline file we are pulling the lastet code from git and deploying the model and inferencing logic to docker image and then pushing it to docker hub
