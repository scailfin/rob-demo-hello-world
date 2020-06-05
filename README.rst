===============================================
Reproducible Open Benchmarks - Hello World Demo
===============================================

.. image:: https://img.shields.io/badge/License-MIT-yellow.svg
   :target: https://github.com/scailfin/benchmark-templates/blob/master/LICENSE



About
=====

The **Hello World Benchmark Demo** is part of the `Reproducible Open Benchmarks for Data Analysis Platform (ROB) <https://github.com/scailfin/rob-core>`_. The aim of this demo is to show the basic features of the benchmark engine and the command line interface.

The source code and input files for the demo are included in this repository. The example is adopted from the `REANA Hello World Demo <https://github.com/reanahub/reana-demo-helloworld>`_. The workflow has a single step that takes a text file with person names as input, together with a greeting phrase, and a sleep time. For each name in the input file a greeting will be written to an output file that is the concatenation of the greeting phrase and the name. For the purpose of this demo the result file is then analyzed to compute a score for every workflow run. Analysis computes the number of distinct 3-grams in the output file. The overall score is the number of 3-grams divided by the number of lines in the output file. The goal is to achieve a high score.



Getting Started
===============

The demo requires an instance of the `ROB Web Service <https://github.com/scailfin/rob-webapi-flask/>`_ and the `ROB Command Line Interface <https://github.com/scailfin/rob-client/>`_. You can follow the instructions on the `Flask Web API - Demo Setup site <https://github.com/scailfin/rob-webapi-flask/blob/master/docs/demo-setup.rst>`_ to setup and run the Web API. The `ROB Command Line Interface <https://github.com/scailfin/rob-client/>`_ page contains information to install the client.

Use the ``robadm`` command line client from the Web API to create a new benchmark. Make sure to set the environment variables that configure the database accordingly, e.g.,:

.. code-block:: bash

    export FLOWSERV_DBMS=SQLITE3
    export SQLITE_FLOWSERV_CONNECT=./.rob/db.sqlite


If the Web API is running on your local machine with the default settings there is no need to configure additional environment variables. If the Web API is running on a different machine or port, for example, set the environment variables **ROB_API_HOST**, **ROB_API_PORT**, and **ROB_API_PATH** accordingly (see `the documentation <https://github.com/scailfin/rob-core/blob/master/docs/configuration.rst>`_ for details).



Hello-World Benchmark
---------------------

To start, you need to register a new workflow with the flowServ backend. This can be done using the ``flowserv`` command line tool. The following commands will download the demo and register it as a new workflow:

.. code-block:: bash

    git clone https://github.com/scailfin/rob-demo-hello-world.git
    flowserv workflows create -n "Hello World" \
        -d "Simple Hello World Demo" \
        -i ../instructions.txt \
        -s ./rob-demo-hello-world/template/


To confirm that everything worked as expected list the available workflows:

.. code-block:: bash

    flowserv workflows list


The output should contain at least the created benchmark. Note that the benchmark identifier will likely be different every time you register a benchmark.


.. code-block:: console

    Benchmark 1
    -----------

    ID          : 13f7f8c4
    Name        : Hello World
    Description : Simple Hello World Demo
    Instructions: This example benchmark is adopted from the REANA Hello World Demo. The workflow has a single step that takes a text file with person names as input, together with a greeting phrase, and a sleep time. For each name in the input file a greeting will be written to an output file that is the concatenation of the greeting phrase and the name. For the purpose of this demo the result file is then analyzed to compute a score for every workflow run. Analysis computes the number of distinct 3-grams in the output file. The overall score is the number of 3-grams divided by the number of lines in the output file. The goal is to achieve a high score.



Run the Benchmark
=================

You can use the ``rob`` command line tool to run a registered benchmark and inspect the run results. Below we list a sequence of ``rob`` commands to inspect and run the created benchmark. There also is a `screen recording of a more comprehensive example <https://asciinema.org/a/285152>`_ available online.


View Benchmark Information
--------------------------

We start by getting a more detailed overview about the created *Hello World* benchmark.

.. code-block:: bash

    rob benchmarks show -b 2a0f6059

The output contains the benchmark name and identifier, the short description, the instructions for benchmark participants, and a simple list of benchmark parameters.

.. code-block:: console

    Hello World (2a0f6059)

    Simple Hello World Demo

    This example benchmark is adopted from the REANA Hello World Demo. The workflow has a single step that takes a text file with person names as input, together with a greeting phrase, and a sleep time. For each name in the input file a greeting will be written to an output file that is the concatenation of the greeting phrase and the name. For the purpose of this demo the result file is then analyzed to compute a score for every workflow run. Analysis computes the number of distinct 3-grams in the output file. The overall score is the number of 3-grams divided by the number of lines in the output file. The goal is to achieve a high score.

    Parameters:
      Names File (file)
      Sleep for (sec.) (decimal)
      Greeting (string)


We can also print the raw JSON object for a benchmark that is returned by the API. The `full specification of the API <https://raw.githubusercontent.com/scailfin/rob-core/master/dev/resources/api/v1/rob.yaml>`_ as an `OpenAPI Spec <https://www.openapis.org/>`_ document. The API specification can for example be viewed using the `Swagger UI <https://swagger.io/tools/swagger-ui/>`_.

.. code-block:: bash

    rob --raw benchmarks show -b 2a0f6059


The resulting JSON object for the *Hello World* benchmark is:

.. code-block:: json

    {
        "description": "Simple Hello World Demo",
        "id": "2a0f6059",
        "instructions": "This example benchmark is adopted from the REANA Hello World Demo. The workflow has a single step that takes a text file with person names as input, together with a greeting phrase, and a sleep time. For each name in the input file a greeting will be written to an output file that is the concatenation of the greeting phrase and the name. For the purpose of this demo the result file is then analyzed to compute a score for every workflow run. Analysis computes the number of distinct 3-grams in the output file. The overall score is the number of 3-grams divided by the number of lines in the output file. The goal is to achieve a high score.",
        "links": [
            {
                "href": "http://localhost:5000/rob/api/v1/benchmarks/2a0f6059",
                "rel": "self"
            },
            {
                "href": "http://localhost:5000/rob/api/v1/benchmarks/2a0f6059/leaderboard",
                "rel": "leaderboard"
            },
            {
                "href": "http://localhost:5000/rob/api/v1/benchmarks/2a0f6059/submissions",
                "rel": "submissions:create"
            }
        ],
        "name": "Hello World",
        "parameters": [
            {
                "as": "data/names.txt",
                "datatype": "file",
                "description": "Names File",
                "id": "names",
                "index": 0,
                "name": "Names File",
                "required": true
            },
            {
                "datatype": "decimal",
                "defaultValue": 10,
                "description": "Sleep for (sec.)",
                "id": "sleeptime",
                "index": 0,
                "name": "Sleep for (sec.)",
                "required": true
            },
            {
                "datatype": "string",
                "defaultValue": "Hello",
                "description": "Greeting",
                "id": "greeting",
                "index": 0,
                "name": "Greeting",
                "required": true
            }
        ]
    }


We can avoid having to include the unique benchmark identifier in ``rob`` commands by setting the environment variables **ROB_BENCHMARK**.


.. code-block:: bash

    export ROB_BENCHMARK=2a0f6059


We can now view benchmark information by simply typing ``rob benchmarks show``.


Benchmark Participants
----------------------

Before participating in a benchmark users need to register with ROB.

.. code-block:: bash

    rob register -u alice -p mypwd

Note that if you omit the password at reistration (and login) the system will prompt for it. After registering a user has to login to obtain an access token.


.. code-block:: bash

    rob login -u alice -p mypwd


The output after a successful login will print the access token.

.. code-block:: console

    export ROB_ACCESS_TOKEN=75e385ca42cc48b1bdafcf7b939f2304


To avoid having to provide the access token as argument for every successive command, we can assign the access token to the environment variable **ROB_ACCESS_TOKEN**. For convenience the output of the ``rob login`` command already provides this assignment. Thus, we can use the following command instead to login and automatically assign the returned access token to the environment variable.

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

    Submission 'Team Alice' created with ID ea9e468a4d274458ac961624dfe06b93.


You can list all submissions the current user is a member of use the command ``rob submissions list``. To show information about a particular submission use the submission identifier ``rob submissions show -s ea9e468a4d274458ac961624dfe06b93``. The environment variable **ROB_SUBMISSION** can again be used to define the default submission.


.. code-block:: bash

    export ROB_SUBMISSION=ea9e468a4d274458ac961624dfe06b93
    rob submissions show


At this point the output of the command will only contain very basic information about the submission.


.. code-block:: console

    ID      : ea9e468a4d274458ac961624dfe06b93
    Name    : Team Alice
    Members : alice


Benchmark Runs
--------------

Each submission can contain multiple benchmark runs. When starting a run the user has to provide arguments for all (required) benchmark parameter. For parameters of type file the user has to provide the unique identifier of a previously uploaded file. To upload files, use:

.. code-block:: bash

    rob files upload -i rob-demo-hello-world/data/names-alice.txt

When starting a run using ``rob runs start`` the system will prompt for values for all benchmark parameters.

.. code-block:: console

    Greeting (string) [default 'Hello']: Hi
    Names File (file):

    Available files
    ---------------
    a786b1ad0ba54956b9de15f437958958	names-alice.txt (2019-12-03 18:44:23)

    > a786b1ad0ba54956b9de15f437958958
    Sleep for (sec.) (decimal) [default 10]: 1
    run f48cfe379c284341a9f10c6c6cdac3dc in state RUNNING

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

    rob runs show -r a29625a9006b42e6a499fe3bbfdcd08a


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

    rob runs download -r a29625a9006b42e6a499fe3bbfdcd08a -f 9b3bd248f43e4e9ea95f7c8f4a7eac88 -o alice.txt


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


To show the best results for each benchmark submission, i.e., the benchmark leader board, use ``rob benchmarks leaders``.

.. code-block:: console

    Rank | Submission | Number of 3-grams | Number of lines |             Score
    -----|------------|-------------------|-----------------|------------------
       1 | Team Alice |               328 |              71 | 4.619718309859155
