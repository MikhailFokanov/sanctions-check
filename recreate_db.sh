#!/bin/bash

docker rm -f sc_postgres
docker-compose up -d postgres