<?php
//main function
function ReadChunk($targetFile, $targetPage, $chunkLength = 512) {
    //reading
    //check page number
    if($targetPage < 0)
        //404
        return false;

    //read basic
    $max = filesize($targetFile);
    $targetPage *= $chunkLength;

    //check size
    if($targetPage > $max)
        //404
        return false;
    else{
        //page must exist
        $stream = fopen($targetFile, "r");
        fseek($stream, $targetPage);
        echo stream_get_contents($stream, $chunkLength);
        fclose($stream);
    }
}

//exec
$i = $_GET["page"] ?? 0;
if(is_numeric($i)){
    ReadChunk("db.dat", $i, 1024);
}