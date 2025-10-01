#!/bin/bash
docker run --rm \
  -v $(pwd):/usr/src \
  -w /usr/src \
  sonarsource/sonar-scanner-cli \
  sonar-scanner \
  -Dsonar.projectKey=devsecops-flask-project \
  -Dsonar.sources=. \
  -Dsonar.host.url=http://host.docker.internal:9000 \
  -Dsonar.login=$1
