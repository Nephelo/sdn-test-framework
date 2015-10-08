# Introduction

This project was part of a student project at Institute of Telematics at KIT.

It provides a testing framework for SDN (software defined networking) apps.
You can test ryu (http://osrg.github.io/ryu/) based apps, by simulating a network
on your computer using mininet (http://mininet.org/):

# Using the testing framework

It will start Mininet and a ryu-controller automatically and executes python unittests.

## Setup

To analyse capture packets you need the dpkt packet. Install it running pip install dpkt

## Writing

### Defining your mininet network
In the networks folder you can find two example mininet networks. sample_network_limited has the same network
topology as sample_network.py, but there are some limitations to the hosts CPU or links. See the documentation
inside the file for more information. You need to include the networks to your testcase like described in the
next section.

### Writing testclass

Write your testclass in ./test-framework folder. Your testclass should start with test_* so it can be found by the
testrunner. Your testcase should extend integration_test.IntegrationTestCase, which extends unittest.TestCase.

Best way to star ist copying and modifying test_ping.py. In the setUp-methode configure your testclass.
Set the Path to your ryu-controller (self.CONTROLLER_PATH), which is relatively to the test-framework folder.

Write your network-topology inside the networks folder. Please have a look at sample_network.py as reference.
Include the network inside your testcase and set it to self.NETWORK.

### Writing Testcase
Write your test-method (should start with test_* to be recognized as testcase).
You can use assert, als defined in python unittest packet. More methods will be available soon.

See features.md for a description of all implemented and planned features.

## Running

There are multiple ways to execute the testcases.

### Important Note: Root rights
You need to run all testcases with root rights. These are required to start mininet.
If there is a better way to to this, please let me know.

### Use the Testrunner
You can execute runner.py with root rights. This will automatically detect all testcases and executes them.

### Use python test discovery
To run all test cases you can alternatively open the console at test-framework folder.
Then run python -m unittest discover with root rights.

### Use your IDE
You also can use your preferred IDE to run the testcases. It tried PyCharm without any problem.

### Note
When running test cases make sure your working directory is ./test-framework If not there could be some errors
regarding file paths.

## Questions?
If you have problems or ideas using this testing framework, feel free to contact me uldlb@student.kit.edu

## License
This code is provided under the BSD 2-Clause License. Please refer to the LICENSE.txt file for further information.
