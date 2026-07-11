pipeline {
    agent any
    stages {
        stage('Checkout') { steps { checkout scm } }
        stage('Python Version') { steps { bat 'python --version' } }
        stage('Prepare Virtual Environment') {
            steps { bat 'python -m venv .venv' }
        }
        stage('Install Dependencies') {
            steps { bat '.venv\\Scripts\\python.exe -m pip install --upgrade pip && .venv\\Scripts\\python.exe -m pip install -r requirements.txt' }
        }
        stage('Unit Tests and Coverage') {
            steps {
                bat '.venv\\Scripts\\python.exe -m pytest --junitxml=test-results.xml --cov=taskflow --cov-report=term-missing --cov-report=xml:coverage.xml --cov-report=html'
            }
        }
    }
    post {
        always {
            junit allowEmptyResults: true, testResults: 'test-results.xml'
            archiveArtifacts allowEmptyArchive: true, artifacts: 'coverage.xml,htmlcov/**'
        }
        success { echo 'TaskFlow continuous testing pipeline succeeded.' }
        failure { echo 'TaskFlow pipeline failed. Review test output.' }
    }
}
