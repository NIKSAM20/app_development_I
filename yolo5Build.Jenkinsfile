pipeline {
    agent any

    stages {
        stage('ECR Authentication and Docker login') {
            steps {
                sh '''
                aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin 854171615125.dkr.ecr.us-west-2.amazonaws.com
                '''
            }
        }

        stage('Build') {
            steps {
                sh '''
                cd yolo5
                docker build -t nikhil-yolo5 .
                '''
            }
        }

        stage('Push to ECR') {
            steps {
                sh '''
                docker tag nikhil-yolo5:latest 854171615125.dkr.ecr.us-west-2.amazonaws.com/nikhil-yolo5:${BUILD_NUMBER}
                docker push 854171615125.dkr.ecr.us-west-2.amazonaws.com/nikhil-yolo5:${BUILD_NUMBER}
                '''

            }
        }       
    }
}