
    
    pipeline {
    agent any

    stages {
        stage('git pull') {
            steps {
                git url: 'https://github.com/tejadata/mlops.git', branch: 'main'
            }
        }
        stage('docker cred'){
            steps {
               bat 'docker login -u <user_name> -p <password>'
            }
        }
        stage('python') {
            steps{
                bat 'C:\\Users\\viswa\\anaconda3\\python.exe -u D:\\MLOPs\\mlops_code\\docker.py'
            }
        }
 
        
        }
    }
