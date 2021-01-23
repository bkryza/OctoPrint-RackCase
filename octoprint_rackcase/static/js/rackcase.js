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

        self.onBeforeBinding = function() {
        }

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
	   var request = { command: "fan_speed", speed: newValue };
	   $.ajax({
		url: "/api/plugin/rackcase",
		type: "POST",
		dataType: "application/json",
		data: request,
		success: function (data) {
                  alert("The lightstate is " + newValue);
		  self.getUpdateUI();  
		}
	   });           
        });


	self.lightState.subscribe(function(newValue) {
	   var request = { command: "light_state", state: newValue };
	   $.ajax({
		url: "/api/plugin/rackcase",
		type: "POST",
		dataType: "application/json",
		data: request,
		success: function (data) {
                  alert("The lightstate is " + newValue);
		  self.getUpdateUI();  
		}
	   });           
        });

	self.fanRed.subscribe(function(newValue) {
	   var request = { command: "fan_rgb", r: self.fanRed(), g: self.fanGreen(), b: self.fanBlue() };
	   $.ajax({
		url: "/api/plugin/rackcase",
		type: "POST",
		dataType: "application/json",
		data: request,
		success: function (data) {
		  self.getUpdateUI();  
		}
	   });           
        });
   	self.fanGreen.subscribe(function(newValue) {
	   var request = { command: "fan_rgb", r: self.fanRed(), g: self.fanGreen(), b: self.fanBlue() };
	   $.ajax({
		url: "/api/plugin/rackcase",
		type: "POST",
		dataType: "application/json",
		data: request,
		success: function (data) {
		  self.getUpdateUI();  
		}
	   });           
        });
	self.fanBlue.subscribe(function(newValue) {
	   var request = { command: "fan_rgb", r: self.fanRed(), g: self.fanGreen(), b: self.fanBlue() };
	   $.ajax({
		url: "/api/plugin/rackcase",
		type: "POST",
		dataType: "application/json",
		data: request,
		success: function (data) {
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
