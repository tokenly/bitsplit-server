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

## GET /api/v1/distribution/{hash}/
Receive the details for a specific distribution.
### DOCUMENTATION COMING SOON

# bitsplitd
Inside the /settings/ folder, there are three major files:

- bitcoin.py - Bitcoind settings and credentials
- bitsplit.py - Bitsplit, mongo, fees, constants, and mailer settings
- counterparty.py - Counterpartyd settings and credentials

The majority of what you will need to change are the bitcoin and
counterparty credentials to point to the instances you wish to use; as
noted in the earlier sections.

Other sections of note, primarily in the bitsplit.py file, are:

- Database settings (currently default)
- SMTP settings
- Reporting email addresses

# api
Inside the /settings/ folder, there will be two major files:

- bitsplit.py - As mentioned above, these are the system settings
- api.py - The host/ports for the API

The majority of what you will need, with respect to the API, will be in
the api.py file.

# Logic Flow by Protocol
# Bitcoin
## Fixed Amount Distribution
1. Create distribution via API, providing protocol, addresses, and
   quantities.
### EXAMPLE OF REQUEST JSON TO COME
2. Distribution created, providing the address to send BTC funds to,
   including any additional fees.
### EXAMPLE OF RESPONSE JSON TO COME
3. Verify that funds are provided for BTC to fund distribution.
4. Create listed distributions transactions of the funds requested to
   the addresses provided. Making use of `sendmany` call.
5. Verify that all transactions have been completed via confirmations.
6. Process any webhooks or notification steps.
7. Finalize distribution and archive.

## Variable Amount Distribution
### COMING IN THE FUTURE


# Counterparty
## Fixed Amount Distribution
1. Create distribution via API, providing protocol, asset, addresses,
   and quantities.
### EXAMPLE OF REQUEST JSON TO COME
2. Distribution created, providing the address to send BTC funds and XCP
   assets to, including any additional fees.
### EXAMPLE OF RESPONSE JSON TO COME
3. Verify that funds are provided for BTC and XCP to fund distribution.
4. Create listed distributions transactions of the asset requested to
   the addresses provided.
5. Verify that all transactions have been completed via confirmations.
6. Process any webhooks or notification steps.
7. Finalize distribution and archive.

## Variable Amount Distribution
### COMING IN THE FUTURE
