# foo-d
> _Tutorial for a location based service._

## Introduction
This tutorial walks through how to build the basic framework for a location based service in python. This example it to find the nearest place to eat given a location as a postcode.

The design thinking is detailed in the file `DESIGN.md` if you wish to understand why and how I chose to solve the problem in the way that I did.

## Pre-requisits
The application is run with `docker` and `docker-compose`. Please use the following links to install.

 * [docker][1]
 * [docker-compose][2]

## Runing the Application
First clone the repository with:
 ```bash
 git clone https://github.com/diversemix/foo-d.git
 ```

Then change to the root folder then build and start with docker-compose:
 ```bash
 cd foo-d
 docker-compose build
 docker-compose up -d
 ```

 Finally open this link in your browser: http://127.0.0.1:8080/

## Loading other data files

The configuration for the application is stored within the `data` directory. This contains the names of the csv files that will be used when the foo-d-service is loaded. You may wish to add files to this folder and make sure that you reference them within the configuration file: `config.json`
[1]: https://docs.docker.com/engine/installation/
[2]: https://docs.docker.com/compose/install/
