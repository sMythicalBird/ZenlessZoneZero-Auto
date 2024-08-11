# coding: utf-8
from PySide6.QtCore import QObject, Signal


class SignalBus(QObject):
    """ Signal bus """

    checkUpdateSig = Signal()
    micaEnableChanged = Signal(bool)


signalBus = SignalBus()