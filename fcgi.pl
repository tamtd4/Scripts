#!/usr/bin/perl -w
use strict;
 
my $fpm = $ARGV[0];
my $url = $ARGV[1];
 
if (!defined $fpm || !defined $url ){
    print "Usage: $0 host:port|path/to/socket /path/to/file \n";
    exit 1;
}
 
if($url =~ /^((?:\/.*)?(\/[^?]*))(?:\?(.*))?$/) {
    $ENV{REQUEST_METHOD}='GET';
    $ENV{SCRIPT_FILENAME}= $1;
    $ENV{SCRIPT_NAME}= $2;
    $ENV{QUERY_STRING}= $3 // '';
}
 
system ('cgi-fcgi', '-bind', '-connect', $fpm);
