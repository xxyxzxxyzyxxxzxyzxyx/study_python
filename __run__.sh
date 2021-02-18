#!/bin/bash


case "$1" in
    "build")
        docker build \
            --rm \
            --pull \
            --no-cache \
            -t study_python \
            -f Dockerfile \
            .
        ;;
    "run")
        docker run \
             -it \
             -v /etc/passwd:/etc/passwd:ro \
             -v /etc/group:/etc/group:ro \
             -v ${PWD}:/home \
             -u $(id -u ${USER}):$(id -g ${USER}) \
             -p 8888:8888 \
             study_python \
             /bin/bash
        ;;
    "jupyter")
        /home/xxyxzxxyzyxxxzxyzxyx/.local/bin/jupyter notebook \
	    --port=8888 \
	    --ip=0.0.0.0 \
	    --allow-root \
	    --no-browser \
        --NotebookApp.token=''
        ;;
    *)
        echo "undefined argment"
        ;;
esac
