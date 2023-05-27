## How to deploy python API in Google cloud run service

- Install gcloud sdk in your system
- Create a New project (in google cloud console - prefer to do it via browser - easier)
- Note down the project id (PROJECT_ID)
- In your terminal type `gcloud init`
- Follow the instruction accordingly
- `gcloud config set project project <PROJECT_ID>` to activate the current project

### Creating a project

- Create a folder containing following file

```
main.py -> main python file (Flask)
requirements.txt -> python requirements
Dockerfile
.dockerignore
.gcloudignore
```

#### Dockerfile

```dockerfile
# https://hub.docker.com/_/python
FROM python:3.11-slim

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

# Install production dependencies.
RUN pip install --no-cache-dir -r requirements.txt

# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
# Timeout is set to 0 to disable the timeouts of the workers to allow Cloud Run to handle instance scaling.
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app

# This command is used to start a Gunicorn server that runs the application 
# defined in the main.py file using the app object (assumed to be a Flask
# application in this case).

```

## Build

```sh
docker build --tag uclchem:python .
```

This command is used to build a Docker image named "helloworld" with the tag "python" using the Dockerfile in the current directory (denoted by the dot at the end of the command).

Note that the "helloworld" and "python" names used in this command are arbitrary and can be changed to whatever names you prefer.

## Run Locally

```sh
docker run -p 9090:8080 -e PORT=8080 uclchem:python
# docker run --rm -p 9090:8080 -e PORT=8080 uclchem:python
```

This command is used to run a Docker container based on the "helloworld" image with the tag "python" that was built using the Dockerfile.

The "-p 9090:8080" option maps port 8080 inside the container to port 9090 on the host machine. This allows the application running inside the container to be accessible from the host machine using the URL <http://localhost:9090>.

The "-e PORT=8080" option sets an environment variable named "PORT" inside the container with a value of 8080. This tells the application running inside the container to listen on port 8080.

The "--rm" option tells Docker to automatically remove the container when it exits.

In development mode:

```sh
docker run -it -p 9090:8080 -e PORT=8080 --mount "type=bind, source=$(pwd), target=/app/" uclchem:python
```

## Deploy

```sh
# Set an environment variable with your GCP Project ID
export GOOGLE_CLOUD_PROJECT=uclchem-388009

# Submit a build using Google Cloud Build
gcloud builds submit --tag gcr.io/uclchem-388009/uclchem
# or gcloud builds submit --tag gcr.io/${GOOGLE_CLOUD_PROJECT}/uclchem

# Deploy to Cloud Run
gcloud run deploy uclchem --image gcr.io/uclchem-388009/uclchem
```
