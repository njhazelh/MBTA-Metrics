pipeline {
    agent any
    stages {
        stage('test') {
            steps {
                sh '''#!/bin/bash
                    if [[ -d mbta-env ]]; then
                        rm -rf mbta-env/
                    fi
                    . activate.sh
                    python3 -m nose2 --plugin nose2.plugins.junitxml --junit-xml
                '''
            }
        }
        stage('deploy') {
            when {
                branch 'master'
            }
            steps {
                echo "I would deploy, if I were setup to do so"
            }
        }
    }
    post {
        always {
            echo "Cleaning up and archiving"
            junit 'nose2-junit.xml'
            deleteDir()
        }
        success {
            slackSend color: 'good',
                message: "Pipeline for ${env.BRANCH_NAME} passed!"
        }
        failure {
            slackSend color: 'danger',
                message: "Pipeline for ${env.BRANCH_NAME} failed!"
        }
    }
}
