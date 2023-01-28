Run Services using Kubernetes
=============================

There is an option to run the currency converter using Kubernetes.

Minikube can be used to run the kubernetes cluster locally, which requires  `installing
and intializing Minikube <https://minikube.sigs.k8s.io/docs/start/>`_ locally on
`Docker Desktop <https://www.docker.com/products/docker-desktop/>`_ for Windows or on Linux

General :doc:`kubectl commands <general_cmds>` can be used to run the kubernetes cluster on Minikube.

Alternatively a :doc:`Powershell Script <ps1_script>` for Windows systems is provided to manage the
Kubernetes cluster running in Minikube.

In both cases Minkube should be installed and initiated before using any of the above two methods.

To install Minikube for your OS
`click here <https://minikube.sigs.k8s.io/docs/start/>`_ for the official instructions

.. toctree::
    :maxdepth: 1

    general_cmds
    ps1_script
