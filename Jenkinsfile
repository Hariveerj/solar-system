pipeline {
    agent any

    tools {
        jdk 'jdk21'
        maven 'maven3'
    }

    environment {
        SONAR_PROJECT_KEY = 'solar-system'
        SONAR_PROJECT_NAME = 'solar-system'
        TRIVY_REPORT_DIR = 'trivy-report'
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Maven Build') {
            steps {
                sh 'mvn clean compile'
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('sonarqube-server') {
                    sh """
                    mvn sonar:sonar \
                      -Dsonar.projectKey=${SONAR_PROJECT_KEY} \
                      -Dsonar.projectName=${SONAR_PROJECT_NAME}
                    """
                }
            }
        }

        stage('Trivy File System Scan') {
            steps {
                sh """
                mkdir -p ${TRIVY_REPORT_DIR}

                # JSON report
                trivy fs \
                  --severity HIGH,CRITICAL \
                  --format json \
                  --output ${TRIVY_REPORT_DIR}/trivy-report.json \
                  .

                # Table report (console friendly)
                trivy fs \
                  --severity HIGH,CRITICAL \
                  --format table \
                  .

                # Fail build if CRITICAL vulnerabilities found
                trivy fs \
                  --severity CRITICAL \
                  --exit-code 1 \
                  .
                """
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'trivy-report/**', fingerprint: true
        }

        success {
            echo 'Pipeline completed successfully'
        }

        failure {
            echo 'Pipeline failed (check Sonar or Trivy results)'
        }
    }
}