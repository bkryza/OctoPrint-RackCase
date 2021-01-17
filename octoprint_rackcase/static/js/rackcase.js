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

	self.temperature = ko.observable(0.0);

        self.humidity = ko.observable(0.0);

        self.voc = ko.observable(0.0);

	self.co2 = ko.observable(0.0);

	self.pressure = ko.observable(0.0);

        self.onBeforeBinding = function() {
        }

        self.setFanSpeed = function() {

        };

        self.onDataUpdaterPluginMessage = function(plugin, data) {
            if (plugin != "rackcase") {
                return;
            }

            self.temperature(data.temperature);
            self.humidity(data.humidity);
	    self.pressure(data.pressure);
            self.voc(data.voc);
            self.co2(data.co2);
        };

	self.lightState.subscribe(function(newValue) {
	   var request = { command: "light_state", state: newValue };
	   $.ajax({
		url: "/api/plugin/rackcase",
		type: "POST",
		dataType: "json",
		data: request,
		success: function (data) {
                  alert("The lightstate is " + newValue);
		  self.getUpdateUI();  
		}
	   });           
        });
    }

    /* view model class, parameters for constructor, container to bind to
     * Please see http://docs.octoprint.org/en/master/plugins/viewmodels.html#registering-custom-viewmodels for more details
     * and a full list of the available options.
     */
    OCTOPRINT_VIEWMODELS.push({
        construct: RackcaseViewModel,
        // ViewModels your plugin depends on, e.g. loginStateViewModel, settingsViewModel, ...
        dependencies: [ /* "loginStateViewModel", "settingsViewModel" */ ],
        // Elements to bind to, e.g. #settings_plugin_rackcase, #tab_plugin_rackcase, ...
        elements: [ "#tab_plugin_rackcase" ]
    });
});
