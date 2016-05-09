=============
Install
=============

The Meerkat framework is developed and deployed using docker(www.docker.com). Docker provides lightweight containers that are completely replicable over many different development and production machines. For development we use docker-compose to administer these containers. This page will detail how to get the meerkat dev environemtn up and running.

Meerkat consists of three components: Abacus, Frontend and API. Each of these components have their own docker container. Then we have one docker container running nginx (a webserver), one container running Postgresql (main database), one container running RabbitMQ (lightweight database) and one container setting up the documentation.

To start of you will need to clone the three meerkat repositories (abacus, frontend and api) into a folder, then also clone the meerkat_docs into the same folder. The docker setup and docker-compose files are in the meerkat_demo repo, it needs to be cloned into the same folder as all the above repositries. You should then have a folder structure that looks like this::

  Top level folder
    - meerkat_abacus
    - meerkat_api
    - meerkat_frontend
    - meerkat_docs
    - meerkat_demo

To start the whole site it should only be required to start docker-compose in the meerkat_demo folder by running::

  $ docker-compose up -d

The first time this command is run a lot of images are downloaded and many packages are installed. This will take some time. Once the command has finished running you should have all the docker containers up and running. You can verify this by running (depending on how docker is setup you might need to use sudo)::

  $ docker ps

This site is now almost ready, we only need to setup some frontend resources by running::

  $ docker exec meerkatdemo_frontend_1 setup_static

This will download and install various NPM modules, download JS and CSS components via Bower and the run gulp to prepare all the static assets. After this you should be able to access the meerkat framework on localhost (or potentially some other address depending on how Docker is setup). To access the technical site the username/password is admin/secret. For development purposes it is useful to read up on docker and docker-compose commands. Mainly to restart containers and read the logs.

Note: If using the infrastructure repositry instead of the meerkat_demo repo you can follow exactly the same steps. Just run all commands from the dev folder and replace meerkat_demo with dev in the setup static command. 

