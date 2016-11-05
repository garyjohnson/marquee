import PyQt5.Qt as qt


class MarqueeScreen(qt.QQuickItem):

    url_changed = qt.pyqtSignal()

    def __init__(self, *args, **kwargs):
        super(MarqueeScreen, self).__init__(*args, **kwargs)

    def componentComplete(self):
        super(MarqueeScreen, self).componentComplete()
