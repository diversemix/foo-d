#!/bin/bash
docker exec -it food_foo-d-service_1 curl -v -H 'Content-Type:text/json'  \
    -X POST -d '{ "postcode" : "KT10 9AX", "radius" : "100000" }' \
    http://127.0.0.1:5000/v1/query
