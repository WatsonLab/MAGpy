#!/usr/bin/env perl

use Color::Mix;
use File::Basename;

my $checkm_file = shift;
my $tree_file   = shift;

my $tbase = $tree_file;
$tbase = basename $tbase, (".nwk",".sml");


&produce_tree("superkingdom",15);
&produce_tree("phylum",17);
&produce_tree("class",18);
&produce_tree("order",19);
&produce_tree("family",20);
&produce_tree("genus",21);




sub produce_tree {

        my $n = shift;
        my $c = shift;

        my $annot = get_annotations($n, $c);
        open(OUT, ">${n}_annot.txt");
	print OUT "clade_marker_size\t1\nclade_marker_color\twhite\nclade_separation\t0.0\n";
	print OUT $annot;
	close OUT;

	print "graphlan_annotate.py --annot ${n}_annot.txt $tree_file $tbase.tree.$n.xml\n";
	system("graphlan_annotate.py --annot ${n}_annot.txt $tree_file $tbase.tree.$n.xml");
	print "graphlan.py --format png --pad 0.5 --dpi 600 --size 8 $tbase.tree.$n.xml $tbase.tree.$n.png\n";
	system("graphlan.py --format png --pad 0.5 --dpi 600 --size 8 $tbase.tree.$n.xml $tbase.tree.$n.png");
}



sub get_annotations {

	my $lev = shift;
	my $col = shift;

	my $ret = "";

	my $title;
	open(IN, $checkm_file);
	while(<IN>) {
		chomp();
		@titles = split(/\t/);
		$title = $titles[$col];
		last;
	}

	my %map;


	while(<IN>) {
		chomp();
		my @data = split(/\t/);

		next unless ($data[$col] =~ m/\w/);

		$map{$data[$col]}++;
	}
	close IN;

	my @things = sort keys %map;
	my $nthings = scalar @things;

	my $cmix = Color::Mix->new;

	my @colours = $cmix->analogous('0000ff', $nthings, $nthings+1); 

	open(COLS, ">$lev.legendcols.txt");

	my %mc;
	for ($i=0;$i<$nthings;$i++) {
		$mc{$things[$i]} = '#' . $colours[$i];
		$mc{$things[$i]} =~ tr/[a-z]/[A-Z]/;
		print COLS "$things[$i]\t" . $mc{$things[$i]} . "\n";
		print "linking $things[$i] to $colours[$i]\n";
	}
	close COLS;

	open(IN, $checkm_file);
	while(<IN>) {
        	last;
	}

	while(<IN>) {
        	chomp();

		my @data = split(/\t/);

		my $label = $data[$col];
		$label =~ s/\s+//g;

		if (exists $mc{$label}) {

			$ret .= "$data[0]\tclade_marker_size\t5.0\n";
			$ret .= "$data[0]\tclade_marker_color\t" . $mc{$label} . "\n";
			$ret .= "$data[0]\tannotation_background_color\t" . $mc{$label} . "\n";
			$ret .= "$data[0]\tring_width\t1\t1.0\n";
			$ret .= "$data[0]\tring_color\t1\t" . $mc{$label} . "\n";
		} else {
			$ret .= "$data[0]\tclade_marker_size\t20.0\n";
                	$ret .= "$data[0]\tclade_marker_color\t" . "white" . "\n";

		}
	}
	close IN;

	return($ret);
}

