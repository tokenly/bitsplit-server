""" Bitsplit Daemon """

from settings.bitsplit import BITSPLIT
from entities.distribution import Distribution
import time
from clients.email import Email


class BitsplitDaemon(object):
    def __init__(self):
        self.LOOP_DELAY = BITSPLIT['loop_delay']

        self.running = True
        self.run_once = False
        self.errors = []

    def run(self):
        while self.running:
            self.run_loop()
            print("Sleeping {} seconds..".format(self.LOOP_DELAY))
            time.sleep(self.LOOP_DELAY)

            if self.run_once:
                self.running = False

    def add_error(self, message):
        self.errors.append(message)

    def clear_errors(self):
        self.errors = []

    def run_loop(self):
        self.verify_distribution_structure()
        self.verify_input_funds()
        self.distribute_transactions()
        self.verify_distributions()

        self.report_errors()
        self.report_verified()

    def verify_distribution_structure(self):
        print("Verifying distributions")
        distros = Distribution.query_new()
        for distro in distros:

            if not distro.validate():
                distro.set_error("Field missing or invalid distribution structure")
                break

    def verify_input_funds(self):
        # VERIFY INPUT FUNDS
        # make all new distributions verify they have funds
        distros = Distribution.query_new()
        for distro in distros:
            if distro.verify_input_funds_exist():
                print(repr('INPUT FUNDS VERIFIED! {}'.format(str(distro._id))))
                distro.set_ready_to_distribute()

    def distribute_transactions(self):
        # DISTRIBUTE TRANSACTIONS
        # for all distributions ready to distribute, cycle through the
        # transactions and send them
        distros = Distribution.query_ready_to_distribute()
        for distro in distros:
            if distro.distribute():
                distro.set_distributed()

        # TODO: one possible outcome, as per @NR is that after
        #       spamming, no txid might come back.. in which case
        #       it is safe to assume that you are being blocked
        #       for attempting to spam, and can retry.. test for
        #       this appropriately

    def verify_distributions(self):
        distros = Distribution.query_distributed()
        for distro in distros:
            if not distro.verify_distributed():
                print(repr('Unable to verify distributed {}'.format(str(distro._id))))
                continue

            distro.set_verified()

    def report_verified(self):
        # REPORT COMPLETE AND SUCCESSFUL
        # for any transactions that failed to attempt distribution
        # email a report to an admin
        # TODO put code for email here
        email = Email(Subject='BitSplit - Verified Report')

        body = ""
        distros = Distribution.query_verified()

        for distro in distros:
            body += "Distribution {} verified<br />".format(str(distro._id))

        if len(distros):
            email.Html = body
            email.send()

        # no more anything
        for distro in distros:
            distro.set_complete()

    def report_errors(self):
        # REPORT INCOMPLETE TRANSACTIONS/DISTRIBUTIONS
        # for any transactions that failed to attempt distribution
        # email a report to an admin
        # TODO put code for email here
        email = Email(Subject='BitSplit - Error Report')
        body = ""

        distros = Distribution.query_error()
        for distro in distros:
            body += "Distribution {} ERROR<br />".format(str(distro._id))

        for error in self.errors:
            body += "ERROR: {}<br />".format(error)

        if len(self.errors):
            email.send()
            self.clear_errors()
