# mnist_web_with_cassandra

![Docker Build Status](https://img.shields.io/badge/docker-pushed-brightgreen.svg)

Running tensorflow's mnist with web server, cassandra and docker.

## Fast launch via docker
Just clone the project and run the commands below. or pull it from [Docker Hub](https://hub.docker.com/r/gtbl2012/mnist-web).
```
cd mnist_web_with_cassandra
docker build -t mnist_web:v1.0 .
docker run --name "mnist_web"  -e CASSANDRA_HOST={your cassandra host:port} -p 80:80 -d mnist-web:v1.0
```

## Run in local mechine
1. install requirements
```
pip install -r requirements.txt
```
2. train predict dataset
```
python3 ./lib/mnist_deep_train.py
python3 ./lib/mnist_softmax_train.py
```
3. set cassandra host and launch web server
```
export CASSANDRA_HOST={your cassandra host:port}
python3 app.py
```

## Try the project
visit [localhost](http://localhost/) after launched the project.

or try our [online version](http://mnist.gtbl2012.cn).(may be not available)
