<?php

$hostip = $_SERVER['SERVER_ADDR'];

$level = 128;

if( $hostip == "::1"){
        exec('/sbin/ifconfig', $resultArray);

        for( $i=0; $i< sizeof($resultArray);++$i){
                if( substr($resultArray[$i],0,4) == "eth0"){
                        if( substr($resultArray[$i+1],0,12) == "        inet"){
                                $inet = explode(" ",$resultArray[$i+1]);
                                $hostip = "$inet[9]";
                                }
                        }

                if( substr($resultArray[$i],0,5) == "wlan0"){
                        if( substr($resultArray[$i+1],0,12) == "        inet"){
                                $inet = explode(" ",$resultArray[$i+1]);
                                $hostip = "$inet[9]";
                                }
                        }
                }
        }


$BASE = dirname(__FILE__);

$request = explode('&',$_SERVER["QUERY_STRING"]);

$DALI[1] = "FE00";
$sa2=0;
$color="";

for($i=0; $request[$i] != "";++$i) {
        $param = explode('=',$request[$i]);
        if($param[0]=="DALI"){
                $sa2 = substr($param[1],0,2);
                $DALI[1] = $param[1];
                }
        if($param[0]=="org")
                $sa2 = $param[1];
        if($param[0]=="Verb")
                $Verb = $param[1];
        if($param[0]=="color")
                $color = $param[1];
        if($param[0]=="level"){
		$levels = sprintf('%02x', $param[1]);
                $level = intval($param[1]);
		}
        }

$sa2 = hexdec($sa2)&254;
$sa2 = dechex($sa2);
$sa3 = hexdec($sa2)|1;
$sa3 = dechex($sa3);

$sa = (hexdec($sa2)&254) /2;
if($sa == 0){
        $sa2 = "0";
        $sa3 = "1";
        }
if($sa < 8){
        $sa2 = "0".$sa2;
        $sa3 = "0".$sa3;
        }

$friend = "Single Address $sa";
if( $sa > 63 )
   $friend = "Group ".($sa-64);
if( $sa > 79 )
   $friend = "Broadcast ";
echo '<html><title>ATX-LED DALI C4 API></title><body><center>';

if( $hostip != "216.92.78.96"){

        echo " Click here for <a href=/ target=new > Hue interface Emulation and LorControl </a><p>";


        if($hostip != "127.0.0.1")
                $hostip = "http://".$hostip."/C4.php?level=$level";
        else
                $hostip = "C4.php";


        if($color != ""){
                $DALI[1] = $DALI[1].$sa3;
                $command = 'sudo /usr/bin/python "' . $BASE . '/DALI/DALI_Color.py" ' . escapeshellarg($DALI[1]) . " 2>&1; echo $?";
                }
        else
                $command = 'sudo /usr/bin/python "' . $BASE . '/DALI/DALI_Arg.py" ' . escapeshellarg($DALI[1]) . " 2>&1; echo $?";

        $output = shell_exec($command);

        if($Verb == "0" ){
                echo "Response: $output";
                exit();
        }
}else{
         $hostip = "http://atxled.com/Pi/C4.php?level=$level";

        if($Verb == "0" ){
                if($DALI[1] == "0100")
                        echo "JFF\n<br>H24E0<br>H2000";
                else
                        echo "N\n";
                exit();
        }

	echo "<html><body><title> C4 API </title>";	
        echo " Demo Mode!!  Run from a Pi!<br>";
        echo " Click here to redirect to <a href=http://me.atxled.com/C4.php > your Pi </a><p>";
        $output = " only valid when running on a Pi";
        }

$pct = intval($level*100 / 254 + .5);


echo  '<img src=http://atxled.com/images/ATX-Brand.gif border=0 width=15% ><br>';
echo "<font size=5 color=Red >$friend</font><br><table><tr>";

echo "<td><br>Brightness: ";;
echo "&nbsp; <a href=$hostip&DALI=$sa3"."00&level=0>Off</a> ";
echo "&nbsp; <a href=$hostip&DALI=$sa3"."06&level=3>Min</a> ";
echo "&nbsp; <a href=$hostip&DALI=$sa2"."80&level=128>50%</a> ";
echo "&nbsp; <a href=$hostip&DALI=$sa3"."05&level=254>Max</a></td></tr><tr><td>";

        for( $i=1; $i<11; ++$i){
		$val = intval(($i*254)/10);
		$Dal = $sa2;
		$Dal .= sprintf('%02x',$val);
		echo "&nbsp;<a href=$hostip&DALI=$Dal&level=$val>$i"."0</a> ";
                }
$Dal = $sa2;
$Dal .= sprintf('%02x',$level);

echo "<br>&nbsp;</td></tr><tr><td>Color @ $pct %: <a href=$hostip&DALI=$Dal"."0090&color=1 >2700K</a>";
echo "&nbsp; <a href=$hostip&DALI=$Dal"."0100&color=1 >3500K</a>";
echo "&nbsp; <a href=$hostip&DALI=$Dal"."0170&color=1 >4000K</a>";
echo "&nbsp; <a href=$hostip&DALI=$Dal"."01F0&color=1 >5000K</a></td></tr></table>";

echo"<hr width=30%>";
echo "<font size=5 color=Red> Broadcast to All</font><p>";
#echo "<a href=$hostip&DALI=FE00&org=$sa2>All Off</a>";
#echo "<br><a href=$hostip&DALI=FEFE&org=$sa2>All On</a>";

        echo "Brightness: ";;
	echo "&nbsp; <a href=$hostip&DALI=FF00&level=0&org=$sa2 >Off</a> ";
	echo "&nbsp; <a href=$hostip&DALI=FF06&level=3&org=$sa2 >Min</a> ";
	echo "&nbsp; <a href=$hostip&DALI=FF05&level=254&org=$sa2 >Max</a><br>";

        for( $i=1; $i<11; ++$i){
		$val = intval(($i*254)/10);
		$Dal = sprintf('FE%02x',$val);
		echo "&nbsp;<a href=$hostip&DALI=$Dal&level=$val&org=$sa2 >$i"."0</a> ";
                }


echo"<hr width=30%>";

        echo "<font size=5 color=Red>Group <font size=3> ( set off )</font></font> <p>";
        for( $i=0; $i<16; ++$i){
                $sa2 = dechex($i*2+128);
                echo "&nbsp;<a href=$hostip&DALI=$sa2"."00>$i</a> ";
                }
echo"<hr width=30%>";

        echo "<font size=5 color=Red>Individual Address: set to $pct % </font><br>";
        for( $i=0; $i<64; ++$i){
                if(( $i & 15 ) == 0 ){
                        echo "<br>$i &nbsp; ";
			}
		$sa2 = sprintf('%02x', $i*2);
		$sa2 .= sprintf('%02x', $level);

		if( $i < 10 )
	                echo "&nbsp; <a href=$hostip&DALI=$sa2 >$i</a> ";
		else
                	echo "<a href=$hostip&DALI=$sa2 >$i</a> ";
                }

echo "<p>Most commands have no response<p>Most recent Response: $output<br>\r\n";
