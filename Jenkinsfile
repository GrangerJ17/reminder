pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                sh '''
                docker build -t check-canvas ./from_canvas
                docker run \
                 --network psql-connecy \
                 --env-file from_canvas/.env \
                 -v $(pwd)/from_canvas/.env:/app/.env \
                check-canvas

                '''
            }
        }
    }
}
