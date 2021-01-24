# weather-forecasts-drf
An Django REST Framework application for pulling, caching, searching and exporting weather forecast information

# weatherapi

`api` — backend application

`build` — build scripts, docker/docker-compose

### How to run

#### Development mode

`docker-compose -f build/docker-compose-dev.yml up`

will run only services needed for development like PostgreSQL, Redis etc

`docker-compose -f build/docker-compose-api.yml up`

will run all needed services and API (backend application)
