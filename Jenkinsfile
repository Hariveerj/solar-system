pipeline {
    agent any

    tools {
        jdk 'jdk21'
        maven 'maven3'
    }

    environment {
        NEXUS_URL   = '13.234.77.86:8081'
        NEXUS_REPO  = 'maven-releases'
        NEXUS_CREDS = 'nexus-creds'

        GROUP_ID    = 'com.example'
        ARTIFACT_ID = 'solar-system'
        VERSION     = '1.0.0'
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
                      -Dsonar.projectKey=solar-system \
                      -Dsonar.projectName=solar-system
                    """
                }
            }
        }

        stage('Install Trivy (if missing)') {
            steps {
                sh '''
                if ! command -v trivy >/dev/null 2>&1; then
                  echo "Installing Trivy..."
                  apt-get update -y
                  apt-get install -y wget tar
                  wget https://github.com/aquasecurity/trivy/releases/download/v0.68.2/trivy_0.68.2_Linux-64bit.tar.gz
                  tar -xzf trivy_0.68.2_Linux-64bit.tar.gz
                  mv trivy /usr/local/bin/
                fi
                trivy --version
                '''
            }
        }

        stage('Trivy File System Scan') {
            steps {
                sh '''
                mkdir -p trivy-report

                trivy fs \
                  --severity HIGH,CRITICAL \
                  --format json \
                  --output trivy-report/trivy-report.json \
                  .

                trivy fs \
                  --severity CRITICAL \
                  --exit-code 1 \
                  .
                '''
            }
        }

        stage('Maven Package') {
            steps {
                sh 'mvn package -DskipTests'
            }
        }

        stage('Upload JAR to Nexus') {
            steps {
                nexusArtifactUploader(
                    nexusVersion: 'nexus3',
                    protocol: 'http',
                    nexusUrl: "${NEXUS_URL}",
                    repository: "${NEXUS_REPO}",
                    credentialsId: "${NEXUS_CREDS}",
                    groupId: "${GROUP_ID}",
                    version: "${VERSION}",
                    artifacts: [
                        [
                            artifactId: "${ARTIFACT_ID}",
                            classifier: '',
                            file: "target/${ARTIFACT_ID}-${VERSION}.jar",
                            type: 'jar'
                        ]
                    ]
                )
            }
        }

        stage('Upload Trivy Report to Nexus') {
            steps {
                nexusArtifactUploader(
                    nexusVersion: 'nexus3',
                    protocol: 'http',
                    nexusUrl: "${NEXUS_URL}",
                    repository: "${NEXUS_REPO}",
                    credentialsId: "${NEXUS_CREDS}",
                    groupId: "${GROUP_ID}",
                    version: "${VERSION}",
                    artifacts: [
                        [
                            artifactId: "${ARTIFACT_ID}-security-report",
                            classifier: '',
                            file: "trivy-report/trivy-report.json",
                            type: 'json'
                        ]
                    ]
                )
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'trivy-report/**', fingerprint: true
        }
        success {
            echo 'CI/CD Pipeline completed successfully'
        }
        failure {
            echo 'CI/CD Pipeline failed – check logs'
        }
    }
}