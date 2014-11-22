from entities.database_entity import DatabaseEntity
from clients.default_bitcoin import DefaultBitcoin
from clients.default_counterparty import DefaultCounterparty


class Distribution(DatabaseEntity):
    collection_name = 'distributions'
    bitcoin = None
    counterparty = None

    # statuses for a distribution
    STATUS_NEW = 'new'
    STATUS_INPUT_VERIFIED = 'input_verified'
    STATUS_READY_TO_DISTRIBUTE = 'ready_to_distribute'
    STATUS_ATTEMPTING_DISTRIBUTE = 'attempting_distribute'
    STATUS_DISTRIBUTED = 'distributed'
    STATUS_VERIFIED = 'verified'  # worked, but not reported
    STATUS_COMPLETE = 'complete'  # reported and completely done
    STATUS_ERROR = 'error'  # bad, will be reported later

    def __init__(self, *args, **kwargs):  # entity
        super(Distribution, self).__init__(*args, **kwargs)
        if not self.__class__.bitcoin:
            self.__class__.bitcoin = DefaultBitcoin()

        if not self.__class__.counterparty:
            self.__class__.counterparty = DefaultCounterparty()

    @classmethod
    def query_new(cls):
        return cls().query({"$or": [
            {"status": cls.STATUS_NEW},
            {"status": {"$exists": False}}
        ]})

    @classmethod
    def query_ready_to_distribute(cls):
        return cls().query({"status": cls.STATUS_READY_TO_DISTRIBUTE})

    @classmethod
    def query_distributed(cls):
        return cls().query({"status": cls.STATUS_DISTRIBUTED})

    @classmethod
    def query_verified(cls):
        return cls().query({"status": cls.STATUS_VERIFIED})

    @classmethod
    def query_complete(cls):
        return cls().query({"status": cls.STATUS_COMPLETE})

    @classmethod
    def query_error(cls):
        return cls().query({"status": cls.STATUS_ERROR})

    def validate(self):
        valid = True

        # TODO: better check the strucure of this array
        if not self.from_addresses:
            # FIXME: check if this can be used as the input array for expected
            #   amounts
            # all must pass to count as valid
            # [{ currency: 'xcp', asset: 'LTBCOIN', address: 'abc123' }]
            print("Distribution requires a from_addresses array")
            valid = False
        # TODO: better check the strucure of this array
        elif not self.to_addresses:
            print("Distribution requires a to_addresses array")
            # [{ currency: 'btc', address: 'efg456' }]
            # {"1GcvsUsfvSqL3eGZBpouL6PigWmRkg1EpL":20769431000000,
            # "1Ja7bpS2mSHAkFnXdtX3BY6nqYsNGMUqhD":1341807000000,
            # "1EAXmBkW5pnnb2Th7wYMy3qNQHLQ4Dem1K":1006354999999,
            # "18b5cbhhEaQdoLZ7QwS8ang38omBBXBFYk":1006354999999,
            #"1XsjpMYcQf8PkX3qqHpuEQSJhxzGFiyQ3":13513884000000}
            valid = False
        elif not self.secret:
            print("Distribution must have a secret generated")
            valid = False

        if not valid:
            print("*** NOT VALID ***")

        return valid

    """
    TODO: BEFORE DISTRIBUTION EXISTS, DURING GENERATION, WE MUST:
    INFORMATION FROM CUSTOMER
    - ASSET and then WHO+AMOUNT
    OR
    - ASSET, AMOUNT, WHO + WHAT PERCENT

    GENERATE:
    - $address = $btc->getaccountaddress($random_account)
    - SAVE BOTH OF THESE VALUES, AS WELL AS A SECRET

    TODO: FOR XCP, VERIFY THE FOLLOWING
    - GET ALL BALANCES FOR ADDRESS: $balances =
        $xcp->get_balances(array('filters'=> array(
            'field' => 'address',
            'op' => '==',
            'value' => $row['address'])));


    TODO: IN THIS FUNCTION, WE WILL ENSURE THAT THE BALANCE IS ENOUGH
    BALANCE EXPECTED:
        SERVICE_FEE + (NUMBER_OF_TO_ADDRESSES * (FEE_AMOUNT + (2 * DUST)))
        $btc->getbalance

    XCP ASSET QUANTITY TOTAL:
        verify that the amount that is trying to be shared is <=
        the total supply of the asset
    XCP BALANCE EXPECTED:
        the SUM of all XCP balances for the "address" with that
        "asset" is >= the amount expected
    """
    def verify_input_funds_exist(self):
        for record in self.from_addresses:
            if record["currency"] == "BTC":
                if not self.verify_btc_funds(record):
                    return False

            elif record["currency"] == "XCP":
                if not self.verify_xcp_funds(record):
                    return False
            else:
                message = "'{}' currency verification not yet " \
                          "implemented".format(record["currency"])
                raise Exception(message)

        return True

    def verify_btc_funds(self, record):
        bitcoin = self.__class__.bitcoin
        balance = bitcoin.get_balance_by_address(record["address"])

        if balance < record["amount"]:
            print("{} not verified.. Balance {} < {}".format(
                record["address"],
                balance,
                record["amount"]
            ))
            return False
        return True

    def verify_xcp_funds(self, record):
        print("ATTEMPTING TO VERIFY XCP")
        counterparty = self.__class__.counterparty
        asset = counterparty.get_asset_info(record["asset"])

        if not asset:
            raise Exception(
                "XCP asset '{}' could not be found".format(record["asset"])
            )

        total_supply = asset["supply"]
        if total_supply < record["amount"]:
            message = "XCP asset '{}' does not have enough supply".format(
                record["asset"]
            )
            raise Exception(message)

        balance = counterparty.get_balance_by_address(record["address"])

        if balance < record["amount"]:
            print("{} not verified.. Balance {} < {}".format(
                record["address"],
                balance,
                record["amount"]
            ))
            return False

        return True

    def verify_distributed(self):
        bitcoin = self.__class__.bitcoin

        for transaction in self.to_addresses:
            # don't double-verify, waste of time
            if transaction['status'] == self.STATUS_VERIFIED:
                continue

            if transaction['currency'] == 'xcp':
                tx = bitcoin.get_transaction(transaction['xcp_tx_hash'])
                if not tx or tx.confirmations == 0:
                    return False

            if transaction['currency'] == 'btc':
                tx = bitcoin.get_transaction(transaction['btc_tx_hash'])
                if not tx or tx.confirmations == 0:
                    return False

            transaction['status'] = self.STATUS_VERIFIED
            self.save()

        return True

    def set_ready_to_distribute(self):
        self.set_status(self.STATUS_READY_TO_DISTRIBUTE)

    def set_complete(self):
        self.set_status(self.STATUS_COMPLETE)

    def set_status(self, status):
        self.status = status
        self.save()

    def set_error(self, message=None):
        self.error = message
        self.set_status(self.STATUS_ERROR)
        self.save()

    def distribute(self):
        for transaction in self.to_addresses:

            # do not de-distribute
            # TODO: check if this transaction has already been sent
            if 'status' in transaction and \
                    transaction['status'] == self.STATUS_DISTRIBUTED:
                continue

            if transaction['currency'] == 'xcp':
                if not self.distribute_xcp_transaction(transaction):
                    self.save()
                    return False
            else:
                raise Exception("'{}' currency transaction distribution not "
                                "implemented".format(transaction['currency']))

            # update transaction to be successfully distibuted
            transaction["status"] = self.STATUS_DISTRIBUTED
            self.save()

        return True

    def raise_xcp_transaction_exception(self, transaction, message):
        raise Exception("XCP {}->{} ({} {}): {}".format(
            transaction["from_address"],
            transaction["to_address"],
            transaction["amount"],
            transaction["asset"],
            message
        ))

    # TODO: may need batch logic here, or elsewhere
    def distribute_xcp_transaction(self, transaction):
        # validate the address
        # FIXME: see if a python library can do this better
        if not self.__class__.bitcoin.validate_address(transaction['to_address']):
            self.raise_xcp_transaction_exception(transaction, "Unable to validate to_address")

        # FIXME: if this fails, could already be unlocked
        # FIXME: try to reduce the amount of locks/unlocks API calls.. perhaps
        #        handle the unlock/lock for one batch of these
        try:
            self.__class__.bitcoin.unlock_wallet()
        except Exception:
            self.__class__.bitcoin.lock_wallet()
            self.__class__.bitcoin.unlock_wallet()

        # Create send.
        send_params = {
            'source': transaction["from_address"],
            'destination': transaction["to_address"],
            'asset': transaction["asset"],
            'quantity': int(transaction["amount"]),
            'fee': int(transaction["miner_fee"]),
            'allow_unconfirmed_inputs': True,
            'regular_dust_size': int(transaction["dust_size"]),
            'multisig_dust_size': int(transaction["dust_size"])
        }

        unsigned_tx_hex = self.__class__.counterparty.create_send(send_params)

        if not unsigned_tx_hex:
            self.raise_xcp_transaction_exception(transaction, "Unable to create_send")

        signed_tx_hex = self.__class__.counteraprty.sign_transaction(unsigned_tx_hex)

        if not signed_tx_hex:
            self.raise_xcp_transaction_exception(transaction, "Unable to sign_tx")

        tx_hash = self.__class__.counterparty.broadcast_transaction(signed_tx_hex)

        if not tx_hash:
            self.raise_xcp_transaction_exception(transaction, "Unable to broadcast_tx")

        self.__class__.bitcoin.lock_wallet()

        transaction['xcp_tx_hash'] = tx_hash

        return True

    def set_distributed(self):
        self.set_status(self.STATUS_DISTRIBUTED)

    def set_verified(self):
        self.set_status(self.STATUS_VERIFIED)
