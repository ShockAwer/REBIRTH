#! /usr/local/bin/perl


#�͂����⁗�ӂ��݁[��̃p�\���^����A�{���ɂ��肪�Ƃ�


#--------------------

$body = '<body bgcolor="#004040" text="#ffffff" link="#eeffee" vlink="#dddddd" alink="#ff0000">';
$bbstitle ="���₵����[��ǁ��͂��";


$logdir = './log/';

$cgiurl = 'getlog.cgi';
$action ='getlog';

$bbsurl = './bbs.cgi';

# ���{��R�[�h�ϊ����C�u����jocde.pl�̃p�X
require './jcode.pl';

# �L�[���[�h�̍ő啶�����i���p�j
$keylength = 64;

# ���� �T�[�o�̎��v������Ă鎞����{���ԈȊO�ɂ��������Ɏg��
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

	# �����̓s����̏���
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
	print "<html><head><title>$bbstitle �ߋ����O</title></head>\n";
	print "$body\n";
	print "<center><font size=+1><b>$bbstitle �ߋ����O</b></font><hr>\n";

	print "<form method=get action=\"$cgiurl\">";
	print "<input type=hidden name=\"action\" value=\"$action\">";
	print "<table>";
#print "<tr><td></td><td>�t�@�C����</td><td align=right>�T�C�Y</td><td align=center>���t</td></tr>";
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

	print "<tr><td></td></tr><tr><td colspan=4>�����W�I�{�^���Ńt�@�C�������w�肵�Ă��������B</td></tr><tr><td></td></tr>\n";
	print "<tr><td colspan=4><select name=\"first\">";
	print "<option value=\"0\">�ŏ�";
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
	print "</select>����";
	print "<select name=\"last\">";
	print "<option value=\"24\">�Ō�";
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
	print "</select>�܂Ł@<input type=submit value=\"Get\"><p>";
	print "<select name=\"searchmode\">";
	print "<option value=\"name\">���e��";
	print "<option value=\"keyword\">���e";
	print "<option value=\"subject\">�薼\n</select>";
	print "�F<input type=text name=\"keyword\" size=\"12\" maxlength=$keylength>";
	print "<input type=submit value=\"Search\"></td></tr></form>";
	print "</table>";
	print "<hr>";
	print "���݃x�[�^�e�X�g���ł��B�o�O����������f���ɏ����Ă�";
	print "<p align=center><a href=\"$bbsurl\">�f����</a></p>";
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
	
	if ($COMMAND{'searchmode'} eq 'name') { $keyword = "���e�ҁF.*>${COMMAND{'keyword'}}<"; }
	elsif ($COMMAND{'searchmode'} eq 'subject') { $keyword = "color=\"#ffffee\"><b>${COMMAND{'keyword'}}</b></font>"; }
	else { $keyword = $COMMAND{'keyword'}; }


	print "Content-type: text/html\n";
	print "<html><head><title>$bbstitle �ߋ����O $COMMAND{'logfile'}</title></head>";
	print "$body";
	print "<h1>$COMMAND{'logfile'} $first���`$last��</h1>";
	$end = @lines;
	$end--;
	foreach (0 .. $end) {
		if ($lines[$_] =~ /<font size=-1>�@���e���F/) {
			$hour = substr( $lines[$_], 36, 4 );
			last if ($hour ge "$first��");
		}
		$skip++;
	}
	$skip--;
	foreach ($skip .. $end) {
		if ($lines[$_] =~ /<font size=-1>�@���e���F/) {
			$hour = substr( $lines[$_], 36, 4 );
			last if ($hour ge "$last��");
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
		if ( $hit > 0 ) { print "<h3>�L�[���[�h�u$COMMAND{'keyword'}�v�� $hit��������܂����B</h3>"; }
		else { print "<h3>�L�[���[�h�u$COMMAND{'keyword'}�v�͌�����܂���ł����B</h3>"; }
	}
	print "</body></html>";

	exit;

}



sub error {

	$error = $_[0];
	if ($error == 0) { $errmsg = '�f�B���N�g�����J���܂���ł����B'; }
	if ($error == 1) { $errmsg = '�t�@�C�����J���܂���ł����B'; }
	if ($error == 2) { $errmsg = '�L�[���[�h���������܂��B'; }

	print "Content-type: text/html\n";
	print "<html><head><title>�G���[</title></head>";
	print "$body";
	print "<h1>$errmsg</h1>";
	print "</body></html>";
	exit;
}




sub by_number {
	$a <=> $b;
}
