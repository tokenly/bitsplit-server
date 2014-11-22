#BitSplit

Cryptocurrency token transaction router and mass distribution system. 

**Supported Protocols:**

* Bitcoin (BTC)
* Counterparty (XCP)

##Usage

###SERVERS

Running the daemon

    ./bitsplitd
    
Running the API server

    ./api
    
###API ENDPOINTS

All endpoints accept and return data in JSON format.

Example API URL: http://localhost:4200/api/v1/distribution/xcp

**/api/v1/distribution/{protocol}/**

* Method: POST
* Parameters:
	* to_addresses (array)
		- address
		- amount
		- asset
* Example Input: {"to_addresses": [{"address":"1LYRgNDuZfdnZKLkLeTb7UG4UQZyZGvV3w","asset":"LTBCOIN","amount":50}]}
* Response:

**[API documentation in progress]**

##Installation and Setup

###REQUIREMENTS & DEPENDENCIES

Python 3.4  
MongoDB

Run the following to install dependencies:
    
    sudo pip install -r requirements.txt

###MONGODB

- Download and install [mongodb](https://github.com/mongodb/mongo) server package
- Hardening may be needed, but this has not yet been researched.

###BITCOIND

- Download [bitcoind source code](https://github.com/bitcoin/bitcoin) and setup a node.
- [Ubuntu Installation Guide](http://virtuedev.com/bitcoin/guide-to-compile-install-bitcoind-on-ubuntu-12-04-using-virtualbox/)

###COUNTERPARTYD

- Download and run [counterpartyd](https://github.com/CounterpartyXCP/counterpartyd) (requires fully up to date and indexed bitcoind node)
- See git repository for installation instructions

###BITSPLITD

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


