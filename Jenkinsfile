pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "rvp0110/flask-posts"
        KUBE_CONFIG = credentials('kubeconfig-file')   // Jenkins credentials ID for kubeconfig
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/Pradeep-Devops-0110/Python-project-02.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    def imageTag = "v${env.BUILD_NUMBER}"
                    sh "docker build --no-cache -t ${DOCKER_IMAGE}:${imageTag} ."
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: 'dockerhub-creds',
                                                      usernameVariable: 'DOCKER_USER',
                                                      passwordVariable: 'DOCKER_PASS')]) {
                        sh '''
                            echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin
                            docker push rvp0110/flask-posts:v$BUILD_NUMBER
                        '''
                    }
                }
            }
        }

        stage('Run Migrations') {
            steps {
                script {
                    def imageTag = "v${env.BUILD_NUMBER}"
                    sh """
                        docker run --rm \
                            -e SECRET_KEY=dev \
                            -e JWT_SECRET_KEY=dev \
                            -e DATABASE_URL=sqlite:///local.db \
                            ${DOCKER_IMAGE}:${imageTag} \
                            flask --app flask_app.app:create_app db upgrade
                    """
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                script {
                    def imageTag = "v${env.BUILD_NUMBER}"
                    sh """
                        kubectl --kubeconfig=${KUBE_CONFIG} set image deployment/flask-posts \
                            flask-posts=${DOCKER_IMAGE}:${imageTag}
                        kubectl --kubeconfig=${KUBE_CONFIG} rollout restart deployment flask-posts
                    """
                }
            }
        }
    }

    post {
        success {
            echo "✅ Deployment successful: ${DOCKER_IMAGE}:v${env.BUILD_NUMBER}"
        }
        failure {
            echo "❌ Build or deploy failed. Check logs."
        }
    }
}
