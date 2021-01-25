(ps aux | grep [D]ocker.app/Contents/MacOS/Docker >> /dev/null) \
    || (echo "Starting Docker..." && open -a Docker && sleep 30)
docker-compose pull
docker-compose -f ../build/docker-compose-dev.yml up -d
docker-compose run --rm waiter dockerize -wait tcp://localhost:5432 -timeout 1m
python manage.py migrate