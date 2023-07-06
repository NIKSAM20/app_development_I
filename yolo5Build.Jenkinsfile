pipeline {
    agent any

    stages {
        stage('Authentication') {
            steps {
                sh 'echo authenticating...'
            }
        }
    }

    stages {
        stage('Build') {
            steps {
                sh 'echo building...'
            }
        }
    }

    stages {
        stage('Push to ECR') {
            steps {
                sh 'echo pushing...'
            }
        }
    }
}
