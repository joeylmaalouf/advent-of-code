#!/usr/bin/env perl6

my $input = 'input.txt'.IO.slurp;
my @seeds = parse-seeds($input);
my %maps = parse-maps($input);
say 'part 1: ' ~ get-seed-locations(@seeds, %maps).min;
say 'part 2: ' ~ get-seed-locations(ranges-to-values(@seeds), %maps).min;

#| get the list of seeds
sub parse-seeds ($text) {
	return (($text ~~ rx/seeds\:(<[\s\d]>+)/) ~~ m:g/(\d+)/).map({ .Int });
};

#| get the mappings for each category
sub parse-maps ($text) {
	return $text.split(rx/\n\n/)[1 .. *].map: {
		my ($category, $ranges) = $_.split(rx/\smap\:\n/);
		$category => $ranges.split(rx/\n/).map: {
			my $parts = $_.split(rx/\s/);
			{
				'dst-start' => $parts[0],
				'src-start' => $parts[1],
				'length' => $parts[2],
			}
		}
	};
};

#| apply the mappings in order to get to locations from seeds
sub get-seed-locations (@seeds, %maps) {
	return @seeds.map: {
		my $value = $_;
		for (
			'seed-to-soil',
			'soil-to-fertilizer',
			'fertilizer-to-water',
			'water-to-light',
			'light-to-temperature',
			'temperature-to-humidity',
			'humidity-to-location',
		) -> $category {
			$value = get-mapped-value($value, %maps{$category});
		}
		$value
	};
};

#| get the shifted value if it exists in the given ranges
sub get-mapped-value ($value, @ranges) {
	for @ranges -> %range {
		if %range{'src-start'} <= $value && $value < %range{'src-start'} + %range{'length'} {
			return %range{'dst-start'} + $value - %range{'src-start'};
		}
	}
	return $value;
};

#| convert a list of ranges to flattened values
sub ranges-to-values (@ranges) {
	my @values;
	for @ranges -> $start, $length {
		@values.append($start .. $start + $length - 1);
	}
	return @values;
};
