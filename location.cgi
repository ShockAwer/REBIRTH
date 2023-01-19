#! /usr/bin/perl

#

#ろけーしょん

#1997.9.14製作

#すくりぷと　ばい　ゆいちゃっと　

#　　　　　　　　　Since  1996

#



&decode;

&html if($url);

&html2;



sub html{



print "Location: $url\n\n";

print "Pragma: no cache\n";

print "Expires: Thu, 16 Dec 1994 16:00:GMT\n\n";

exit;

}#html END



sub decode{	#一般的なデコード＆変数への代入

$buffer = $ENV{'QUERY_STRING'};

@pairs = split(/&/,$buffer);

	foreach $pair (@pairs) {

		($name, $value) = split(/=/, $pair);

		$value =~ tr/+/ /;

		$value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;

		$value =~ s/\n//g;	$value =~ s/\r//g;

		$FORM{$name} = $value;

	}

	$url = $FORM{'url'};

}#decode END



sub html2{

print "Content-type: text/html\n\n";

print <<"_HTML_";

<HTML><HEAD>

<TITLE>フォームで移動。</TITLE>

</HEAD></HTML>

_HTML_

exit;

}#html2 END

__END__
