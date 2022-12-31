<?php

//Plugin name: GPS_Tracker

add_action( 'wp_ajax_get_real_time_location', 'get_real_time_location_func' );
add_action( 'wp_ajax_nopriv_get_real_time_location', 'get_real_time_location_func' );

function get_real_time_location_func() {
	$post_meta = get_post_meta(671);

	wp_die(json_encode($post_meta));
}

add_action( 'wp_enqueue_scripts', 'gps_tracker_scripts' );

function gps_tracker_scripts($hook) {

    wp_enqueue_style('gps_tracker_css', 'https://unpkg.com/leaflet@1.9.3/dist/leaflet.css');

	wp_enqueue_script( 'gps_tracker_js', 'https://unpkg.com/leaflet@1.9.3/dist/leaflet.js', array('jquery') );
	wp_enqueue_script( 'gps_tracker_custom_js', plugin_dir_url(__FILE__) . 'gps_tracker.js', array('jquery') );

	// in JavaScript, object properties are accessed as ajax_object.ajax_url, ajax_object.we_value
	wp_localize_script( 'gps_tracker_js', 'gps_tracker_data',
            array( 'ajax_url' => admin_url( 'admin-ajax.php' )) );
}

add_shortcode('gps_tracker', function() {
    $content = <<<CONTENT
        <div id="map"></div>
        <style>
              #map { height: 400px; }
        </style>
CONTENT;

    return $content;

});