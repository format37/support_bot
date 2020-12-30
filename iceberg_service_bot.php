<?php
$json = file_get_contents('php://input');
$action = json_decode($json, true);
$message        = $action['message']['text'];
$chat           = $action['message']['chat']['id'];
$user           = $action['message']['from']['id'];
$message = urlencode($message);
file_get_contents("http://localhost:8084/relay?user=$user&text=$message");
?>
