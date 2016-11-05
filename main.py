#!/usr/bin/env python

import os
import sys
import signal
import logging

import PyQt5.Qt as qt

import marquee.widgets.marquee as marquee
import marquee.screens.marquee_screen as marquee_screen
import marquee.main_window as main_window
import marquee.services as services
import marquee.service.mqtt_service as mqtt_service


def exit_on_ctrl_c():
    signal.signal(signal.SIGINT, signal.SIG_DFL)


def main():
    exit_on_ctrl_c()

    app = qt.QApplication(sys.argv)

    qt.qmlRegisterType(marquee.Marquee, 'Widgets', 1, 0, 'Marquee')
    qt.qmlRegisterType(marquee_screen.MarqueeScreen, 'Screens', 1, 0, 'MarqueeScreen')

    window = main_window.MainWindow()
    window.showFullScreen()

    mqtt = services.get(mqtt_service.MqttService)
    mqtt.start()

    sys.exit(app.exec_())


if __name__ == '__main__':

    log_levels = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
    }
    log_level_name = os.environ.get('MQE_LOG', 'ERROR')
    logging.basicConfig(level=log_levels[log_level_name])
    logging.getLogger().setLevel(log_levels[log_level_name])
    logger = logging.getLogger(__name__)
    logger.debug('marquee log level is {}'.format(log_level_name))

    main()
