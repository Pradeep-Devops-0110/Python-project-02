pipeline {
    agent any

    environment {
        IMAGE_NAME = "flask-posts"
        IMAGE_TAG = "dev"
        REGISTRY = "docker.io/rvp0110"   // change if using DockerHub or another registry
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/Pradeep-Devops-0110/Python-project-02.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $IMAGE_NAME:$IMAGE_TAG .'
            }
        }

        stage('Run Migrations') {
            steps {
                sh '''
                docker run --rm \
                  -e SECRET_KEY=dev \
                  -e JWT_SECRET_KEY=dev \
                  -e DATABASE_URL="sqlite:///local.db" \
                  $IMAGE_NAME:$IMAGE_TAG \
                  flask --app flask_app.app:create_app db upgrade
                '''
            }
        }

        stage('Push to Registry') {
            steps {
                sh 'docker tag $IMAGE_NAME:$IMAGE_TAG $REGISTRY/$IMAGE_NAME:$IMAGE_TAG'
                sh 'docker push $REGISTRY/$IMAGE_NAME:$IMAGE_TAG'
            }
        }

        stage('Deploy to Minikube') {
            steps {
                sh 'kubectl apply -f k8s/deployment.yaml'
                sh 'kubectl apply -f k8s/service.yaml'
            }
        }
    }
}
