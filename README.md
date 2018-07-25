CycleCloud Kafka Sample Cluster
===================================

The CycleCloud Kafka sample demonstrates configuring and launching a basic
Apache Kafka ( https://kafka.apache.org/ ) cluster from the CycleCloud
GUI.

This example implements a simple Kafka cluster with running on the same nodes as
its Zookeeper ensemble.

In general, a Kafka application will consist of a Kafka Cluster and one or more
Kafka Client Applications connecting from other clusters.

@see: [ https://kafka.apache.org/documentation.html#introduction ]

The cluster uses the `kafka-cookbook` from the Chef Supermarket and available on
github.

@see: [ https://github.com/mthssdrbrg/kafka-cookbook ]



Pre-Requisites
--------------

This sample requires the following:

  1. CycleCloud must be installed and running.

     a. If this is not the case, see the CycleCloud QuickStart Guide for
        assistance.

  2. The CycleCloud CLI must be installed and configured for use.

  3. You must have access to log in to CycleCloud.

  4. You must have access to upload data and launch instances in your chosen
     Cloud Provider account.

  5. You must have access to a configured CycleCloud "Locker" for Project Storage
     (Cluster-Init and Chef).

  6. Optional: To use the `cyclecloud project upload <locker>` command, you must
     have a Pogo configuration file set up with write-access to your locker.

     a. You may use your preferred tool to interact with your storage "Locker"
        instead.


Usage
=====

A. Configuring the Project
--------------------------

The first step is to configure the project for use with your storage locker:

  1. Open a terminal session with the CycleCloud CLI enabled.

  2. Switch to the Kafka sample directory.

  3. Run ``cyclecloud project add_target my_locker`` (assuming the locker is named "my_locker").
     The locker name will generally be the same as the cloud provider you created when configuring
     CycleCloud. The expected output looks like this:::

       $ cyclecloud project add_target my_locker
       Name: kafka
       Version: 1.0.0
       Targets:
          my_locker: {'default': 'true', 'is_locker': 'true'}

     NOTE: You may call add_target as many times as needed to add additional target lockers.

       
B. Deploying the Project
------------------------

To upload the project (including any local changes) to your target locker, run the
`cyclecloud project upload` command from the project directory.  The expected output looks like
this:::

    $ cyclecloud project upload
    Sync completed!

*IMPORTANT*

For the upload to succeed, you must have a valid Pogo configuration for your target Locker.


C. Importing the Cluster Template
---------------------------------

To import the cluster:

  1. Open a terminal session with the CycleCloud CLI enabled.

  2. Switch to the Kafka sample directory.

  3. Run ``cyclecloud import_template kafka -f ./templates/kafka.txt``.  The
     expected output looks like this:::

       $ cyclecloud import_template kafka -f ./kafka.txt
       Importing template kafka....
       ----------------------
       Kafka : *template*
       ----------------------
       Keypair: $keypair
       Cluster nodes:
           proxy: off
       Total nodes: 1


D. Creating a Kafka Cluster
-------------------------------

  1. Log in to your CycleCloud from your browser.

  2. Click the **"Clusters"** to navigate to the CycleCloud "Clusters" page, if
     you are not already there.

  3. Click the **"+"** button in the "Clusters" frame to create a new cluster.

  4. In the cluster creation page, click on the **Kafka** cluster icon.

  5. At a minimum, select the Cloud Provider Credentials to use and enter a Name
     for the cluster.

  6. Click the **"Start"** button.


E. Starting and Stopping the Kafka Cluster
----------------------------------------------

  1. Select the newly created Kafka cluster from the **Clusters**
     frame on the CycleCloud "Clusters" page

  2. To start the cluster, click the **Start** link in the cluster status
     frame.
     
  3. Later, to stop a started cluster, click the **Terminate** link in the
     cluster status frame.
     
F. Testing the Kafka Cluster
----------------------------------------------
  

  1. Start the cluster and log in to ``broker-1``.  
::

    $ cyclecloud connect broker-1
    [cyclecloud@ip-10-142-234-201 ~]$ sudo su - kafkauser
    -bash-4.1$ cd /opt/kafka
    -bash-4.1$ bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic test
    -bash-4.1$ bin/kafka-topics.sh --describe --zookeeper localhost:2181 --topic test
    -bash-4.1$ bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 3 --partitions 1 --topic my-replicated-topic
    -bash-4.1$ bin/kafka-topics.sh --describe --zookeeper localhost:2181 --topic my-replicated-topic
    -bash-4.1$ bin/kafka-topics.sh --list --zookeeper localhost:2181
    -bash-4.1$ bin/kafka-console-producer.sh --broker-list localhost:9092 --topic my-replicated-topic
    test
    test2
    test3
    ...
    ^C
    -bash-4.1$ bin/kafka-console-consumer.sh --zookeeper localhost:2181 --from-beginning --topic my-replicated-topic
    test
    test2
    test3
    ^C


Contributing
============

This project welcomes contributions and suggestions.  Most contributions require you to agree to a
Contributor License Agreement (CLA) declaring that you have the right to, and actually do, grant us
the rights to use your contribution. For details, visit https://cla.microsoft.com.

When you submit a pull request, a CLA-bot will automatically determine whether you need to provide
a CLA and decorate the PR appropriately (e.g., label, comment). Simply follow the instructions
provided by the bot. You will only need to do this once across all repos using our CLA.

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or
contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.


