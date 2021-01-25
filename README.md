# weather-forecasts-drf
An Django REST Framework application for pulling, caching, searching and exporting weather forecast information

## Project Structure

`api` — backend application

`build` — build scripts, docker/docker-compose

## How to run
1. Create a virtual env `python3 -m venv venv`
2. Activate venv `source ./venv/bin/activate`
3. Configure local postgres database `./scripts/setup-dev.sh`
4. Replace `__YOUR_OPEN_WEATHER_MAP_API_KEY_HERE__` in `api/.env` with your Open Weather Map API Key 
4. Start django server `cd api && python manage.py runserver`

## Features
### API features
1. Trigger a weather search for a particular lat long. (e.g. lat=33.441792&amp;lon=-94.037689) from a weather data integration
2. Return stored weather data and their metadata based on applied filters/search.
3. Export filtered data as CSV with selected columns of your choice.
### Development features
#### API documentation
You can see the API documentation at `/api/v1/doc` endpoint
#### Code styling
Hooks have been already setup for checking/fixing code styling before commits
#### Continuous Integration
CircleCI is configured to test the application and check code styling