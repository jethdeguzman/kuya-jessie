#!/bin/bash

deploy() {
    docker run -p 0.0.0.0:80:80 -p 0.0.0.0:443:443 --volumes-from kuyajessie --name nginx --restart always --link kuyajessie:kuyajessie -d nginx:1.10
}

undeploy() {
    docker stop nginx
    docker rm nginx
}

case "$1" in
    build)
        build $2
        ;;
    deploy)
        deploy $2
        ;;
    undeploy)
        undeploy $2
        ;;
    *)
        echo "nginx deploy|undeploy"
esac