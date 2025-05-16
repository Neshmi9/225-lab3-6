pipeline {
    agent any 

    environment {
        DOCKER_CREDENTIALS_ID = 'roseaw-dockerhub'
        DOCKER_IMAGE = 'cithit/alhayen-dev'  // <-- your DockerHub image
        IMAGE_TAG = "build-${BUILD_NUMBER}"
        GITHUB_URL = 'https://github.com/neshmi9/225-lab3-6.git'  // <-- your GitHub repo
    }

    stages {
        stage('Checkout') {
            steps {
                checkout([$class: 'GitSCM', branches: [[name: '*/main']],
                          userRemoteConfigs: [[url: "${GITHUB_URL}"]]])
            }
        }

        stage('Lint HTML') {
            steps {
                sh 'npm install htmlhint --save-dev'
                sh 'npx htmlhint *.html'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    docker.build("${DOCKER_IMAGE}:${IMAGE_TAG}", "-f Dockerfile.build .")
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    docker.withRegistry('https://index.docker.io/v1/', "${DOCKER_CREDENTIALS_ID}") {
                        docker.image("${DOCKER_IMAGE}:${IMAGE_TAG}").push()
                    }
                }
            }
        }

        stage('Deploy to Dev Environment') {
            steps {
                withCredentials([file(credentialsId: 'kubeconfig-alhayek', variable: 'KUBECONFIG')]) {
                    script {
                        sh "sed -i 's|${DOCKER_IMAGE}:latest|${DOCKER_IMAGE}:${IMAGE_TAG}|' deployment-dev.yaml"
                        sh "kubectl --kubeconfig=$KUBECONFIG apply -f deployment-dev.yaml"
                    }
                }
            }
        }

        stage("Run Acceptance Tests") {
            steps {
                script {
                    sh 'docker stop qa-tests || true'
                    sh 'docker rm qa-tests || true'
                    sh 'docker build -t qa-tests -f Dockerfile.test .'
                    sh 'docker run qa-tests'
                    sh 'docker stop qa-tests || true'
                    sh 'docker rm qa-tests || true'
                }
            }
        }

        stage('Deploy to Prod Environment') {
            steps {
                withCredentials([file(credentialsId: 'kubeconfig-alhayek', variable: 'KUBECONFIG')]) {
                    script {
                        sh "sed -i 's|${DOCKER_IMAGE}:latest|${DOCKER_IMAGE}:${IMAGE_TAG}|' deployment-prod.yaml"
                        sh "kubectl --kubeconfig=$KUBECONFIG apply -f deployment-prod.yaml"
                    }
                }
            }
        }

        stage('Check Kubernetes Cluster') {
            steps {
                withCredentials([file(credentialsId: 'kubeconfig-alhayek', variable: 'KUBECONFIG')]) {
                    script {
                        sh "kubectl --kubeconfig=$KUBECONFIG get all"
                    }
                }
            }
        }
    }

    post {
        success {
            slackSend color: "good", message: "✅ Build Completed: ${env.JOB_NAME} #${env.BUILD_NUMBER}"
        }
        unstable {
            slackSend color: "warning", message: "⚠️ Build Unstable: ${env.JOB_NAME} #${env.BUILD_NUMBER}"
        }
        failure {
            slackSend color: "danger", message: "❌ Build Failed: ${env.JOB_NAME} #${env.BUILD_NUMBER}"
        }
    }
}
