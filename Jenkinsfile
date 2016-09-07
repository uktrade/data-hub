node {
   stage 'Checkout'
   ws {
     checkout scm
   }

   stage 'Unit test'
   step([$class: 'GitHubSetCommitStatusBuilder'])
   wrap([$class: 'AnsiColorBuildWrapper', 'colorMapName': 'XTerm']) {
     sh 'echo $WORKSPACE'
     sh 'cd $WORKSPACE'
     sh 'pwd'
     sh 'KORBEN_CONF_PATH=korben/jenkins.yml python setup.py test'
   }

   stage 'Clean workspace'
   step([$class: 'WsCleanup'])
}
