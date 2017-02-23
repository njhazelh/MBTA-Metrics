pipeline {
    agent { docker 'python:3.5' }
    stages {
        stage('test') {
            steps {
                sh '''#!/bin/bash -l
                    source activate.sh
                    nose2 --plugin nose2.plugins.junitxml --junit-xml
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
            junit 'nose2-junit.xml'
            deleteDir()
        }
    }
}
