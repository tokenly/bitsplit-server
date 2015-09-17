"""
BITSPLIT DAEMON SETTINGS
"""
from __future__ import absolute_import
from bitsplit.drivers.bitcoin import Bitcoin

CURRENCY_DRIVERS = {
    'BTC': Bitcoin,
}

# Duration to wait before checking for Distributions if all work completed.
NO_WORK_DELAY = 10


# EVERYTHING BENEATH THESE LINES IS DEPRECATED
# AND UNDER REVIEW FOR REMOVAL
SATOSHI_MOD_OLD = pow(10, 8)
BITSPLIT_OLD_SETTINGS = {
    'database_engine': 'mongo',
    'database_url': 'mongodb://localhost:27017/bitsplit',

    # delays and batch sizes
    'btc_batch_size': 20,  # number to run
    'btc_batch_delay': 5 * 60,  # seconds
    'loop_delay': 10,  # seconds

    # costs/fees
    'bitpslit_btc_fee_per_distribution': 0.000078,
    'satoshi_mod': SATOSHI_MOD_OLD,
    'xcp_miner_fee': 0.00001,
    'xcp_dust_size': 0.000025,
    'decimals': 8,

    # mailer
    'smtp_host': '',
    'smtp_port': 587,
    'smtp_tls': False,
    'smtp_username': '',
    'smtp_password': '',

    'email_from': '"BitSplit" <noreply@bitsplit.io>',
    'email_to': '',
}

BITSPLIT_OLD_SETTINGS['xcp_fee_per_to_address'] = \
    (2 * BITSPLIT_OLD_SETTINGS['xcp_dust_size']) + \
    BITSPLIT_OLD_SETTINGS['xcp_miner_fee']

from decimal import getcontext

getcontext().prec = BITSPLIT_OLD_SETTINGS['decimals']
