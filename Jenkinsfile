pipeline {
    agent any

    stages {
        stage('Build') {
            step {
            withCredentials([
                    string(credentialsId: 'PGPASSWORD', variable: 'PGPASSWORD'),
                    string(credentialsId: 'CANVASDB', variable: 'CANVASDB'),
                    string(credentialsId: 'DISCORD_WEBHOOK_URL', variable: 'DISCORD_WEBHOOK_URL'),
                    string(credentialsId: 'PGUSER', variable: 'PGUSER'),
                    string(credentialsId: 'SYSPGPORT', variable: 'SYSPGPORT'),
                    string(credentialsId: 'HOST_TO_DB', variable: 'HOST_TO_DB'),
                    string(credentialsId: 'CANVAS_TOKEN', variable: 'CANVAS_TOKEN')
            ]) {
                    sh '''
                    docker run \
                    --network psql-connecy \
                    -e PGPASSWORD \
                    -e CANVASDB \
                    -e DISCORD_WEBHOOK_URL \
                    -e PGUSER \
                    -e SYSPGPORT \
                    -e HOST_TO_DB \
                    -e CANVAS_TOKEN \
                    check-canvas
                        '''
                }
           }
        }
    }
}
