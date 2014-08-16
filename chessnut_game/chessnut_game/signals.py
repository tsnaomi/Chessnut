"""Simple signalling framework for use in Chessnut."""
from chessnut_game.constants import Black, White


class SignalBase(object):
    """Base class for the signals module. Defines valid signals."""
    # Define new signals here.
    signals = {
        'next_turn': {
            Black: [],
            White: [],
        },
        'piece_moved': {},
        'space_moved_from': {},
        'space_moved_to': {},
    }


class SignalCollector(SignalBase):
    """Simple object that collects signals to be registered."""


class SignalManager(SignalBase):
    """Manages registering, updating, and triggering of signals."""
