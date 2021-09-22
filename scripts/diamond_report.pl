#!/usr/bin/env perl

use strict;
use Bio::SeqIO;
use File::Basename;

unless (@ARGV==3) {
	print "Incorrect number of arguments\n";
	exit;
}

my $tsv = shift;
my $faa = shift;
my $outdir = shift;

my $con;
my $bin;

my $binid = basename $tsv;
$binid =~ s/.diamond.tsv//g;

my $in = Bio::SeqIO->new(-file => $faa, -format => 'fasta');
while(my $seq = $in->next_seq) {
	my $sid = $seq->primary_id;
	my(@cdata) = split(/_/, $sid);
        my $num = pop @cdata;
        my $conid = join("_", @cdata);
	
	$bin->{$binid}->{fap}++;
	$con->{$conid}->{fap}++;
}

print "got " . $bin->{$binid}->{fap} . "\n";

my %ids;

my $lastid = "none";

open(IN, $tsv) || die "cannot open tsv\n";
while(<IN>) {
	chomp();
	my ($qseqid,$sseqid,$stitle,$pident,$qlen,$slen,$length,$mismatch,$gapopen,$qstart,$qend,$sstart,$send,$evalue,$bitscore) = split(/\t/);

	my $frac = $qlen / $slen;

	my(@cdata) = split(/_/, $qseqid);
        my $id = pop @cdata;
        my $conid = join("_", @cdata);
	
	#print "DMD: $conid\n";

	if ($qseqid ne $lastid) {
		# we have a top hit

		my $org = undef;

		if ($stitle =~ m/OS=(.+)GN=/) {
			$org = $1;
		} elsif ($stitle =~ m/OS=(.+)/) {
			$org = $1
		}

		my @tax   = split(/\s+/, $org);
		my $genus = $tax[0];
	
		$bin->{$binid}->{proteins}++;
		$con->{$conid}->{proteins}++;
		if ($frac > 0.8) {
			$bin->{$binid}->{fulllen}++;
			$con->{$conid}->{fulllen}++;
		}

		$bin->{$binid}->{genus}->{$genus}++;
		$bin->{$binid}->{org}->{$org}++;

		$con->{$conid}->{genus}->{$genus}++;
		$con->{$conid}->{org}->{$org}++;

		$bin->{$binid}->{sump} += $pident;
		$bin->{$binid}->{sumpn}++;
		$con->{$conid}->{sump} += $pident;
		$con->{$conid}->{sumpn}++;

		#print "$qseqid\t$genus\t$org\t$slen\t$qlen\t$pident\n";
	}

	$lastid = $qseqid;
	
}
close IN;

unless (-d $outdir) {
	mkdir $outdir;
}

open(BIN, ">$outdir/bin.$binid.tsv");
while(my($bn,$hr) = each %{$bin}) {
	print BIN $bn;
	print BIN "\t", $hr->{fap};
	print BIN "\t", $hr->{proteins};
	print BIN "\t", $hr->{fulllen};
	
	my @sg = sort {$hr->{genus}->{$b} <=> $hr->{genus}->{$a}} keys %{$hr->{genus}};
	print BIN "\t", $sg[0];
	print BIN "\t", $hr->{genus}->{$sg[0]};

	my @og = sort {$hr->{org}->{$b} <=> $hr->{org}->{$a}} keys %{$hr->{org}};
        print BIN "\t", $og[0];
        print BIN "\t", $hr->{org}->{$og[0]};

	if ($hr->{sumpn} > 0) {
		my $mean = sprintf("%0.2f", $hr->{sump} / $hr->{sumpn});
		print BIN "\t", $mean;
	} else {
		print BIN "\t0";
	}
	print BIN "\n";

}
close BIN;

#exit;
open(CON, ">$outdir/con.$binid.tsv");
while(my($cn,$hr) = each %{$con}) {
        print CON $cn;

	if ($cn == 99) {
		warn "cn is $cn\n";
	}

	print CON "\t", $hr->{fap};
        print CON "\t", $hr->{proteins};
        print CON "\t", $hr->{fulllen};

        my @sg = sort {$hr->{genus}->{$b} <=> $hr->{genus}->{$a}} keys %{$hr->{genus}};
        print CON "\t", $sg[0];
        print CON "\t", $hr->{genus}->{$sg[0]};

        my @og = sort {$hr->{org}->{$b} <=> $hr->{org}->{$a}} keys %{$hr->{org}};
        print CON "\t", $og[0];
        print CON "\t", $hr->{org}->{$og[0]};

	if ($hr->{sumpn} > 0) {
		my $mean = sprintf("%0.2f", $hr->{sump} / $hr->{sumpn});
       	 	print CON "\t", $mean;
	} else {
		print CON "\t0";
	}

        print CON "\n";

}

close CON;

