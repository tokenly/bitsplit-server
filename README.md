Bitsplit Server
===============
Cryptocurrency token transaction router and mass distribution system.

Primary Components
------------------
* Daemon - The processor of Distributions and their Transactions.
* API - The creator of Distribution "jobs" to be processed.
* Client - The user-facing frontend HTML/CSS/JS to interface with API.

Supported Protocols
-------------------
* Bitcoin (BTC)
* Upcoming: Counterparty (XCP)

Supported Distribution Formats
------------------------------
* Fixed input to fixed output
* Upcoming: Variable input to percentile output


Installation and Setup
======================
The Bitsplit code relies on Python 2.7.x, and can be run in a virtual
environment to ensure that it is run properly in a sandbox.  It also
relies on the servers/APIs installed "somewhere" that let you interface
with the Bitcoin, Counterparty, etc. networks.

Requirements and Dependencies
-----------------------------
Basic software dependencies:

* Python 2.7.x - https://www.python.org/downloads/
* Bitcoind - https://github.com/bitcoin/bitcoin
    * [Ubuntu Installation Guide](http://virtuedev.com/bitcoin/guide-to-compile-install-bitcoind-on-ubuntu-12-04-using-virtualbox/)
* Counterpartyd - https://github.com/CounterpartyXCP/counterpartyd
    * Requires fully up to date and indexed bitcoind node.

Installing Bitsplit Server
--------------------------
1. Clone the repository.

    $ git clone git@github.com:tokenly/bitsplit-server.git

2. Move to the source code folder and create a virtual environment.

    $ cd bitsplit-server
    $ virtualenv venv

3. Turn on the virtual environment, and install the required packages.

    $ source venv/bin/activate
    $ pip install -r requirements.txt

Configuration
-------------
All configuration files are located in the `settings` folder with the
appropriate naming for their section being configured:

* daemon.py - Bitsplit Daemon
* api.py - Bitsplit API
* bitcoin.py - Bitcoin protocol
* counterparty.py - Counterparty protocol
* mail.py - SMTP/Mailer

Starting the Services
---------------------
Now that you have things installed, you need only start the two primary
services that make up the Bitsplit project:

* Start the Daemon and process distributions:

    ./bitsplitd

Run Unit Tests
--------------
To ensure that the code is complete and tested with 90%+ code coverage,
return to the shell:

1. Enter the virtual environment.

    $ cd ~/code/bitsplit/
    $ source venv/bin/activate

2. Run the tests.

    $ ./test

3. View the results.  An ASCII-style output should display, and HTML
   reporting of the coverage should also be generated in the `coverage`
   directory.
