pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                sh '''
                docker build -t check-canvas ./from_canvas/
                '''
            }
        }
    }
}
