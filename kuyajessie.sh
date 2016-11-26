#!/bin/bash

build() {
    docker build -t codeawesome/kuyajessie .
}

deploy() {
    docker run -p 0.0.0.0:8000:8000 --name kuyajessie -d codeawesome/kuyajessie
}

undeploy() {
    docker stop kuyajessie
    docker rm kuyajessie
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
        echo "kuyajessie build|deploy|undeploy"
esac
