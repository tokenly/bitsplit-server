# Bitsplit Server (Alpha)

Cryptocurrency token transaction router and mass distribution system.

Host the server-side applications required for Bitsplit to run properly:
* Daemon that processes distributions
* API that allows insert/view of distributions

## Supported Protocole:
* Bitcoin (BTC)
* Counterparty (XCP)


# Installation and Setup
The Bitsplit code relies on Python 2.7.x, and can be run in a virtual
environment to ensure that it is run properly in a sandbox.  It also
relies on the servers/APIs installed "somewhere" that let you interface
with the Bitcoin, Counterparty, etc. networks.

## Requirements and Dependencies
Basic software dependencies:

* Python 2.7.x - https://www.python.org/downloads/
* MongoDB 3.0.x - https://www.mongodb.org/downloads/
    * Hardening is likely required, but has not been researched yet.
* Bitcoind - https://github.com/bitcoin/bitcoin
    * [Ubuntu Installation Guide](http://virtuedev.com/bitcoin/guide-to-compile-install-bitcoind-on-ubuntu-12-04-using-virtualbox/)
* Counterpartyd - https://github.com/CounterpartyXCP/counterpartyd
    * Requires fully up to date and indexed bitcoind node.


## Installing Bitsplit Server
1. Clone the repository.

    $ git clone git@github.com:tokenly/bitsplit-server.git

2. Move to the source code folder and create a virtual environment.

    $ cd bitsplit-server
    $ virtualenv venv

3. Turn on the virtual environment, and install the required packages.

    $ source venv/bin/activate
    $ pip install -r requirements.txt

# Starting the Services
Now that you have things installed, you need only start the two primary
services that make up the Bitsplit project:

* Start the Daemon and process distributions:

    ./bitsplitd

* Start the API and allow end-users to make requests:

    ./api


# API Endpoints
All endpoints accept and return data in JSON format.

## POST /api/v1/distribution/
Create a new distribution.

### DOCUMENTATION COMING SOON

## GET /api/v1/distribution/<hash>/
Receive the details for a specific distribution.


# Bitsplitd

Inside the /settings/ folder, there are three major files:

- bitcoin.py - bitcoind settings and credentials
- bitsplit.py - bitsplit, mongo, and mailer settings
- counterparty.py - counterpartyd settings and credentials

The majority of what you will need to change are the bitcoin and
counterparty credentials to point to the instances you wish to use; as
noted in the earlier sections.

Other sections of note, primarily in the bitsplit.py file, are:

- Mongo database settings (currently default)
- SMTP settings
- Reporting email addresses
