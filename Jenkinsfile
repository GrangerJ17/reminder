pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                sh '''
                docker build -t check-canvas ./from_canvas/
                docker run --network psql-connecy --env-file .env from-canvas
                '''
            }
        }
    }
}
