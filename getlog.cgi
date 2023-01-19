#! /usr/bin/perl


#はじあや＠ふぁみーるのパソヲタさん、本当にありがとう


#--------------------

$body = '<body bgcolor="#004040" text="#ffffff" link="#eeffee" vlink="#dddddd" alink="#ff0000">';
$bbstitle ="あやしいわーるど＠はるな";


$logdir = './log/';

$cgiurl = 'getlog.cgi';
$action ='getlog';

$bbsurl = './bbs.cgi';

# 日本語コード変換ライブラリjocde.plのパス
require './jcode.pl';

# キーワードの最大文字数（半角）
$keylength = 64;

# 時差 サーバの時計がずれてる時や日本時間以外にしたい時に使う
$tim = 0;

$\ = "\n";

#--------------------

#if ($ENV{'REQUEST_METHOD'} eq "POST") { read(STDIN, $buffer, $ENV{'CONTENT_LENGTH'}); }
#else { $buffer = $ENV{'QUERY_STRING'}; }


$buffer = $ENV{'QUERY_STRING'};


@argv = split(/&/,$buffer);
foreach (@argv) {
	($name, $value) = split(/=/);
	$value =~ tr/+/ /;

	$value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
	&jcode'convert(*value,'sjis');

	# 処理の都合上の処理
	$value =~ s/\\/\\\\/;
	$value =~ s/\[/\\[/;

	$COMMAND{$name} = $value;
}


&error(2) if (length($COMMAND{'keyword'}) > $keylength);
&viewlog if ($COMMAND{'action'} eq "$action");


&list;
	
sub list {

	&error(0) if(!opendir(DIR, $logdir));

	@files=readdir(DIR);
	closedir(DIR);

               @files = sort by_number @files;
               $end = @files;
               $end--; 

	print "Content-type: text/html\n\n";
	print "<html><head><title>$bbstitle 過去ログ</title></head>\n";
	print "$body\n";
	print "<center><font size=+1><b>$bbstitle 過去ログ</b></font><hr>\n";

	print "<form method=get action=\"$cgiurl\">";
	print "<input type=hidden name=\"action\" value=\"$action\">";
	print "<table>";
#print "<tr><td></td><td>ファイル名</td><td align=right>サイズ</td><td align=center>日付</td></tr>";
	foreach (0 .. $end) {
		if (!($files[$_] eq "." or $files[$_] eq "..")) {
			($dev,$ino,$mode,$nlink,$uid,$gid,$rdev,$size,$atime,$mtime,$ctime,$blksize,$blocks) = stat "$logdir$files[$_]";
			($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = gmtime($mtime + 32400 + $tim);
			$mon++;
			$mon = "0$mon" if ($mon < 10);
			if ($mday < 10)  { $mday  = "0$mday";  }
			if ($min < 10)  { $min =  "0$min";  }
			if ($hour < 10) { $hour = "0$hour"; }
			$checked = ' checked' if ($_ == $end);
			print "<tr><td><input type=\"radio\" name=\"logfile\" value=\"$files[$_]\"$checked></td>";
			print "<td><a href=\"$logdir$files[$_]\">$files[$_]</a></td>";
			print "<td align=right>$size\ byte</td>";
		}
	}

	print "<tr><td></td></tr><tr><td colspan=4>※ラジオボタンでファイル名を指定してください。</td></tr><tr><td></td></tr>\n";
	print "<tr><td colspan=4><select name=\"first\">";
	print "<option value=\"0\">最初";
	print "<option value=\"1\">1";
	print "<option value=\"2\">2";
	print "<option value=\"3\">3";
	print "<option value=\"4\">4";
	print "<option value=\"5\">5";
	print "<option value=\"6\">6";
	print "<option value=\"7\">7";
	print "<option value=\"8\">8";
	print "<option value=\"9\">9";
	print "<option value=\"10\">10";
	print "<option value=\"11\">11";
	print "<option value=\"12\">12";
	print "<option value=\"13\">13";
	print "<option value=\"14\">14";
	print "<option value=\"15\">15";
	print "<option value=\"16\">16";
	print "<option value=\"17\">17";
	print "<option value=\"18\">18";
	print "<option value=\"19\">19";
	print "<option value=\"20\">20";
	print "<option value=\"21\">21";
	print "<option value=\"22\">22";
	print "<option value=\"23\">23";
	print "</select>から";
	print "<select name=\"last\">";
	print "<option value=\"24\">最後";
	print "<option value=\"1\">1";
	print "<option value=\"2\">2";
	print "<option value=\"3\">3";
	print "<option value=\"4\">4";
	print "<option value=\"5\">5";
	print "<option value=\"6\">6";
	print "<option value=\"7\">7";
	print "<option value=\"8\">8";
	print "<option value=\"9\">9";
	print "<option value=\"10\">10";
	print "<option value=\"11\">11";
	print "<option value=\"12\">12";
	print "<option value=\"13\">13";
	print "<option value=\"14\">14";
	print "<option value=\"15\">15";
	print "<option value=\"16\">16";
	print "<option value=\"17\">17";
	print "<option value=\"18\">18";
	print "<option value=\"19\">19";
	print "<option value=\"20\">20";
	print "<option value=\"21\">21";
	print "<option value=\"22\">22";
	print "<option value=\"23\">23";
	print "</select>まで　<input type=submit value=\"Get\"><p>";
	print "<select name=\"searchmode\">";
	print "<option value=\"name\">投稿者";
	print "<option value=\"keyword\">内容";
	print "<option value=\"subject\">題名\n</select>";
	print "：<input type=text name=\"keyword\" size=\"12\" maxlength=$keylength>";
	print "<input type=submit value=\"Search\"></td></tr></form>";
	print "</table>";
	print "<hr>";
	print "現在ベータテスト中です。バグを見つけたら掲示板に書いてね";
	print "<p align=center><a href=\"$bbsurl\">掲示板へ</a></p>";
	print "<h4 align=right>Getlog Ver0.3b3</h4>";
	print "</body></html>";
}



sub viewlog {

	if (!open(DB,"$logdir$COMMAND{'logfile'}")) { &error(1); }
	@lines = <DB>;
	close(DB);
	$COMMAND{'last'} = $COMMAND{'first'} + 1 if ($COMMAND{'first'} >= $COMMAND{'last'});
	$first = $COMMAND{'first'};
	$last = $COMMAND{'last'};

	$first = "0$COMMAND{'first'}" if ($first < 10);
	$last = "0$COMMAND{'last'}" if ($last < 10);
	
	if ($COMMAND{'searchmode'} eq 'name') { $keyword = "投稿者：.*>${COMMAND{'keyword'}}<"; }
	elsif ($COMMAND{'searchmode'} eq 'subject') { $keyword = "color=\"#ffffee\"><b>${COMMAND{'keyword'}}</b></font>"; }
	else { $keyword = $COMMAND{'keyword'}; }


	print "Content-type: text/html\n";
	print "<html><head><title>$bbstitle 過去ログ $COMMAND{'logfile'}</title></head>";
	print "$body";
	print "<h1>$COMMAND{'logfile'} $first時～$last時</h1>";
	$end = @lines;
	$end--;
	foreach (0 .. $end) {
		if ($lines[$_] =~ /<font size=-1>　投稿日：/) {
			$hour = substr( $lines[$_], 36, 4 );
			last if ($hour ge "$first時");
		}
		$skip++;
	}
	$skip--;
	foreach ($skip .. $end) {
		if ($lines[$_] =~ /<font size=-1>　投稿日：/) {
			$hour = substr( $lines[$_], 36, 4 );
			last if ($hour ge "$last時");
		}
		

		if ($keyword ne '') {
			if ($lines[$_] =~ /$keyword/) {
				$flag = 1;
				$hit++; 
			}
			push( @article, $lines[$_] );
			if ($lines[$_] =~ /<\/blockquote>/) {
				print @article if ($flag > 0);  
				splice( @article, 0 );
				$flag = 0;
			}
		}
		else { print $lines[$_]; }

	}
	if ($keyword ne '') {
		print "<hr>";
		$keyword =~ s/\\\\/\\/;
		$keyword =~ s/\\\[/\[/;
		if ( $hit > 0 ) { print "<h3>キーワード「$COMMAND{'keyword'}」は $hit件見つかりました。</h3>"; }
		else { print "<h3>キーワード「$COMMAND{'keyword'}」は見つかりませんでした。</h3>"; }
	}
	print "</body></html>";

	exit;

}



sub error {

	$error = $_[0];
	if ($error == 0) { $errmsg = 'ディレクトリが開けませんでした。'; }
	if ($error == 1) { $errmsg = 'ファイルが開けませんでした。'; }
	if ($error == 2) { $errmsg = 'キーワードが長すぎます。'; }

	print "Content-type: text/html\n";
	print "<html><head><title>エラー</title></head>";
	print "$body";
	print "<h1>$errmsg</h1>";
	print "</body></html>";
	exit;
}




sub by_number {
	$a <=> $b;
}
