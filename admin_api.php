<?php
//================================================================
// This is a 1 single combined PHP API interface

//================================================================
//Config
$docsPath = '';
$hashesPath = 'hashes.dim';

//================================================================
//Check password

if(!isset($_POST['password'])){
	echo "This specific page is admin's page.";
	return;
}
$password = $_POST['password'] ?? '';
$password = hash('sha256', $password);
$passhash = file_get_contents('passhash.key');
if($password != $passhash){
    echo 'Wrong Password!!!';
	return;
}

//Request is from the admin

//================================================================
//Useful

class Dimperpreter {
    var $code;		//source
	var $i=0;		//main index
	var $l=0;		//source length
    //custom vars
    var $lastStart=0;
    var $lastEnd=0;
	public function __construct(string $x){
		$x = ' ' . $x;
		$this->code = $x;
		$this->l = strlen($x);
	}
	public function Next(){
		//
        $this->lastStart = $this->i;
        //
		$o = $this->i;	//index 2
		$c = '';		//char at index2
		$arg = '';		//last readed argument;
		$args = (array) null;
		while($o<$this->l){
			$c=$this->code[$o];
			if($c=='@') $o++;
			else if($c==',' || $c==';'){
				$arg=substr($this->code,$this->i,$o-$this->i);
				$this->i=$o + 1;
				$o++;
				$arg=str_replace("@@","@",$arg);
				$arg=str_replace("@,",",",$arg);
				$arg=str_replace("@;",";",$arg);
				array_push($args,$arg);
				if($c==';'){
                    //
                    $this->lastEnd = $o;
					//
                    return $args;
                }
			}
			$o++;
		}
		$this->i=$o;
		return null;
	}
    public function ReadRawBeforeLast(){
        return substr($this->code,0,$this->lastStart);
    }
    public function ReadRawInsideLast(){
        return substr($this->code,$this->lastStart,$this->lastEnd - $this->lastStart);
    }
    public function ReadRawAfterLast(){
        return substr($this->code,$this->lastEnd);
    }
}

function createDirectories($path){
    if (!is_dir($path))
        // Create the directory recursively with the necessary permissions
        // The 'true' argument in mkdir makes it create the directories recursively
        mkdir($path, 0777, true);
}

//================================================================
//Recognize the command

$command = $_POST['command'] ?? '';

//================================================================
//List()
if($command == 'L'){
	echo file_get_contents($hashesPath);
}
//================================================================
//Modify(docs_path, new_hash, FILE['file'])
else if($command == 'M'){
	echo 'M: ';
	$relPath = $_POST['target'] ?? false;
	$hash = $_POST['hash'] ?? false;
	if($_FILES['file']){
		if($relPath){
			if($hash){
				//Create directory
				$targetPath = $docsPath . $relPath;
				createDirectories(substr($targetPath, 0, strrpos($targetPath, '/')));
				//Replace
				move_uploaded_file($_FILES["file"]["tmp_name"], $targetPath);
				//Update hash
				$dimp = new Dimperpreter(file_get_contents($hashesPath));
				$line = $dimp->Next();
				while($line){
					if(trim($line[0]) == $relPath){
						file_put_contents($hashesPath, $dimp->ReadRawBeforeLast() . "\n" . $relPath . ',' . $hash . ';' . $dimp->ReadRawAfterLast());
						break;
					}
					$line = $dimp->Next();
				}
				if(!$line)
					echo "Couldn't find the entry in listed files.";
				//end
				else
					echo "Done.";
			}
			else
				echo "No hash of the file provided.";
		}
		else
			echo 'No target path provided.';
	}
	else
		echo "No file uploaded.";
}
//================================================================
//Delete(docs_path)
else if($command == 'D'){
	echo 'D: ';
	$relPath = $_POST['target'] ?? false;
	if($relPath){
		//remove hash
		$dimp = new Dimperpreter(file_get_contents($hashesPath));
		$line = $dimp->Next();
		while($line){
			if(trim($line[0]) == $relPath){
				//found matching relative path
				//remove it from the list
				file_put_contents($hashesPath, $dimp->ReadRawBeforeLast() . $dimp->ReadRawAfterLast());
				//delete file
				unlink($docsPath . $relPath);
				echo 'Done';
				break;
			}
			$line = $dimp->Next();
		}
		if(!$line)
			echo "Couldn't find the entry in listed files.";
	}
	else
		echo "No target pointed.";
}
//================================================================
//Add(docs_path, new_hash, FILE['file'])
else if($command == 'A'){
	echo 'A: ';
	$relPath = $_POST['target'] ?? false;
	$hash = $_POST['hash'] ?? false;
	if($_FILES['file']){
		if($relPath){
			if($hash){
				//Create directory
				$targetPath = $docsPath . $relPath;
				createDirectories(substr($targetPath, 0, strrpos($targetPath, '/')));
				//Replace
				move_uploaded_file($_FILES["file"]["tmp_name"], $targetPath);
				//Add hash
				file_put_contents($hashesPath, file_get_contents($hashesPath) . "\n" . $relPath . ',' . $hash . ';');
				//end
				echo "Done.";
			}
			else
				echo "No hash of the file provided.";
		}
		else
			echo 'No target path provided.';
	}
	else
		echo "No file uploaded.";
}
//================================================================
//?
else{
	echo '?';
}


/*
echo shell_exec("python calc_hashes.py");
$dimp = new Dimperpreter(file_get_contents('hashes.dim'));
$line = $dimp->Next();
while($line){
    print_r($line);
    echo '<br>';
    $line = $dimp->Next();
}
*/