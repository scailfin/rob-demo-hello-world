===============================================
Reproducible Open Benchmarks - Hello World Demo
===============================================

.. image:: https://img.shields.io/badge/License-MIT-yellow.svg
   :target: https://github.com/scailfin/benchmark-templates/blob/master/LICENSE



About
=====

The **Hello World Benchmark Demo** is part of the *Reproducible Open Benchmarks for Data Analysis Platform (ROB)*. The aim of this demo is to show the basic features of the benchmark engine and the command line interface.

The source code and input files for the demo are included in this repository. The example is adopted from the `REANA Hello World Demo <https://github.com/reanahub/reana-demo-helloworld>`_. The workflow has a single step that takes a text file with person names as input, together with a greeting phrase, and a sleep time. For each name in the input file a greeting will be written to an output file that is the concatenation of the greeting phrase and the name. For the purpose of this demo the result file is then analyzed to compute a score for every workflow run. Analysis computes the number of distinct 3-grams in the output file. The overall score is the number of 3-grams divided by the number of lines in the output file. The goal is to achieve a high score.




Getting Started
===============

The demo requires an instance of the `ROB Web Service <https://github.com/scailfin/rob-webapi-flask/blob/master/README.rst>`_ and the `ROB Command Line Interface <https://github.com/scailfin/rob-client/blob/master/README.rst>`_. The following instructions can be used to setup the environment. The shown commands assume that the setup directory is ``~/projects/rob`` and that a `virtual environment <https://virtualenv.pypa.io/en/stable/>`_ is used:

.. code-block:: bash

    # -- Create the project directory and the virtual environment

    mkdir ~/projects/rob
    cd ~/projects/rob
    virtualenv ~/.venv/rob
    source ~/.venv/rob/bin/activate

    # -- Install the ROB core library

    git clone https://github.com/scailfin/rob-core.git
    cd rob-core/
    pip install -e .
    cd ..

    # --  Install anc configure Web service

    git clone https://github.com/scailfin/rob-webapi-flask.git
    cd rob-webapi-flask/
    pip install -e .
    export FLASK_APP=robflask.api
    export FLASK_ENV=development
    export ROB_API_DIR=~/projects/rob/.rob
    export ROB_ENGINE_CLASS=MultiProcessWorkflowEngine
    export ROB_ENGINE_MODULE=robcore.controller.backend.multiproc
    cd ..

    # -- Create the ROB database

    export ROB_DBMS=SQLITE3
    export SQLITE_ROB_CONNECT=~/projects/rob/.rob/db.sqlite
    robadm init

    # Install the ROB command line client
    git clone https://github.com/scailfin/rob-client.git
    cd rob-client/
    pip install -e .
    cd ..



Hello-World Benchmark
---------------------


The following commands will download the demo and register it as a new benchmark with the local ROB Web Service:

.. code-block:: bash

    cd ~/projects/rob
    git clone https://github.com/scailfin/rob-demo-hello-world.git
    robadm benchmarks create -n "Hello World" \
        -d "Simple Hello World Demo" \
        -i rob-demo-hello-world/instructions.txt \
        -s rob-demo-hello-world/template/


Start the Web Service:

.. code-block:: bash

    flask run


Use a separate terminal to interact with the Web Service:

.. code-block:: bash

    # -- Register a new user and login

    rob register -u myuser -p mypwd
    eval $(rob login -u myuser -p mypwd)

    # -- List benchmarks
    rob benchmarks list
