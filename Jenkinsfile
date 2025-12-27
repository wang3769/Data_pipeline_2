pipeline {
    agent { docker { image 'finance-pipeline_1.0.0' } }

    stages {

        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/wang3769/Data_pipeline_2.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'pip3 install -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                // Run the single test file inside the `test` folder
                sh 'pytest -q test/test.py'
            }
        }

        stage('Build Project Docker Image') {
            steps {
                echo 'Building Docker Image...'
                sh 'docker build -t finance-pipeline .'
            }
        }

        stage('test Project Docker Image') {
            steps {
                echo 'testing Docker Image...'

            }
        }

        stage('deploy Project Docker Image') {
            steps {
                echo 'deploying Docker Image...'

            }
        }
    }

    post {
        success {
            echo 'CI Pipeline Successful!'
        }
    }
}
