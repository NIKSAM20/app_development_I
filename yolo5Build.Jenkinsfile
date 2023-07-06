pipeline {
    agent any

    environment{
        ECR_URL = '854171615125.dkr.ecr.us-west-2.amazonaws.com'
        REPO_NAME = 'nikhil-yolo5'
    }

    stages {
        stage('ECR Authentication and Docker login') {
            steps {
                sh '''
                aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin ${ECR_URL}
                '''
            }
        }

        stage('Build') {
            steps {
                sh '''
                cd yolo5
                docker build -t ${REPO_NAME} .
                '''
            }
        }

        stage('Push to ECR') {
            steps {
                sh '''
                docker tag nikhil-yolo5:latest ${ECR_URL}/nikhil-yolo5:0.${BUILD_NUMBER}
                docker push ${ECR_URL}/${REPO_NAME}:0.${BUILD_NUMBER}
                '''

            }
        }

        stage('Trigger Deploy') {
            steps {
                build job: 'Yolo5Deploy', wait: false, parameters: [
                string(name: 'YOLO5_IMAGE_URL', value: "${ECR_URL}/${REPO_NAME}:0.${BUILD_NUMBER}")
                ]
            }
        }    
    }
}