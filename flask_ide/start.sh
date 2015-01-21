#!/bin/bash

export SERVER_COMMAND="python flask_ide/manage.py runserver --host=0.0.0.0 --port=$PORT";
if [ "$1" == "twisted" ]; then
    export SERVER_COMMAND="twistd -n web --port $FLASK_PORT --wsgi=app.app";
fi

$SERVER_COMMAND
