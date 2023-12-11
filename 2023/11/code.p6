#!/usr/bin/env perl6

my @galaxies = parse-galaxies('input.txt'.IO.lines.map(*.comb));
say 'part 1: ' ~ get-distances(expand-universe(@galaxies, 2)).sum;
say 'part 2: ' ~ get-distances(expand-universe(@galaxies, 1000000)).sum;

#| get the list of galaxies
sub parse-galaxies (@universe) {
	my @galaxies;
	for @universe.kv -> $y, @row {
		for @row.kv -> $x, $space {
			@galaxies.push(($x, $y)) if $space eq '#';
		};
	};
	return @galaxies;
};

#| duplicate any rows/columns that have no galaxies in them
sub expand-universe (@galaxies, $multiplier) {
	my @expanded;
	my @occupied-cols = @galaxies.map(*[0]).unique.sort;
	my @occupied-rows = @galaxies.map(*[1]).unique.sort;
	for @galaxies -> @galaxy {
		(my $x, my $y) = @galaxy;
		# each galaxy should be shifted over based on how many empty rows/columns before it were expanded
		my $empty-cols = $x - @occupied-cols.grep(* < $x).elems;
		my $empty-rows = $y - @occupied-rows.grep(* < $y).elems;
		@expanded.push((
			$x + $empty-cols * ($multiplier - 1),
			$y + $empty-rows * ($multiplier - 1),
		));
	};
	return @expanded;
};

#| calculate how far away all of the galaxies are
sub get-distances (@galaxies) {
	my @distances;
	for 0 .. @galaxies.elems - 1 -> $i {
		for $i + 1 .. @galaxies.elems - 1 -> $j {
			@distances.push(
				abs(@galaxies[$i][0] - @galaxies[$j][0]) +
				abs(@galaxies[$i][1] - @galaxies[$j][1])
			);
		};
	};
	return @distances;
};
