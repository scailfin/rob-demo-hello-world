===============================================
Reproducible Open Benchmarks - Hello World Demo
===============================================

.. image:: https://img.shields.io/badge/License-MIT-yellow.svg
   :target: https://github.com/scailfin/benchmark-templates/blob/master/LICENSE



About
=====

The **Hello World Benchmark Demo** is part of the `Reproducible and Reusable Data Analysis Workflow Server (flowServ) <https://github.com/scailfin/flowserv-core>`_. The aim of this demo is to show the basic features of the benchmark engine and the command line interface.

The source code and input files for the demo are included in this repository. The example is adopted from the `REANA Hello World Demo <https://github.com/reanahub/reana-demo-helloworld>`_. The workflow has two steps: the first step takes a text file with person names as input, together with a greeting phrase, and a sleep time. For each name in the input file a greeting will be written to an output file that is the concatenation of the greeting phrase and the name. For the purpose of this demo the result file is then analyzed in the second step to compute a score for every workflow run. Analysis computes the number of distinct 3-grams in the output file. The overall score is the number of 3-grams divided by the number of lines in the output file. The goal is to achieve a high score.



Getting Started
===============

The demo requires an instance of the `Reproducible and Reusable Data Analysis Workflow Server (flowServ) <https://github.com/scailfin/flowserv-core>_`. You can install **flowServ** using the following command (note that it is recommended to installthe package within a virtual environment).


.. code-block:: bash

    pip install flowserv-core[docker]

After installing **flowServ** you need to configure the server and initialize the database. In this example we use a SQLite database. All files are stored in a subfolder of the current working directory (see `the documentation <https://github.com/scailfin/flowserv-core/blob/master/docs/configuration.rst>`_ for details on configuration parameters).

.. code-block:: bash

    export FLOWSERV_API_DIR=$PWD/.flowserv
    export FLOWSERV_DATABASE=sqlite:///$PWD/.flowserv/db.sqlite

    flowserv init



Hello-World Benchmark
---------------------

To start, you need to register a new workflow with the **flowServ** backend. This can be done using the ``flowserv`` and ``rob`` command line tools.

The following commands will download the demo and register it as a new workflow:

.. code-block:: bash

    git clone https://github.com/scailfin/rob-demo-hello-world.git
    flowserv workflows create "helloworld" \
        -n "Hello World" \
        -d "Simple Hello World Demo" \
        -k helloworld


To confirm that everything worked as expected list the available workflows:

.. code-block:: bash

    rob benchmarks list


The output should contain at least the created benchmark. Note that the benchmark identifier will likely be different every time you register a benchmark.


.. code-block:: console

    Workflow 1
    ----------
    
    ID          : helloworld
    Name        : Hello World
    Description : Simple Hello World Demo
    Instructions: This example benchmark is adopted from the REANA Hello World Demo ...
    

Configuration Options
---------------------

By default all workflow steps will be executed as separate processes using the `Python subprocess package <https://docs.python.org/3/library/subprocess.html>`_. This default behavior can be changed by providing a configuration file that defines the backend that will be used for the different environments that are defined in the workflow specification and the post-processing workflow. For `the Hello World workflow <https://github.com/scailfin/rob-demo-hello-world/blob/master/benchmark.yaml>`_ the environments are ``python:3.9`` for the main part and ``heikomueller/flowserv:0.8.0`` for the post-processing part.

If you want to run the post-processing step using Docker, for example, create a file ``workers.yaml`` with the following content:

.. code-block:: bash

    workers:
      - worker: docker
        image: heikomueller/flowserv:0.8.0


Then either change change the command that was used to register the workflow to:

.. code-block:: bash

    flowserv workflows create "helloworld" \
        -n "Hello World" \
        -d "Simple Hello World Demo" \
         -c workers.yaml \
        -k helloworld


As an alternative, worker configurations can be defined on a per-submission basis. When creating a submission use the following command instead of the one that is show below:

.. code-block:: bash

    rob submissions create -n 'Team Alice' -c worker.yaml

Note that this will only affect the main workflow steps but not the post-processing step.


Run the Benchmark
=================

You can use the ``rob`` command line tool to run a registered workflow and inspect the run results. Below we list a sequence of commands to inspect and run the created workflow. To avoid having to include the unique workflow identifier in ``rob`` commands set the environment variable **ROB_BENCHMARK**.


.. code-block:: bash

    export ROB_BENCHMARK=helloworld


We can now view benchmark information by simply typing ``rob benchmarks show``.


Benchmark Participants
----------------------

Before participating in a benchmark users need to register with ROB.

.. code-block:: bash

    rob users register -u alice -p mypwd

Note that if you omit the password at reistration (and login) the system will prompt for it. After registering a user has to login to obtain an access token.


.. code-block:: bash

    rob login -u alice -p mypwd


The output after a successful login will print the access token.

.. code-block:: console

    export FLOWSERV_ACCESS_TOKEN=...


To avoid having to provide the access token as argument for every successive command, we can assign the access token to the environment variable **FLOWSERV_ACCESS_TOKEN**. For convenience the output of the ``rob login`` command already provides this assignment. Thus, we can use the following command instead to login and automatically assign the returned access token to the environment variable.

.. code-block:: bash

    eval $(rob login -u alice -p mypwd)


Use the following command to verify that the login was successful.

.. code-block:: bash

    rob whoami


the output should be

.. code-block:: console

    Logged in as alice.


Benchmark Submissions
---------------------

Users that want to participate in a benchmark have to create a *benchmark submission*. Each user can be a member of multiple submissions. All submissions for a benchmark have to have a unique name.

.. code-block:: bash

    rob submissions create -n 'Team Alice'


The output of the command will contain the unique submission identifier. Note that these identifiers are random UUID's. The submission identifier will therefore likely be different every time you create a submission.

.. code-block:: console

    export ROB_SUBMISSION=6cc79d980f774c7a9e7161915c1891de


You can list all submissions the current user is a member of use the command ``rob submissions list``. To show information about a particular submission use the submission identifier ``rob submissions show -g 6cc79d980f774c7a9e7161915c1891de``. The environment variable **ROB_SUBMISSION** can again be used to define the default submission.


.. code-block:: bash

    export ROB_SUBMISSION=6cc79d980f774c7a9e7161915c1891de
    rob submissions show


At this point the output of the command will only contain very basic information about the submission.


.. code-block:: console

    ID      : 6cc79d980f774c7a9e7161915c1891de
    Name    : Team Alice
    Members : alice
    
    Uploaded Files
    --------------
    
    ID | Name | Created At | Size
    ---|------|------------|-----
    

Each submission can contain multiple benchmark runs. When starting a run the user has to provide arguments for all (required) benchmark parameters. For parameters of type file the user has to provide the unique identifier of a previously uploaded file.

To upload files, use:

.. code-block:: bash

    rob files upload -i rob-demo-hello-world/data/names-alice.txt

When starting a run using ``rob runs start`` the system will prompt for values for all benchmark parameters.

.. code-block:: console

    Select file identifier from uploaded files:
    
    ID                               | Name            | Created at         
    ---------------------------------|-----------------|--------------------
    1257590f80ff4349b419bb7a20e2be59 | names-alice.txt | 2021-02-25T13:09:49
    
    Names File (file) $> 1257590f80ff4349b419bb7a20e2be59
    Sleep for (sec.) (float) [default '10'] $> 0.1
    Greeting (string) [default 'Hello'] $> Hi
    
    started run 987c72293cf64e0f877557ad358f84ba is SUCCESS


To view the status of all submission runs use:

.. code-block:: bash

    rob runs list


Depending on the state of the submitted run the output will look similar to one of the two options below:

.. code-block:: console

    ID                               | Submitted at               | State
    ---------------------------------|----------------------------|--------
    a29625a9006b42e6a499fe3bbfdcd08a | 2020-06-05T17:11:22.140346 | RUNNING

    or

    ID                               | Submitted at               | State
    ---------------------------------|----------------------------|--------
    a29625a9006b42e6a499fe3bbfdcd08a | 2020-06-05T17:11:22.140346 | SUCCESS


To get information about a successful run use:

.. code-block:: bash

    rob runs show a29625a9006b42e6a499fe3bbfdcd08a


The output will show the run timestamps as well as the produced output files.

.. code-block:: console

    ID: a29625a9006b42e6a499fe3bbfdcd08a
    Started at: 2020-06-05 13:11:22
    Finished at: 2020-06-05 13:17:17
    State: SUCCESS

    Arguments:
      Greeting = Hi
      Names File = names-alice.txt (843974550dc14c0bb9c142264ee54d57)
      Sleep for (sec.) = 5.0
    
    Resources:
      results/analytics.json (12705f33e4fe4740a3607d849642f1d1)
      results/greetings.txt (9b3bd248f43e4e9ea95f7c8f4a7eac88)
    

You can download output files that were generated by a workflow run. The following example downloads the ``results/greetings.txt`` file and stores it as ``alice.txt`` in the current working directory.


.. code-block:: bash

    rob runs download file -f bde2d546a5714154b9d191d2d4fb4f17 -o alice.txt a29625a9006b42e6a499fe3bbfdcd08a


The downloaded file should look like this:

.. code-block:: console

    Hi ADRIANA
    Hi ALESSANDRO
    Hi ALYSHA
    Hi ANDRES
    Hi ANTOINETTE
    Hi ASHLEIGH
    Hi BARRINGTON
    Hi BETTY
    Hi BRENDA
    Hi CAPUCINE
    Hi CARYN
    ...


To show the best results for each benchmark submission, i.e., the benchmark leader board, use ``rob benchmarks ranking``.

.. code-block:: console

    Rank | Submission | Number of 3-grams | Number of lines |             Score
    -----|------------|-------------------|-----------------|------------------
       1 | Team Alice |               328 |              71 | 4.619718309859155
