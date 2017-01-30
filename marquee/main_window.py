try:
    import ConfigParser as config
except:
    import configparser as config

import sys
from pydispatch import dispatcher
import marquee.signals as signals
import PyQt5.Qt as qt


class MainWindow(qt.QQuickView):

    rotation_changed = qt.pyqtSignal()

    def __init__(self, *args, **kwargs):
        super(qt.QQuickView, self).__init__()
        dispatcher.connect(self._on_show_window, signals.SHOW_WINDOW, sender=dispatcher.Any)
        dispatcher.connect(self._on_hide_window, signals.HIDE_WINDOW, sender=dispatcher.Any)

        self._rotation = self.get_rotation()
        self.engine().rootContext().setContextProperty('screenRotation', qt.QVariant(self.rotation))
        self.setSource(qt.QUrl('main.qml'))

        self.setHeight(self.screen().size().height())
        self.setWidth(self.screen().size().width())
        self.setResizeMode(qt.QQuickView.SizeRootObjectToView)

        surfaceFormat = qt.QSurfaceFormat()
        surfaceFormat.setAlphaBufferSize(8);
        self.setFormat(surfaceFormat);
        self.setClearBeforeRendering(True);
        self.setColor(qt.QColor(qt.Qt.transparent));

        self.visible = False
        self._refresh_window_flags()
        self._refresh_window_state()

    def _on_show_window(self):
        self.visible = True
        self._refresh_window_flags()
        self._refresh_window_state()

    def _on_hide_window(self):
        self.visible = False
        self._refresh_window_flags()
        self._refresh_window_state()

    def _refresh_window_state(self):
        window_state = qt.Qt.WindowFullScreen if self.visible else qt.Qt.WindowMinimized
        self.setWindowState(window_state)

    def _refresh_window_flags(self):
        window_type = qt.Qt.SubWindow if sys.platform == 'darwin' else qt.Qt.Tool
        window_chrome = qt.Qt.FramelessWindowHint | qt.Qt.WindowSystemMenuHint
        on_top = qt.Qt.WindowStaysOnTopHint if self.visible else 0

        self.setFlags(window_type | window_chrome | on_top | qt.Qt.WindowTransparentForInput)

    @qt.pyqtProperty(int, notify=rotation_changed)
    def rotation(self):
        return self._rotation

    @rotation.setter
    def rotation(self, value):
        self._rotation = value
        self.rotation_changed.emit()

    def get_rotation(self):
        config_parser = config.SafeConfigParser(allow_no_value=False)
        with open('marquee.cfg') as config_file:
            config_parser.readfp(config_file)
        return int(config_parser.get('general', 'rotation'))

