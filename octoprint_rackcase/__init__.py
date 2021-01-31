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
import time
import board
import busio
import digitalio
import adafruit_ccs811
import adafruit_bme280
import pigpio


class RackcasePlugin(
    octoprint.plugin.StartupPlugin,
    octoprint.plugin.SettingsPlugin,
    octoprint.plugin.AssetPlugin,
    octoprint.plugin.TemplatePlugin,
    octoprint.plugin.SimpleApiPlugin,
):
    def __init__(self):
        self._checkSensors = None
        self._ccs811_reset = digitalio.DigitalInOut(board.D18)
        self._ccs811_reset.direction = digitalio.Direction.OUTPUT
        self.init_ccs811()

        self._i2c_bus = busio.I2C(board.SCL, board.SDA)
        self._ccs811 = adafruit_ccs811.CCS811(self._i2c_bus, address=0x5B)
        self._bme280 = adafruit_bme280.Adafruit_BME280_I2C(
            self._i2c_bus, address=0x76
        )
        self.R_PIN = 8
        self.G_PIN = 7
        self.B_PIN = 25
        self.FAN_PIN = 12
        self.LIGHT_PIN = 16
        self.pgpio = pigpio.pi()
        self.pgpio.set_PWM_frequency(self.LIGHT_PIN, 120)
        self.pgpio.set_PWM_frequency(self.FAN_PIN, 25000)
        self.pgpio.set_PWM_dutycycle(self.FAN_PIN, 50)

    def get_api_commands(self):
        return dict(
            light_state=["state"],
            fan_speed=["speed"],
            fan_rgb=["r", "g", "b"],
        )

    def on_api_command(self, command, data):
        import flask
        if command == "light_state":
            light_state = False
            if "state" in data:
                light_state = int(data["state"])
            self._logger.info("light_state command called - {light_state}".format(light_state=light_state))
            self.pgpio.write(self.LIGHT_PIN, light_state)
            return
        if command == "fan_speed":
            fan_speed = 0
            if "speed" in data:
                fan_speed = int(data["speed"])
            self._logger.info("fan_speed command called - {fan_speed}".format(fan_speed=fan_speed))
            self.pgpio.set_PWM_dutycycle(self.FAN_PIN, min(fan_speed, 255))
            return
        if command == "fan_rgb":
            r = int(data["r"])
            g = int(data["g"])
            b = int(data["b"])
            self._logger.info("fan_rgb command called -[{}, {}, {}]".format(r, g, b))
            self.pgpio.set_PWM_dutycycle(self.R_PIN, 255-min(r, 255))
            self.pgpio.set_PWM_dutycycle(self.G_PIN, 255-min(g, 255))
            self.pgpio.set_PWM_dutycycle(self.B_PIN, 255-min(b, 255))
            return


    def on_api_get(self, request):
        import flask
        light_state = (self._pca.channels[8].duty_cycle == 0x0000)
        return flask.jsonify(light_state=light_state)

    def init_ccs811(self):
        self._ccs811_reset.value = True
        time.sleep(0.1)
        self._ccs811_reset.value = False
        time.sleep(0.1)
        self._ccs811_reset.value = True

    def on_after_startup(self):
        self.startTimer(15.0)

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
        self._logger.debug("Starting sensors check timer")
        self._checkSensorsTimer = RepeatedTimer(
            interval, self.checkSensors, None, None, True
        )
        self._checkSensorsTimer.start()

    def checkSensors(self):
        self._logger.debug("Updating rackcase sensors")
        temperature = round(self._bme280.temperature, 2)
        humidity = round(self._bme280.relative_humidity, 2)
        pressure = round(self._bme280.pressure, 2)

        timeout = time.time() + 10
        while not self._ccs811.data_ready:
            if time.time() > timeout:
                self._logger.debug("CCS811 TIMED OUT...")
                return
            pass

        voc = round(self._ccs811.tvoc, 2)
        co2 = round(self._ccs811.eco2, 2)
        self._plugin_manager.send_plugin_message(
            self._identifier,
            dict(
                temperature=temperature,
                humidity=humidity,
                pressure=pressure,
                voc=voc,
                co2=co2,
                fanSpeed=self.pgpio.get_PWM_dutycycle(self.FAN_PIN),
                fanRed=self.pgpio.get_PWM_dutycycle(self.R_PIN),
                fanGreen=self.pgpio.get_PWM_dutycycle(self.G_PIN),
                fanBlue=self.pgpio.get_PWM_dutycycle(self.B_PIN),
                lightState=self.pgpio.get_PWM_dutycycle(self.LIGHT_PIN),
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
