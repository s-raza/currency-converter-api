Kubernetes Powershell Script
============================

A Windows Powershell script ``k8s.ps1`` is provided that automates most of the steps in the
:doc:`Kubernetes General Commands <general_cmds>` section.

This script automates the below steps from the
:doc:`Kubernetes General Commands <general_cmds>` section.

- Sets up the environment for `kubectl` if not already set.
- Automatically sets up the configuration using the `.env` file if not already set.
- Option to build the Docker images and run Pods in one go.
- Option to expose the React UI and forward the port for either the production build
  using NGINX server or the React development server.
- Wait for the API backend to startup before exposing the React UI.
- Delete the Kubernetes cluster and wait for all the pods to terminate before showing
  confirmation for the delete operation.


Minikube Installation
---------------------

Follow the installation and starting instructions :ref:`here <general-minikube-installation>`
for Minikube.

Install kubectl
---------------

Follow the installation instructions :ref:`here <general-install-kubectl>` for kubectl.

NGINX Production Build Server
-----------------------------

With Building Images
++++++++++++++++++++

This part should be done with the ``-build`` switch if running for the first time.
All subsequent runs will not require building images unless there is any change in
the source code. It will take sometime to build the images for the first time.

This exposes the production build using NGINX server by default if the ``-dev`` switch
is not provided.

To build the images and run in one go, run the below command.

.. code-block::

    currency-converter-api> .\k8s.ps1 -build
    ▶ Building Docker images...

    [+] Building 4.3s (62/62) FINISHED
    => [currency-converter-prod-server internal] load build definition from Dockerfile.nginx                                       0.0s
    => => transferring dockerfile: 649B                                                                                            0.0s
    => [currency-converter-updater internal] load build definition from Dockerfile.db                                              0.0s
    => => transferring dockerfile: 1.40kB                                                                                          0.0s
    => [currency-converter-dev-server internal] load build definition from Dockerfile.frontend                                     0.1s
    => => transferring dockerfile: 907B                                                                                            0.0s
    => [currency-converter-api internal] load build definition from Dockerfile.api                                                 0.1s
    => => transferring dockerfile: 1.40kB                                                                                          0.0s
    => [currency-converter-prod-server internal] load .dockerignore                                                                0.1s
    => => transferring context: 34B                                                                                                0.0s
    => [currency-converter-updater internal] load .dockerignore                                                                    0.1s
    => => transferring context: 34B                                                                                                0.0s
    => [currency-converter-dev-server internal] load .dockerignore                                                                 0.1s
    => => transferring context: 34B                                                                                                0.0s
    => [currency-converter-api internal] load .dockerignore                                                                        0.1s
    => => transferring context: 34B                                                                                                0.0s
    => [currency-converter-prod-server internal] load metadata for docker.io/library/nginx:1.23.3-alpine-slim                      2.8s
    => [currency-converter-dev-server internal] load metadata for docker.io/library/node:18.12.1-slim                              2.8s
    => [currency-converter-updater internal] load metadata for docker.io/library/python:3.9.16-slim                                2.4s
    => [currency-converter-updater internal] load build context                                                                    0.2s
    => => transferring context: 1.83kB                                                                                             0.2s
    => [currency-converter-updater  1/16] FROM docker.io/library/python:3.9.16-slim@sha256:50c261237b02d3597d9ad74e72f6d67daadb14  0.0s
    => [currency-converter-api internal] load build context                                                                        0.2s
    => => transferring context: 226.77kB                                                                                           0.2s
    => CACHED [currency-converter-api  2/16] RUN apt-get update; apt-get install curl -y                                           0.0s
    => CACHED [currency-converter-api  3/16] RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry POETRY_VER  0.0s
    => CACHED [currency-converter-api  4/16] RUN groupadd -r appgrp                                                                0.0s
    => CACHED [currency-converter-api  5/16] RUN useradd -r -m appusr                                                              0.0s
    => CACHED [currency-converter-api  6/16] RUN usermod -a -G appgrp appusr                                                       0.0s
    => CACHED [currency-converter-api  7/16] WORKDIR /app/backend                                                                  0.0s
    => CACHED [currency-converter-api  8/16] RUN chown appusr:appgrp /app/backend                                                  0.0s
    => CACHED [currency-converter-updater  9/16] COPY --chown=appusr:appgrp ./backend/pyproject.toml ./backend/poetry.lock* ./     0.0s
    => CACHED [currency-converter-updater 10/16] RUN poetry install --no-root --without dev                                        0.0s
    => CACHED [currency-converter-updater 11/16] COPY --chown=appusr:appgrp ./backend/db ./db                                      0.0s
    => CACHED [currency-converter-updater 12/16] COPY --chown=appusr:appgrp ./backend/ext_api ./ext_api                            0.0s
    => CACHED [currency-converter-updater 13/16] COPY --chown=appusr:appgrp ./backend/utils ./utils                                0.0s
    => CACHED [currency-converter-updater 14/16] COPY --chown=appusr:appgrp ./backend/settings.py ./                               0.0s
    => CACHED [currency-converter-updater 15/16] COPY --chown=appusr:appgrp ./backend/start_updates.py ./                          0.0s
    => CACHED [currency-converter-updater 16/16] COPY --chown=appusr:appgrp ./.env ./                                              0.0s
    => [currency-converter-prod-server] exporting to image                                                                         0.7s
    => => exporting layers                                                                                                         0.0s
    => => writing image sha256:36d117726c9c61621412badb93275919d4a80bf4da97a73ab0bfd302c2238b75                                    0.0s
    => => naming to docker.io/library/currency-converter-updater                                                                   0.0s
    => => writing image sha256:4e17c3f783f02954c62264725e5f8dbb78d68c9ff2db04a0096b50ab09aaa5cd                                    0.0s
    => => naming to docker.io/library/currency-converter-api                                                                       0.0s
    => => writing image sha256:1b67c6d562e79bb330ce9dd3b33dbffcf106860707dc18ee8c128ecb903230fc                                    0.0s
    => => naming to docker.io/library/currency-converter-dev-server                                                                0.0s
    => => writing image sha256:a2c366ae193cbaa1677bffbc84ca0c0360adfa4c8d69c0707610bca8d4dd22b9                                    0.0s
    => => naming to docker.io/library/currency-converter-prod-server                                                               0.0s
    => CACHED [currency-converter-api  9/16] COPY --chown=appusr:appgrp ./backend/pyproject.toml ./backend/poetry.lock* ./         0.0s
    => CACHED [currency-converter-api 10/16] RUN poetry install --no-root --without dev                                            0.0s
    => CACHED [currency-converter-api 11/16] COPY --chown=appusr:appgrp ./backend/currency_api ./currency_api                      0.0s
    => CACHED [currency-converter-api 12/16] COPY --chown=appusr:appgrp ./backend/db ./db                                          0.0s
    => CACHED [currency-converter-api 13/16] COPY --chown=appusr:appgrp ./backend/utils ./utils                                    0.0s
    => CACHED [currency-converter-api 14/16] COPY --chown=appusr:appgrp ./backend/settings.py ./                                   0.0s
    => CACHED [currency-converter-api 15/16] COPY --chown=appusr:appgrp ./backend/api_main.py ./                                   0.0s
    => CACHED [currency-converter-api 16/16] COPY --chown=appusr:appgrp ./.env ./                                                  0.0s
    => [currency-converter-prod-server base 1/1] FROM docker.io/library/node:18.12.1-slim@sha256:70bf84739156657c85440e6a55a3d77a  0.0s
    => [currency-converter-dev-server internal] load build context                                                                 0.3s
    => => transferring context: 841.71kB                                                                                           0.2s
    => [currency-converter-prod-server internal] load build context                                                                0.4s
    => => transferring context: 842.90kB                                                                                           0.4s
    => [currency-converter-prod-server stage-1 1/5] FROM docker.io/library/nginx:1.23.3-alpine-slim@sha256:49b61e3ddce9e2e4b639dc  0.0s
    => CACHED [currency-converter-dev-server runtime 1/8] RUN apt-get update; apt-get install curl -y                              0.0s
    => CACHED [currency-converter-dev-server runtime 2/8] RUN groupadd -r appgrp                                                   0.0s
    => CACHED [currency-converter-dev-server runtime 3/8] RUN useradd -r -m appusr                                                 0.0s
    => CACHED [currency-converter-dev-server runtime 4/8] RUN usermod -a -G appgrp appusr                                          0.0s
    => CACHED [currency-converter-dev-server runtime 5/8] WORKDIR /app/frontend                                                    0.0s
    => CACHED [currency-converter-dev-server runtime 6/8] RUN chown appusr:appgrp /app/frontend                                    0.0s
    => CACHED [currency-converter-dev-server node-deps 1/2] COPY frontend/package.json .                                           0.0s
    => CACHED [currency-converter-dev-server node-deps 2/2] RUN npm install                                                        0.0s
    => CACHED [currency-converter-dev-server runtime 7/8] COPY --chown=appusr:appgrp --from=node-deps /node_modules ./node_module  0.0s
    => CACHED [currency-converter-dev-server runtime 8/8] COPY --chown=appusr:appgrp ./frontend ./                                 0.0s
    => CACHED [currency-converter-prod-server build-stage 2/7] WORKDIR /app                                                        0.0s
    => CACHED [currency-converter-prod-server build-stage 3/7] COPY frontend/package*.json /app                                    0.0s
    => CACHED [currency-converter-prod-server build-stage 4/7] RUN npm install                                                     0.0s
    => CACHED [currency-converter-prod-server build-stage 5/7] COPY ./frontend/public/ /app/public                                 0.0s
    => CACHED [currency-converter-prod-server build-stage 6/7] COPY ./frontend/src/ /app/src                                       0.0s
    => CACHED [currency-converter-prod-server build-stage 7/7] RUN npm run build                                                   0.0s
    => CACHED [currency-converter-prod-server stage-1 2/5] COPY --from=build-stage /app/build/ /usr/share/nginx/html               0.0s
    => CACHED [currency-converter-prod-server stage-1 3/5] COPY ./nginx.conf.template /etc/nginx/conf.d/                           0.0s
    => CACHED [currency-converter-prod-server stage-1 4/5] COPY ./start_nginx.sh /docker-entrypoint.d/                             0.0s
    => CACHED [currency-converter-prod-server stage-1 5/5] RUN chmod +x /docker-entrypoint.d/start_nginx.sh                        0.0s

    Use 'docker scan' to run Snyk tests against images to find vulnerabilities and learn how to fix them
    ▶ Setting up configuration...
    ▶ Starting up Kubernetes cluster in minikube...

    ▶ Setting up services...
    ✅ Setup complete!

    ▶ Exposing nginx-prod-server-svc service for deployment...
    ✅ Access the nginx-prod-server-svc on http://localhost:3003

    Forwarding from 0.0.0.0:3003 -> 80

Without Building Images
+++++++++++++++++++++++

If the images are already built, the ``k8s.ps1`` script can be run directly
without the ``-build`` switch.

If the shell environment was already set before, the script will not attempt to set
it up again in subsequent runs in the same shell session.

.. code-block::

    currency-converter-api> .\k8s.ps1
    ▶ Setting up configuration...
    ▶ Starting up Kubernetes cluster in minikube...

    ▶ Setting up services...
    ✅ Setup complete!

    ▶ Exposing nginx-prod-server-svc service for deployment...
    ✅ Access the nginx-prod-server-svc on http://localhost:3003

    Forwarding from 0.0.0.0:3003 -> 80

Use Ctrl+c to stop the forwarding.

React Development Server
------------------------

To use React's built in development server to expose its UI use the ``-dev`` switch.
This can be used in combination with the ``-build`` switch to build the images before
exposing the service.

.. code-block::

    currency-converter-api> .\k8s.ps1 -dev
    ▶ Setting up configuration...
    ▶ Starting up Kubernetes cluster in minikube...

    ▶ Setting up services...
    ✅ Setup complete!

    ▶ Exposing react-dev-server-svc service for deployment...
    ✅ Access the react-dev-server-svc on http://localhost:3002

    Forwarding from 0.0.0.0:3002 -> 3002

Use Ctrl+c to stop the forwarding.

Delete the Kubernetes Cluster
-----------------------------

The previous steps only shut down the forwarding of traffic to `localhost`.

To shutdown and delete the Kubernetes cluster use the following.

.. code-block::

    currency-converter-api> .\k8s.ps1 -delete
    ▶ Deleting deployments...
    ▶ Waiting for pods to terminate...
    ✅ Pods terminated!

    ▶ Deleting configuration...
    ✅ Configuration deleted!
