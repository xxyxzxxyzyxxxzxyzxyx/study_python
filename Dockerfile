# Dockerfile
FROM python:3


# apt-get
RUN apt-get update \
    && apt-get install -y \
        sudo \
        curl \
        gosu \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*


# 
