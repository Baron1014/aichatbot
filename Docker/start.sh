#!/bin/bash

welcome_message(){
    cat << EOF
  
Welcome to use the Playlab working environment

This docker environment is built for the AIChatbot course 
All projects are in the /workspace/projects directory
The nginx web server root is in the /workspace/www directory

EOF
}

source /Docker/env_setup.sh

# setup personal repo 
git config --global user.name $GIT_NAME
git config --global user.email $GIT_EMAIL
git config --global core.editor vim

sudo cp /Docker/ngrok /bin/
sudo chmod 755 /bin/ngrok

if [ $RUN_FLASK == true ]; then
    running=$(ps -ef | grep uwsgi | grep -v 'grep')
    if [[ "$running" == "" ]]; then 
       uwsgi -d /tmp/uWSGI.log /Docker/uWSGI.ini
    fi
fi

welcome_message

