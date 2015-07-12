"""
TEST BITSPLIT DAEMON
"""
from bitsplit.daemon import Daemon
from unittest.mock import Mock, MagicMock
from bitsplit.models.distribution import Distribution


class TestBitsplitDaemon(object):
    """
    TEST BITSPLIT DAEMON
    """
    def __init__(self):
        self.daemon = None

    def setup(self):
        """ Create Daemon instance. """
        self.daemon = Daemon()

    def test_instantiation(self):
        """ Test that it worked at least once. """
        assert self.daemon is not None

    def test_running(self):
        """ Test that it worked at least once. """
        self.daemon.tick = Mock()
        self.daemon.run(count=1, delay=0)

        assert self.daemon.tick.called

    def test_tick(self):
        """ Test that it worked at least once. """
        self.daemon.tick()

    def test_handle_incoming(self):
        """ Test calls to the incoming distributions. """
        old_func = Distribution.find_pending_incoming_funds

        good_mock_distro = MagicMock()
        good_mock_distro.has_incoming_funds = Mock(return_value=True)

        bad_mock_distro = MagicMock()
        bad_mock_distro.has_incoming_funds = Mock(return_value=False)

        Distribution.find_pending_incoming_funds = Mock(return_value=[
            good_mock_distro,
            bad_mock_distro,
        ])

        self.daemon.handle_incoming_distributions()

        Distribution.find_pending_incoming_funds = old_func

        assert good_mock_distro.set_pending_outgoing.called
        assert not bad_mock_distro.set_pending_outgoing.called

    def test_handle_outgoing(self):
        """ Test calls to the outgoing distributions. """
        old_func = Distribution.find_pending_outgoing_funds

        good_mock_distro = MagicMock()
        good_mock_distro.has_sent_all_transactions = Mock(return_value=True)

        bad_mock_distro = MagicMock()
        bad_mock_distro.has_sent_all_transactions = Mock(return_value=False)

        Distribution.find_pending_outgoing_funds = Mock(return_value=[
            good_mock_distro,
            bad_mock_distro,
        ])

        self.daemon.handle_outgoing_distributions()

        Distribution.find_pending_outgoing_funds = old_func

        assert good_mock_distro.set_pending_verification.called
        assert not good_mock_distro.send_unsent_transactions.called

        assert not bad_mock_distro.set_pending_verification.called
        assert bad_mock_distro.send_unsent_transactions.called

    def test_handle_verification(self):
        """ Test calls to the distributions needing verification. """
        old_func = Distribution.find_pending_verification

        good_mock_distro = MagicMock()
        good_mock_distro.is_complete = Mock(return_value=True)

        bad_mock_distro = MagicMock()
        bad_mock_distro.is_complete = Mock(return_value=False)

        Distribution.find_pending_verification = Mock(return_value=[
            good_mock_distro,
            bad_mock_distro,
        ])

        self.daemon.verify_completed_distributions()

        Distribution.find_pending_verification = old_func

        assert good_mock_distro.set_verified.called
        assert not bad_mock_distro.set_verified.called
