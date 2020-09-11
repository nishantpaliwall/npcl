pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                echo 'This is my first jenkins file Build Stage'
            }
        }
        stage('DockerImageBuild')    {
            agent {
                dockerfile {
                    dir 'Python/firstTry/'
                    filename 'Dockerfile'
                    registryCredentialsId 'NishantDockerHub'
                    registryUrl 'https://hub.docker.com/u/nishantpaliwall'
                }
            }
            steps {
                echo 'This docker image Build Stage'
            }

        }
    }
}
