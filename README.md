Deployment
----------

    git clone https://github.com/dankolbman/tblog
    cd tblog
    docker build -t tblog_app:v1 .
    docker run -d -p 80:8000 tblog_app:v1

To pull and update server:

    docker exec <cont id> git pull
    docker exec <cont id> supervisorctl restart tblog

