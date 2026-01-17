pipeline {
    agent any

    tools {
        jdk 'jdk21'
        maven 'maven3'
    }

    environment {
        // ==== Project Info ====
        GROUP_ID    = 'com.example'
        ARTIFACT_ID = 'solar-system'
        VERSION     = '1.0-SNAPSHOT'

        // ==== Sonar ====
        SONAR_PROJECT_KEY  = 'solar-system'
        SONAR_PROJECT_NAME = 'solar-system'

        // ==== Nexus ====
        NEXUS_URL   = '13.232.240.121:8081'
        NEXUS_REPO  = 'maven-snapshots'
        NEXUS_CREDS = 'nexus-creds'
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
                sh '''
                mkdir -p trivy-report

                trivy fs \
                  --severity HIGH,CRITICAL \
                  --format json \
                  --output trivy-report/trivy-report.json .

                trivy fs --severity CRITICAL --exit-code 1 .
                '''
            }
        }

        stage('Maven Package') {
            steps {
                sh 'mvn package -DskipTests'
            }
        }

        stage('Verify Artifact') {
            steps {
                sh 'ls -lh target'
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
                            file: 'trivy-report/trivy-report.json',
                            type: 'json'
                        ]
                    ]
                )
            }
        }

        stage('Deployment Approval') {
            steps {
                input message: 'Approve deployment using Nexus artifact?',
                      ok: 'Proceed'
            }
        }

        stage('Trigger Deployment Pipeline') {
            steps {
                build job: 'solar-system-deploy',
                      parameters: [
                          string(name: 'VERSION', value: "${VERSION}")
                      ]
            }
        }
    }

    post {
        success {
            echo 'CI pipeline completed successfully'
        }
        aborted {
            echo 'Deployment was declined by user'
        }
        failure {
            echo 'CI pipeline failed – check logs'
        }
        always {
            archiveArtifacts artifacts: 'trivy-report/**', fingerprint: true
        }
    }
}