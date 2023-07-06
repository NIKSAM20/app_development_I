pipeline {
    agent any

    stages {
        stage('Authentication') {
            steps {
                sh 'echo authenticating...'
            }
        }

        stage('Build') {
            steps {
                sh 'echo building...'
            }
        }

        stage('Push to ECR') {
            steps {
                sh 'echo pushing...'
            }
        }       
    }
}