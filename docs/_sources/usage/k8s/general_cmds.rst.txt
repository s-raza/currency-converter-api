Kubernetes General Commands
===========================

This guide is generic and can be followed for most OS's to setup the various tools needed
to run a Kubernetes cluster locally for testing purposes.

.. _general-minikube-installation:

Minikube Installation
---------------------

Install Minikube by following the official Minikube
`Getting Started <https://minikube.sigs.k8s.io/docs/start/>`_ guide for your OS.

Starting Minikube
-----------------

Ensure that Docker is running on your OS before starting Minikube using the below command

.. code-block:: text

    > minikube start
    😄  minikube v1.28.0 on Microsoft Windows 10 Pro 10.0.19044 Build 19044
        ▪ MINIKUBE_ACTIVE_DOCKERD=minikube
    ✨  Automatically selected the docker driver. Other choices: virtualbox, ssh
    📌  Using Docker Desktop driver with root privileges
    👍  Starting control plane node minikube in cluster minikube
    🚜  Pulling base image ...
    🔥  Creating docker container (CPUs=2, Memory=4000MB) ...
    🐳  Preparing Kubernetes v1.25.3 on Docker 20.10.20 ...
        ▪ Generating certificates and keys ...
        ▪ Booting up control plane ...
        ▪ Configuring RBAC rules ...
    🔎  Verifying Kubernetes components...
        ▪ Using image gcr.io/k8s-minikube/storage-provisioner:v5
    🌟  Enabled addons: storage-provisioner, default-storageclass
    🏄  Done! kubectl is now configured to use "minikube" cluster and "default" namespace by default

.. _general-install-kubectl:

Install kubectl
---------------

Install `kubectl` by following the official documentation for your OS
`here <https://kubernetes.io/docs/tasks/tools/>`_

Before proceeding to execute any of the following `kubectl` commands ensure that
they are executed from the root directory of the project.

For example:

.. code-block:: bash

    > cd currency-converter-api

Setup environment for kubectl commands
--------------------------------------

Before we can interact with the Kubernetes cluster running inside minikube we need
to point the shell to Minikube's Docker daemon.

The command to do this is the same for all OS's, except for the name of the shell,
which is shell specific.

.. code-block:: bash

    currency-converter-api> minikube docker-env --shell <name of the shell>

The available options for the shell names are ``fish, cmd, powershell, tcsh, bash, zsh``.
By default the shell name is auto-detected by the ``minikube docker-env`` command.

For Example if we run the below command in Powershell, it provides us with the
instructions for how to setup it up to interact with the Kubernetes cluster running
in Minikube via the `kubectl <https://kubernetes.io/docs/tasks/tools/>`_ command for
Powershell.

.. code-block:: bash

    currency-converter-api> minikube docker-env
    $Env:DOCKER_TLS_VERIFY = "1"
    $Env:DOCKER_HOST = "tcp://127.0.0.1:5949"
    $Env:DOCKER_CERT_PATH = "C:\Users\User\.minikube\certs"
    $Env:MINIKUBE_ACTIVE_DOCKERD = "minikube"
    # To point your shell to minikube's docker-daemon, run:
    # & minikube -p minikube docker-env --shell powershell | Invoke-Expression

Finally we can run the command given to us by the `minikube docker-env` command to setup
our shell to make it ready to execute the `kubectl` command directly on the Kubernetes
cluster running inside Minikube.

Build Docker Images
-------------------

We need to build the docker images before we can use them in a Kubernetes cluster.

The below command builds the images on the minikube node that is running within the
Docker environment in the OS. This is possible because our shell is pointed to the
Minikube's `docker-daemon` as a result of the previous step.

.. code-block:: bash

    currency-converter-api> docker compose build

Setup Configuration
-------------------

This is to read configuration parameters from the `.env` file in root directory of
the project and define them as a Kubernetes secret named as `currency-app-config`.
This is then referred in the Kubernetes manifest files to define environment
variables in the Pods.

Before running this ensure to copy the file `.env-template` to `.env` in the same directory.

.. code-block:: bash

    currency-converter-api> kubectl create secret generic currency-app-config --from-env-file=./.env
    secret/currency-app-config created

Start Kubernetes Cluster
------------------------

Create the containers and pods in the Kubernetes cluster

.. code-block:: text

    currency-converter-api> kubectl apply -f .\kubernetes
    deployment.apps/api-server created
    service/api-server-svc created
    deployment.apps/db-server created
    service/db-server-svc created
    deployment.apps/react-dev-server created
    service/react-dev-server-svc created
    deployment.apps/nginx-prod-server created
    service/nginx-prod-server-svc created
    deployment.apps/redis-server created
    service/redis-server-svc created
    deployment.apps/updater-server created

Verify that the pods were created

.. code-block:: bash

    currency-converter-api> kubectl get pods
    NAME                                 READY   STATUS    RESTARTS   AGE
    api-server-6f4c477dbd-2dhgw          1/1     Running   0          64s
    db-server-64845b6ddf-5hrfz           1/1     Running   0          64s
    nginx-prod-server-55b988b76c-4kzt8   1/1     Running   0          64s
    react-dev-server-8bb66566-kpn5s      1/1     Running   0          64s
    redis-server-6bb5466dcf-zr7rm        1/1     Running   0          64s
    updater-server-c5dc7c5fc-sbcrb       1/1     Running   0          63s

Forward Ports
-------------

After starting the Kubernetes cluster we need to expose its entry point along with
forwarding the port on which the React UI is running.

It may take a while before the API backend starts up, as it waits for the MySQL database
container to become functional before serving its end points.

The React UI can then be accessed on either ``http://localhost:3003`` or ``http://localhost:3002``
for NGINX and React development server respectively.

NGINX Server
++++++++++++

Expose the NGINX server that serves a production build of the React UI.

.. code-block:: bash

    currency-converter-api> kubectl port-forward service/nginx-prod-server-svc 3003:3003 --address 0.0.0.0
    Forwarding from 0.0.0.0:3003 -> 80

React Development Server
++++++++++++++++++++++++

Expose React's built-in Webpack development server.

.. code-block:: bash

    > kubectl port-forward service/react-dev-server-svc 3002:3002 --address 0.0.0.0
    Forwarding from 0.0.0.0:3002 -> 3002

Use Ctrl+c to stop the forwarding.

Delete the Kubernetes Cluster
-----------------------------

The previous step only shuts down the forwarding of traffic to `localhost`.

Use the following command to shutdown and delete the Kubernetes cluster.

.. code-block:: text

    currency-converter-api> kubectl delete -f .\kubernetes
    deployment.apps "api-server" deleted
    service "api-server-svc" deleted
    deployment.apps "db-server" deleted
    service "db-server-svc" deleted
    deployment.apps "react-dev-server" deleted
    service "react-dev-server-svc" deleted
    deployment.apps "nginx-prod-server" deleted
    service "nginx-prod-server-svc" deleted
    deployment.apps "redis-server" deleted
    service "redis-server-svc" deleted
    deployment.apps "updater-server" deleted

Verify that all the Pods were removed.

.. code-block:: text

    currency-converter-api> kubectl get pods
    No resources found in default namespace.
