#!/usr/bin/env perl

use File::Basename;

my @csv = @ARGV;

foreach $c (@csv) {
	my $base = basename $c, ".csv";

	open(IN, $c);
	while(<IN>) {
		next if (m/^intersect/);
		print "$base,";
		print;
		last;
	}
	close IN;
}
