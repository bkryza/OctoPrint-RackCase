/*
 * View model for OctoPrint-RackCase
 *
 * Author: Bartek Kryza
 * License: AGPLv3
 */
$(function() {
    function RackcaseViewModel(parameters) {
        var self = this;

        // assign the injected parameters, e.g.:
        // self.loginStateViewModel = parameters[0];
        // self.settingsViewModel = parameters[1];

        self.lightState = ko.observable(false);

        self.fanSpeed = ko.observable(0);
        self.fanRed = ko.observable(0);
        self.fanGreen = ko.observable(0);
        self.fanBlue = ko.observable(0);

        self.temperature = ko.observable(0.0);

        self.humidity = ko.observable(0.0);

        self.voc = ko.observable(0.0);

        self.co2 = ko.observable(0.0);

        self.pressure = ko.observable(0.0);

        self.onBeforeBinding = function() {}

        self.onDataUpdaterPluginMessage = function(plugin, data) {
            if (plugin != "rackcase") {
                return;
            }

            self.temperature(data.temperature);
            self.humidity(data.humidity);
            self.pressure(data.pressure);
            self.voc(data.voc);
            self.co2(data.co2);
            self.lightState(data.lightState);
            self.fanSpeed(data.fanSpeed);
            self.fanRed(data.fanRed);
            self.fanGreen(data.fanGreen);
            self.fanBlue(data.fanBlue);
        };

        self.fanSpeed.subscribe(function(newValue) {
            OctoPrint.simpleApiCommand("rackcase", "fan_speed", {
                    "speed": newValue
                })
                .done(function(data) {});
        });

        self.lightState.subscribe(function(newValue) {
            OctoPrint.simpleApiCommand("rackcase", "light_state", {
                    "state": newValue
                })
                .done(function(data) {
                    //self.getUpdateUI();
                });
        });

        self.fanRed.subscribe(function(newValue) {
            OctoPrint.simpleApiCommand("rackcase", "fan_rgb", {
                    "r": self.fanRed(),
                    "g": self.fanGreen(),
                    "b": self.fanBlue()
                })
                .done(function(data) {
                    //self.getUpdateUI();
                });
        });
        self.fanGreen.subscribe(function(newValue) {
            OctoPrint.simpleApiCommand("rackcase", "fan_rgb", {
                    "r": self.fanRed(),
                    "g": self.fanGreen(),
                    "b": self.fanBlue()
                })
                .done(function(data) {
                    //self.getUpdateUI();
                });
        });
        self.fanBlue.subscribe(function(newValue) {
            OctoPrint.simpleApiCommand("rackcase", "fan_rgb", {
                    "r": self.fanRed(),
                    "g": self.fanGreen(),
                    "b": self.fanBlue()
                })
                .done(function(data) {
                    //self.getUpdateUI();
                });
        });

    }

    ko.bindingHandlers.sliderRange = {
        init: function(element, valueAccessor, allBindingsAccessor) {
            var options = allBindingsAccessor().sliderOptions || {};
            $(element).slider(options);
            ko.utils.registerEventHandler(element, "slidechange", function(event, ui) {
                var observable = valueAccessor();
                observable.Min(ui.values[0]);
                observable.Max(ui.values[1]);
            });
            ko.utils.domNodeDisposal.addDisposeCallback(element, function() {
                $(element).slider("destroy");
            });
            ko.utils.registerEventHandler(element, "slide", function(event, ui) {
                var observable = valueAccessor();
                observable.Min(ui.values[0]);
                observable.Max(ui.values[1]);
            });
        },
        update: function(element, valueAccessor, allBindingsAccessor) {
            var value = ko.utils.unwrapObservable(valueAccessor());
            if (isNaN(value.Min())) value.Min(0);
            if (isNaN(value.Max())) value.Max(0);

            $(element).slider("option", allBindingsAccessor().sliderOptions);
            $(element).slider("values", 0, value.Min());
            $(element).slider("values", 1, value.Max());
        }
    };
    /* view model class, parameters for constructor, container to bind to
     * Please see http://docs.octoprint.org/en/master/plugins/viewmodels.html#registering-custom-viewmodels for more details
     * and a full list of the available options.
     */
    OCTOPRINT_VIEWMODELS.push({
        construct: RackcaseViewModel,
        // ViewModels your plugin depends on, e.g. loginStateViewModel, settingsViewModel, ...
        dependencies: [ /* "loginStateViewModel", "settingsViewModel" */ ],
        // Elements to bind to, e.g. #settings_plugin_rackcase, #tab_plugin_rackcase, ...
        elements: ["#tab_plugin_rackcase"]
    });
});

