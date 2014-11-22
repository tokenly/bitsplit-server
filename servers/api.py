#!/usr/local/bin/python
"""
BitSplit API
"""

from flask import Flask, render_template
from flask import request

from settings.bitsplit import BITSPLIT

from entities.distribution import Distribution

from clients.default_bitcoin import DefaultBitcoin
from clients.default_counterparty import DefaultCounterparty

from errors.asset_not_found_error import AssetNotFoundError
from errors.insufficient_asset_supply_error import InsufficientAssetSupplyError

import uuid

app = Flask(__name__, static_folder="../media", template_folder="../templates")


@app.route("/api/v1/distribution/xcp/", methods=['POST'])
def api_v1_distribution():
    data = {
        'to_addresses': [],
        'from_addresses': []
    }

    amount_sums_by_asset = {}
    # Convert the CSV format to addresses
    if request.mimetype == 'text/csv':
        raw = request.data
        lines = raw.split("\n")

        data['to_addresses'] = get_to_addresses_from_csv_lines(lines)

        # TODO: Lines starting with WEBHOOK will be URLs to hit on success
        # TODO: Lines starting with EMAIL will be addresses to email on success

    # Convert the JSON format to addresses
    elif request.mimetype in ('application/json','text/json'):
        json = request.get_json(True)
        data['to_addresses'] = get_to_addresses_from_json(json)

        # TODO: Gather webhook URLs
        # TODO: Gather success email addresses

    # Must have at least one to_address (even though one would be silly)
    if len(data['to_addresses']) == 0:
        raise Exception("At least one distribution record must be provided")

    # Figure out if asset is divisible and do some logic
    for to_address in data['to_addresses']:
        asset_name = to_address['asset']
        asset = get_xcp_asset(asset_name)

        # Asset could not be found
        if not asset:
            raise AssetNotFoundError()

        # Multiply divisible assets by satoshi_mod (10^8)
        if asset['divisible']:
            to_address['amount'] *= BITSPLIT['satoshi_mod']

    # Sum the XCP needed by asset
    for to_address in data['to_addresses']:
        if not to_address['asset'] in amount_sums_by_asset:
            amount_sums_by_asset[to_address['asset']] = 0
        amount_sums_by_asset[to_address['asset']] += to_address['amount']

    # Figure out how much of the assets exist, and that there are enough to
    # cover the transactions needed
    for asset_name in amount_sums_by_asset:
        amount = amount_sums_by_asset[asset_name]
        asset = get_xcp_asset(asset_name)
        if amount > asset['supply']:
            raise InsufficientAssetSupplyError()

    # generate a wallet address
    bitcoin = DefaultBitcoin()

    account_name = get_random_xcp_account_name()
    receiving_address = bitcoin.generate_wallet(account=account_name)

    data['account'] = account_name
    data['status'] = Distribution.STATUS_NEW
    data['secret'] = uuid.uuid4().hex

    # update all to_addresses to have the from_address that was generated
    for to_address in data['to_addresses']:
        to_address['from_address'] = receiving_address

    # XCP: figure out how much of each asset needs to be deposited
    for asset_name in amount_sums_by_asset:
        amount = float(amount_sums_by_asset[asset_name])

        from_address = {}

        from_address['currency'] = 'XCP'
        from_address['address'] = receiving_address
        from_address['asset'] = asset_name
        from_address['amount'] = amount

        data['from_addresses'].append(from_address)

    # BTC: figure out how many fees need to be paid
    btc_amount = get_distribution_btc_fee(data)
    data['from_addresses'].append({
        'address': receiving_address,
        'currency': 'BTC',
        'amount': btc_amount
    })

    # throws exception on failure
    distro = Distribution(data=data)
    distro.validate()
    distro._data = {"abc": 123}
    print(distro._data)
    distro.save()

    return distro.to_json()


def get_random_xcp_account_name():
    """ Generate a random counterparty address """
    random_hash = uuid.uuid4().hex[0:6]
    account_name = BITSPLIT['xcp_account_prefix'] + random_hash
    return account_name


def get_xcp_asset(asset_name):
    """ MRU cache for CounterParty asset lookup """
    counterparty = DefaultCounterparty()
    cached_assets = {}
    if not asset_name in cached_assets:
        asset = counterparty.get_asset(asset_name)
        cached_assets[asset_name] = asset
    else:
        asset = cached_assets[asset_name]

    return cached_assets[asset_name]


def get_to_addresses_from_json(json):
    to_addresses = []
    if type(json) is not dict:
        raise Exception("JSON provided must be a list")
    if 'to_addresses' not in json:
        raise Exception('to_addresses field required')
    for obj in json['to_addresses']:
        to_address = {}
        if not 'asset' in obj:
            raise Exception("Each array object must have an 'asset'")
        to_address['asset'] = obj['asset']

        if not 'amount' in obj:
            raise Exception("Each array object must have an 'amount'")
        to_address['amount'] = float(obj['amount'])

        if not 'address' in obj:
            raise Exception("Each array object must have an 'address'")
        to_address['address'] = obj['address']

        to_address['currency'] = 'XCP'

        to_addresses.append(to_address)
    return to_addresses


def get_to_addresses_from_csv_lines(lines):
    to_addresses = []

    # format is
    # 0: asset
    # 1: amount
    # 2: address
    for line in lines:
        # skip blank lines
        if not line.strip():
            continue

        to_address = get_to_address_from_csv_line(line)
        to_addresses.append(to_address)

    return to_addresses


def get_to_address_from_csv_line(line):
    to_address = {}
    cols = line.split(',')
    if len(cols) is not 3:
        message = "CSV lines must follow 'ASSET,AMOUNT,ADDRESS' format"
        raise Exception(message)

    for index, col in enumerate(cols):
        val = col.strip()
        if index == 0:
            to_address['asset'] = val
        elif index == 1:
            to_address['amount'] = float(val)
        elif index == 2:
            to_address['address'] = val

    return to_address


def get_distribution_btc_fee(data):
    to_address_count = len(data['to_addresses'])
    btc_amount = to_address_count * BITSPLIT['xcp_fee_per_to_address']
    return btc_amount


@app.route('/')
def index():
    return render_template('index.html')


def run():
    app.run(host="0.0.0.0", port=4200, debug=True)
