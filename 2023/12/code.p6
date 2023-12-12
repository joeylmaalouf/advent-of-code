#!/usr/bin/env perl6

say 'part 1: ' ~ parse-gear-records('input.txt'.IO.lines, 1).map(&get-valid-arrangements).flat.elems;
say 'part 2: ' ~ parse-gear-records('input.txt'.IO.lines, 5).map(&get-valid-arrangements).flat.elems;
# TODO: math solution instead of brute force solution so part 2 solves in reasonable time

#| parse each gear condition template and its corresponding group sizes
sub parse-gear-records (@lines, $multiplier) {
	return @lines.map: {
		my @parts = $_.split(rx/\s/);
		@parts[0] = (@parts[0] ~ '?') x ($multiplier - 1) ~ @parts[0];
		@parts[1] = (@parts[1] ~ ',') x ($multiplier - 1) ~ @parts[1];
		%(
			'template' => @parts[0].comb.List,
			'groups' => @parts[1].split(rx/\,/).map(*.Int).List,
		);
	};
};

#| get the valid arrangements for the given gear condition record
sub get-valid-arrangements (%record) {
	return get-all-arrangements('', %record{'template'}.Array).grep: {
		# get the actual group sizes for each possible layout
		# and compare them against the given group sizes
		($_ ~~ m:g/(\#+)/).map(*.chars).List eqv %record{'groups'}
	};
};

#| recursively generate all of the possible layouts for the given gear group template
sub get-all-arrangements ($layout, @template) {
	if @template {
		my @arrangements;
		my $gear = @template.shift;
		if $gear eq '?' {
			@arrangements.append(get-all-arrangements($layout ~ '.', @template.clone));
			@arrangements.append(get-all-arrangements($layout ~ '#', @template.clone));
		}
		else {
			@arrangements.append(get-all-arrangements($layout ~ $gear, @template.clone));
		};
		return @arrangements;
	}
	else {
		return $layout;
	};
};
