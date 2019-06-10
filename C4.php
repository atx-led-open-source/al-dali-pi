<?php

$request = explode('&',$_SERVER["QUERY_STRING"]);
$DALI = explode('=',$request[0]);

if( $DALI[0] != "DALI" ){
	echo "Send DALI command as <a href=C4.php?DALI=FE00>DALI=xxyy</a> ";
	exit();
	}
	

$org = explode('=',$request[1]);
$Verb = explode('=',$request[2]);


$sa2 = substr($DALI[1],0,2);

if($org[0] == "org" )
	$sa2 = $org[1];

$sa2 = hexdec($sa2)&254;
$sa2 = dechex($sa2);

$sa = (hexdec($sa2)&254) /2;
if($sa == 0)
	$sa2 = "00";
if($sa < 16)
	$sa2 = "0".$sa2;


$friend = "Add $sa ";
if( $sa > 63 )
   $friend = "Group ".($sa-64);
if( $sa > 79 )
   $friend = "Broadcast ";

$command = "sudo /usr/bin/python /home/pi/DALI_Arg.py $DALI[1] 2>&1; echo $?";

$output = shell_exec($command);

if($Verb[1] == "0" ){
	echo "Response: $output";
	exit();
	}

echo '<html><body><center>';
echo  '<img src=http://atxled.com/images/ATX-Brand.gif border=0 width=10% ><p>';
echo "<a href=C4.php?DALI=$sa2"."00 >$friend Off</a>";
echo "<br><a href=C4.php?DALI=$sa2"."80 >$friend 50%</a>";
echo "<br><a href=C4.php?DALI=$sa2"."FE >$friend ON</a>";
echo "<p>Broadcast Shortcuts<p>";
echo "<a href=C4.php?DALI=FE00&org=$sa2>All Off</a>";
echo "<br><a href=C4.php?DALI=FEFE&org=$sa2>All On</a>";

	echo "<p>Groups shortcuts ( set Off ) <p>";
	for( $i=0; $i<16; ++$i){
		$sa2 = dechex($i*2+128);
		echo "<a href=C4.php?DALI=$sa2"."00>$i</a> ";
		}
	echo "<p>Individual shortcuts ( set Off )<p>";
	for( $i=0; $i<16; ++$i){
		$sa2 = dechex($i*2);
		if( $i < 8 )
			$sa2 = "0".$sa2;
		echo "<a href=C4.php?DALI=$sa2"."00>$i</a> ";
		if($i == 7)
			echo "<br>";
		}

	echo "<br>";
	for( $i=16;$i<32; ++$i){
		$sa2 = dechex($i*2);
		echo "<a href=C4.php?DALI=$sa2"."00>$i</a> ";
		if($i == 23)
			echo "<br>";
		}

echo "<p>Most commands have no response<p>Response: $output<br>\r\n";

?>

