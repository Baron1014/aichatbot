# personal settings
GIT_NAME="Baron"
GIT_EMAIL="nm6101080@gs.ncku.edu.tw"
GITLAB_LOGIN=Baron

# docker configuration
COURSE=aichatbot

## setup docker web service port mapping (format => host:container)
PORT_MAPPING=3000:3000
NGINX_PORT=8082

# project parameters, must be consistent with gitlab URLs
# start docker env with / without uWSGI and nginx proxy
RUN_FLASK=true

COURSE_GITLAB="aichatbot_fall_2021"

#projects without flask
PROJECT="test"

#flask project list
FLASK_PROJECT="scream"

# mount to /workspace/www in container
CURRENT_FLASK_FOLDER=scream
