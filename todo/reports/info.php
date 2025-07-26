<?php
header('Content-Type: application/json');
try{
    echo json_encode([
        'size' => filesize("db.dat")
        ,'chunkLength' => 1024
    ]);
}catch (Exception $e) {
    echo '{}';
}
