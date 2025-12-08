pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/YOUR_USERNAME/finance-pipeline-repo.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'pip3 install -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                sh 'pytest -q'
            }
        }

        stage('Build Project Docker Image') {
            steps {
                sh 'docker build -t finance-pipeline .'
            }
        }
    }

    post {
        success {
            echo 'CI Pipeline Successful!'
        }
    }
}
