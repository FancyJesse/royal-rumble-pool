<?php
	if(empty($_POST['entry_name'])){
		exit();
	}

	$pythonScript = '../royalrumblepool.py';
	$name = trim($_POST['entry_name']);
	$comment = empty($_POST['entry_comment']) ? '' : trim($_POST['entry_comment']);
	$cmd = 'python3 ' .
		$pythonScript .
		' -add ' .
		escapeshellarg($name) .
		' ' .
		escapeshellarg($comment);

	$output = shell_exec($cmd);
	echo $output;
?>
