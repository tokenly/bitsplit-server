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
    * [Ubuntu Installation Guide][bitcoind-ubuntu]
* Counterpartyd - https://github.com/CounterpartyXCP/counterpartyd
    * Requires fully up to date and indexed bitcoind node.


Installing Bitsplit Server
--------------------------
1. Clone the repository.
```
    $ git clone git@github.com:tokenly/bitsplit-server.git
```
2. Move to the source code folder and create a virtual environment.
```
    $ cd bitsplit-server
    $ virtualenv venv
```
3. Turn on the virtual environment, and install the required packages.
```
    $ source venv/bin/activate
    $ pip install -r requirements.txt
```

Configuration
-------------
All configuration files are located in the `settings` folder with the
appropriate naming for their section being configured:

* daemon.py - Bitsplit Daemon
* api.py - Bitsplit API
* webserver.py - Bitsplit Webserver for HTML/CSS/JS
* bitcoin.py - Bitcoin protocol
* counterparty.py - Counterparty protocol
* mail.py - SMTP/Mailer


Starting the Services
---------------------
Now that you have things installed, you need only start the two primary
services that make up the Bitsplit project:

* Start the Daemon and process Distributions:
```
   ./bitsplitd
```

* Start the API and receive Distributions:
```
    ./api
```

* Start the client-facing webserver and receive web visits:
```
    ./webserver
```

Run Unit Tests
--------------
To ensure that the code is complete and tested with 90%+ code coverage,
return to the shell:

1. Enter the virtual environment.
```
    $ cd ~/code/bitsplit/
    $ source venv/bin/activate
```

2. Run the tests.
```
    $ ./test
```
3. View the results.  An ASCII-style output should display, and HTML
   reporting of the coverage should also be generated in the `coverage`
   directory.


Creating Currency Drivers
=========================
Currency Drivers are intended to be easy to implement, as the basis for
the Bitsplit system is very generic, with specificity added in the
Drivers alone.

As such, code for a Driver should look fairly simple, understanding this
example is completely silly and only intends to convey that you can use
any basis you need to in order to make a driver:

```python
from bitsplit.driver import Driver
from some.library.you.are.using import Banana

class BananaDriver(Driver):
    def setup(self, distribution):
        """ Any extra steps to take after creation? """
        self.incoming_bananas = [1]
        self.outgoing_bananas = []

    def teardown(self):
        """ Any extra steps to take before destruction? """
        pass

    def verify_incoming(self, transaction):
        """ Verify that an incoming transaction has been received. """
        return 1 in self.incoming_bananas

    def process_outgoing(self, transaction):
        """ Process an outgoing transaction. """
        self.outgoing_bananas.append(transaction.get('amount'))
        return True

    def verify_outgoing(self, transaction):
        """ Verify an outgoing transaction was processed properly. """
        return len(self.outgoing_bananas) === 3
```

With a Distribution and its Transactions looking like the following,
with a few pieces of additional information for the Daemon to process
it, wrapped within an object using getters/setters:

```python
{
    "id": "abc123",  # hash
    "incoming": [
        {
            "currency": "btc",
            "address": "abc123",
            "amount": "1.00010000",
        }
    ],
    "outgoing": [
        {
            "currency": "btc",
            "address": "abc123",
            "amount": "0.50000000",
        },
        {
            "currency": "btc",
            "address": "xyz321",
            "amount": "0.50000000",
        },
    ],
}
```

[bitcoind-ubuntu]: http://virtuedev.com/bitcoin/guide-to-compile-install-bitcoind-on-ubuntu-12-04-using-virtualbox/
