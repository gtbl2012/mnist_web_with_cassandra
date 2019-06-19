FROM ubuntu:latest

MAINTAINER admin@gtbl2012.cn

# Change source
COPY ./sources.list /etc/apt/sources.list

# Install basic dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
#        build-essential \
#        cmake \
#        wget \
#        libsnappy-dev \
        python3-dev \
        python3-pip \
        python3-setuptools
#        tzdata \
#        vim

# Set timezone
RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime

# Set locale
ENV LANG C.UTF-8 LC_ALL=C.UTF-8

# Initialize work environment
RUN pip3 install wheel
RUN pip3 install --upgrade setuptools
RUN pip3 install werkzeug==0.14.1 \
                 tensorflow \
                 flask \
                 cassandra-driver \
                 pillow \
                 -i https://pypi.tuna.tsinghua.edu.cn/simple

# Initialize workspace
RUN mkdir /workspace
COPY ./ /workspace

# Train basic data set (Already built)
# RUN python3 /workspace/lib/mnist_softmax_train.py
# RUN python3 /workspace/lib/mnist_deep_train.py

ENTRYPOINT ["python3", "/workspace/app.py"]

WORKDIR /workspace

EXPOSE 80