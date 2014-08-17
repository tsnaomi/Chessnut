"""Simple signaling framework for use in Chessnut.

Valid signals may be found (and added/removed) in the SignalBase class.

Signals have a handler and optionally a trigger. When a call to
SignalManager.dispatch is made for a given signal with a given trigger,
all handlers for that signal corresponding to that trigger are run. If
no trigger is provided, then all handlers for the given signal are run
every time it's dispatched. Signal handlers are only run once; after
running, they are unregistered.

Handlers are tuples consisting of a callable followed by arguments to be
passed to that callable.

For example: if the Pawn's 'en_passant' boolean is set, it registers for a
'start_turn' signal to unset 'en_passant' at the beginning of its players
next turn. That signal takes the form:

    signal='start_turn'
    trigger=pawn.player
    handler=(lambda: setattr(self, 'en_passant', False))

...and is interpreted as: "When the 'start_turn' signal is dispatched for the
pawn's player, set this pawn's 'en_passant' attribute to False."
"""

from chessnut_game.exceptions import InvalidSignalError


class SignalBase(object):
    """Base class for the signals module. Defines valid signals."""
    def __init__(self):
        # Define new signals here.
        self.signals = {
            'piece_moved': {},
            'space_moved_from': {},
            'space_moved_to': {},
            'start_turn': {},
        }


class SignalCollector(SignalBase):
    """Simple object that collects signals to be registered."""
    def register(self, signal, handler, trigger=None):
        """Add a signal to the signals dict."""
        try:
            self.signals[signal].setdefault(trigger, [])
            self.signals[signal][trigger].append(handler)

        except KeyError:
            raise InvalidSignalError("%s is not a valid signal." % signal)


class SignalManager(SignalBase):
    """Manages registering, updating, and triggering of signals."""
    def update(self, collection):
        """Update the signals contained in the manager with signals
        from a SignalCollector object.
        """
        for signal, updates in collection.signals.items():
            for trigger, handlers in updates:
                try:
                    self.signals[signal].setdefault(trigger, [])
                    self.signals[signal][trigger].extend(handlers)
                except KeyError:
                    raise InvalidSignalError(
                        "%s is not a valid signal." % signal
                    )

    def dispatch(self, signal, trigger):
        """Dispatch any signals with the given trigger and then update
        the contained signals with any new signals returned.
        """
        if signal not in self.signals:
            raise InvalidSignalError("%s is not a valid signal." % signal)

        new_signal_collections = []

        try:
            for handler in self.signals[signal][trigger]:
                new_signal_collections.append(handler[0](*handler[1:]))

            self.signals[signal][trigger] = []

            for collection in new_signal_collections:
                self.update(collection)

        except KeyError:
            pass
