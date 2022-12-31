jQuery(document).ready(function($) {

	var map = L.map('map').setView([44.5, 26.0], 13);

	L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
	    maxZoom: 19,
		    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
		}).addTo(map);


	var locationMarker = L.marker([44.5, 26.0]).addTo(map);

	console.log(locationMarker);
	var data = {
		'action': 'get_real_time_location'
	};

	function get_location () {
		jQuery.post(gps_tracker_data.ajax_url, data, function(response) {
			var responseObj = JSON.parse(response);

	        console.log(responseObj['lat']);
	        console.log(responseObj['lng']);

		    var newLatLng = new L.LatLng(responseObj['lat'], responseObj['lng']);
	   		locationMarker.setLatLng(newLatLng);
	   		map.setView(newLatLng, 13);

		});
	}

	setInterval(
		get_location, 1000
	);
});