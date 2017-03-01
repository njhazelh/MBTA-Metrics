#!groovy

pipeline {
    agent any
    stages {
        stage('test') {
            steps {
                sh '''#!/bin/bash
                    if [[ -d mbta-env ]]; then
                        rm -rf mbta-env/
                    fi
                    . ./bin/activate.sh
                    python3 -m nose2 -c unittest.cfg
                '''
                script {
                    def lintErr = sh script: '''#!/bin/bash
                            . ./bin/activate.sh
                            mkdir htmllint
                            python3 -m pylint --rcfile=.pylintrc -f html mbtaalerts > htmllint/index.html
                        ''', returnStatus: true
                    echo "Lint error: $lintErr"
                    if (lintErr != 0 && lintErr < 4) {
                        error "Found fatal error during Linting"
                    }
                }
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
            publishHTML(target: [
                allowMissing: false,
                alwaysLinkToLastBuild: false,
                keepAll: true,
                reportDir: 'htmllint',
                reportFiles: 'index.html',
                reportName: 'Linter Report'
            ])
            publishHTML(target: [
                allowMissing: false,
                alwaysLinkToLastBuild: false,
                keepAll: true,
                reportDir: 'htmlcov',
                reportFiles: 'index.html',
                reportName: 'Coverage Report'
            ])
            deleteDir()
        }
        success {
            slackSend color: 'good',
                message: "Pipeline for ${env.BRANCH_NAME} passed: ${env.BUILD_URL}"
        }
        failure {
            slackSend color: 'danger',
                message: "Pipeline for ${env.BRANCH_NAME} failed: ${env.BUILD.URL}"
        }
    }
}
