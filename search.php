<?php
try {
    $request_text = 'TealSearch integration: PHP Error';
    // Check parameters
    if (isset($_GET['wms_app_token']) && isset($_GET['wms_hostname']) && isset($_GET['$telsearch_key']) && isset($_GET['request_text'])) {
        $wms_app_token = $_GET['wms_app_token'];
        $wms_hostname = $_GET['wms_hostname'];
        $telsearch_key = $_GET['telsearch_key'];
        $request_text = $_GET['request_text'];

        if (isset($_GET['telsearch_phonebook'])) {
            $telsearch_phonebook = $_GET['telsearch_phonebook'];
            $output = shell_exec("/var/www/telsearch_integration/main.py " . $request_text . " " . $telsearch_key . " " . $wms_hostname . " " . $wms_app_token . " " . $telsearch_phonebook . " 2>&1");
        } else {
            $output = shell_exec("/var/www/telsearch_integration/main.py " . $request_text . " " . $telsearch_key . "  " . $wms_hostname . " " . $wms_app_token . " 2>&1");
        }

        echo $output;
    } else {
        echo("TealSearch integration: Invalid parameters");
    }
} catch (Exception $e) {
    echo $request_text;
}
?>