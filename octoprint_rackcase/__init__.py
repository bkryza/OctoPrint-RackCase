# coding=utf-8
from __future__ import absolute_import

### (Don't forget to remove me)
# This is a basic skeleton for your plugin's __init__.py. You probably want to adjust the class name of your plugin
# as well as the plugin mixins it's subclassing from. This is really just a basic skeleton to get you started,
# defining your plugin as a template plugin, settings and asset plugin. Feel free to add or remove mixins
# as necessary.
#
# Take a look at the documentation on what other plugin mixins are available.

import octoprint.plugin
from octoprint.util import RepeatedTimer
import board
import busio
import digitalio
import adafruit_ccs811
import adafruit_bme280
from adafruit_pca9685 import PCA9685


class RackcasePlugin(
    octoprint.plugin.StartupPlugin,
    octoprint.plugin.SettingsPlugin,
    octoprint.plugin.AssetPlugin,
    octoprint.plugin.TemplatePlugin,
):
    def __init__(self):
        self._checkSensors = None
        self._ccs811_reset = digitalio.DigitalInOut(board.D18)
        self._ccs811_reset.direction = digitalio.Direction.OUTPUT
        self.init_ccs811()

        self._light_control_button = digitalio.DigitalOut(board.D18)
        self._i2c_bus = busio.I2C(board.SCL, board.SDA)
        self._ccs811 = adafruit_ccs811.CCS811(i2c_bus, address=0x5B)
        self._bme280 = adafruit_bme280.Adafruit_BME280_I2C(
            i2c_bus, address=0x76
        )
        self._pca = PCA9685(i2c_bus)
        self._pca.frequency = 60

    def init_ccs811():
        self._ccs811_reset.value = True
        time.sleep(0.1)
        self._ccs811_reset.value = False
        time.sleep(0.1)
        ccs811_reset.value = True

    def on_after_startup(self):
        self.startTimer(5.0)

    ##~~ SettingsPlugin mixin

    def get_settings_defaults(self):
        return dict(
            # put your plugin's default settings here
        )

    ##~~ AssetPlugin mixin

    def get_assets(self):
        # Define your plugin's asset files to automatically include in the
        # core UI here.
        return dict(
            js=["js/rackcase.js"],
            css=["css/rackcase.css"],
            less=["less/rackcase.less"],
        )

    ##~~ Softwareupdate hook

    def get_update_information(self):
        # Define the configuration for your plugin to use with the Software Update
        # Plugin here. See https://docs.octoprint.org/en/master/bundledplugins/softwareupdate.html
        # for details.
        return dict(
            rackcase=dict(
                displayName="Rackcase Plugin",
                displayVersion=self._plugin_version,
                # version check: github repository
                type="github_release",
                user="bkryza",
                repo="OctoPrint-RackCase",
                current=self._plugin_version,
                # update method: pip
                pip="https://github.com/bkryza/OctoPrint-RackCase/archive/{target_version}.zip",
            )
        )

    def startTimer(self, interval):
        self._logger.info("STARTING SENSORS CHECK TIMER")
        self._checkSensorsTimer = RepeatedTimer(
            interval, self.checkSensors, None, None, True
        )
        self._checkSensorsTimer.start()

    def checkSensors(self):
        self._logger.info("Updating rackcase sensors")
        while not self._ccs811.data_ready:
            pass
        self._plugin_manager.send_plugin_message(
            self._identifier,
            dict(
                temperature=self._bme280.temperature,
                humidity=self._bme280.humidity,
                voc=self._cs811.tvoc,
                co2=self._cs811.eco2,
            ),
        )


# If you want your plugin to be registered within OctoPrint under a different name than what you defined in setup.py
# ("OctoPrint-PluginSkeleton"), you may define that here. Same goes for the other metadata derived from setup.py that
# can be overwritten via __plugin_xyz__ control properties. See the documentation for that.
__plugin_name__ = "Rackcase Plugin"

# Starting with OctoPrint 1.4.0 OctoPrint will also support to run under Python 3 in addition to the deprecated
# Python 2. New plugins should make sure to run under both versions for now. Uncomment one of the following
# compatibility flags according to what Python versions your plugin supports!
# __plugin_pythoncompat__ = ">=2.7,<3" # only python 2
__plugin_pythoncompat__ = ">=3,<4"  # only python 3
# __plugin_pythoncompat__ = ">=2.7,<4" # python 2 and 3


def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = RackcasePlugin()

    global __plugin_hooks__
    __plugin_hooks__ = {
        "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
    }
