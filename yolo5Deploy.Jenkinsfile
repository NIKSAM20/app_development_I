pipeline {

    agent any

    parameters { string(name: 'YOLO5_IMAGE_URL', defaultValue: '', description: '') }
    
    stages {
        stage('Deploy') {
            steps {
                sh '''
                echo authenticaing EKS cluster
                echo go to k8s/yolo5.yaml, and change the image to {YOLO5_IMAGE_URL}
                echo "apply -f k8s/yolo5.yaml"
                '''
            }
        }
    }
}