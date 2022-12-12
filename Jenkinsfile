
   pipeline {
    agent any

    stages {
        stage('Hello') {
            steps {
                git url: 'https://github.com/tejadata/mlops.git', branch: 'main'
            }
        }
        stage('python') {
            steps{
                bat 'C:\\Users\\viswa\\anaconda3\\python.exe -u D:\\MLOPs\\mlops_code\\docker.py'
            }
        }
 
        
        }
    }
