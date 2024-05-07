<?php
try {

    $request_text = $_GET['request_text'];
    $telsearch_key = $_GET['telsearch_key'];

    if(isset($_GET['wms_app_token']) && isset($_GET['telsearch_phonebook']) && isset($_GET['wms_hostname'])) {
        $wms_app_token = $_GET['wms_app_token'];
        $telsearch_phonebook = $_GET['telsearch_phonebook'];
        $wms_hostname = $_GET['wms_hostname'];
        $output = shell_exec("/var/www/telsearch_integration/main.py ".$request_text." ".$telsearch_key." ".$wms_hostname." ".$wms_app_token." ".$telsearch_phonebook." 2>&1");
    } else {
        $output = shell_exec("/var/www/telsearch_integration/main.py ".$request_text." ".$telsearch_key."  ".$wms_hostname." ".$wms_app_token." 2>&1");
    }

    echo($output);
} catch (Exception $e) {
    echo $request_text;
}
?>