pipeline {
    agent any

    tools {
        jdk 'jdk21'
        maven 'maven3'
    }

    environment {
        // Project
        GROUP_ID    = 'com.example'
        ARTIFACT_ID = 'solar-system'
        VERSION     = '1.0-SNAPSHOT'

        // Sonar
        SONAR_PROJECT_KEY  = 'solar-system'
        SONAR_PROJECT_NAME = 'solar-system'

        // Nexus
        NEXUS_URL   = '13.234.202.23:8081'
        NEXUS_REPO  = 'maven-snapshots'
        NEXUS_CREDS = 'nexus-creds'
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        
        //  ===== AI CODE REVIEW ======
		
        stage('AI Code Review') {
            steps {
                sh '''
                python3 ai-agent/code_review.py \
                  > ai-code-review.txt || true
                cat ai-code-review.txt || true
                '''
            }
        }

        stage('Maven Build') {
            steps {
                sh 'mvn clean package -DskipTests'
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('sonarqube-server') {
                    sh '''
                    mvn org.sonarsource.scanner.maven:sonar-maven-plugin:sonar \
                      -Dsonar.projectKey=${SONAR_PROJECT_KEY} \
                      -Dsonar.projectName=${SONAR_PROJECT_NAME}
                    '''
                }
            }
        }

        stage('Trivy File System Scan') {
            steps {
                sh '''
                mkdir -p trivy-report
                trivy fs . \
                  --severity HIGH,CRITICAL \
                  --format json \
                  --output trivy-report/trivy-report.json
                '''
            }
        }

        // ====== AI SECURITY REVIEW ======

        stage('AI Security Review') {
            steps {
                sh '''
                python3 ai-agent/security_review.py \
                  trivy-report/trivy-report.json \
                  > ai-security.txt || true
                cat ai-security.txt || true
                '''
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
                    artifacts: [[
                        artifactId: "${ARTIFACT_ID}",
                        file: "target/${ARTIFACT_ID}-${VERSION}.jar",
                        type: 'jar'
                    ]]
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
                    artifacts: [[
                        artifactId: "${ARTIFACT_ID}-security-report",
                        file: "trivy-report/trivy-report.json",
                        type: 'json'
                    ]]
                )
            }
        }

        // ===== AI AUTO APPROVAL ======
        stage('AI Deployment Approval') {
            steps {
                script {
                    def decision = sh(
                        script: '''
                        python3 ai-agent/deploy_decision.py \
                          trivy-report/trivy-report.json || echo APPROVE
                        ''',
                        returnStdout: true
                    ).trim()

                    echo "AI Decision: ${decision}"

                    if (decision != "APPROVE") {
                        error " Deployment blocked by AI"
                    }
                }
            }
        }

        stage('Deployment Approval') {
            steps {
                input message: 'Approve deployment?',
                      ok: 'Proceed'
            }
        }

        stage('Trigger Phase-2') {
            steps {
                build job: 'solar-system-deploy',
                      parameters: [
                        string(name: 'VERSION', value: "${VERSION}")
                      ]
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'trivy-report/**', fingerprint: true
        }
        success {
            echo '✅ Phase-1 completed successfully'
        }
        failure {
            echo '❌ Phase-1 failed'
        }
    }
}