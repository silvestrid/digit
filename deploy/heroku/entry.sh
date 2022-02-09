#!/bin/bash

set -eu

echo "changin nginx PORT to $PORT"
sed -i 's/PORT/'"$PORT"'/g' /digit/nginx.conf
# export DIGIT_PUBLIC_URL=${DIGIT_PUBLIC_URL:-https://$HEROKU_APP_NAME.herokuapp.com}
