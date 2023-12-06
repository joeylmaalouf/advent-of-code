#!/usr/bin/env perl6

my $input = 'input.txt'.IO.slurp;
my @seeds = parse-seeds($input);
my %maps = parse-maps($input);
my @categories = (
	'seed-to-soil',
	'soil-to-fertilizer',
	'fertilizer-to-water',
	'water-to-light',
	'light-to-temperature',
	'temperature-to-humidity',
	'humidity-to-location',
);
say 'part 1: ' ~ get-seed-locations(@seeds, %maps, @categories).min;
say 'part 2: ' ~ get-seed-range-locations(@seeds, %maps, @categories).min;

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

#| get the location for each of the seeds
sub get-seed-locations (@seeds, %maps, @categories) {
	return @seeds.map: { seed-to-location($_, %maps, @categories) };
}

#| apply each of the mappings to the given value in order
sub seed-to-location ($seed, %maps, @categories) {
	my $value = $seed;
	for @categories -> $category {
		$value = get-mapped-value($value, %maps{$category});
	};
	return $value;
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

#| get the locations for each of the seed ranges
sub get-seed-range-locations (@seeds, %maps, @categories) {
	my @seed-ranges;
	# turn the inputs into actual ranges
	for @seeds -> $start, $length {
		@seed-ranges.push({
			'src-start' => $start,
			'length' => $length,
		});
	}
	for @categories -> $category {
		# once we enter a new category, we want all seed ranges to be available for mapping again
		@seed-ranges = @seed-ranges.map: { $_{'mapped'} = 0; $_ };
		for %maps{$category}.Array -> %mapping-range {
			my @new-seed-ranges;
			for @seed-ranges -> %seed-range {
				# if we've already mapped this range in this category, we don't want to keep checking it
				if %seed-range{'mapped'} {
					@new-seed-ranges.push(%seed-range);
				}
				else {
					# split any seed ranges that partially overlap with the mapping ranges
					# into ones that are fully out of range and fully in range
					my @split-ranges = split-and-map-range(%seed-range, %mapping-range);
					@new-seed-ranges.append(@split-ranges);
				}
			}
			@seed-ranges = @new-seed-ranges;
		}
	}
	return @seed-ranges.map: { $_{'src-start'} };
};

#| split a seed range that may overlap with the mapping range into chunks that are fully inside (and mapped) or outside
sub split-and-map-range (%seeds, %mapping) {
	my $seeds-start = %seeds{'src-start'};
	my $seeds-length = %seeds{'length'};
	my $seeds-end = %seeds{'src-start'} + %seeds{'length'} - 1;
	my $mapping-start = %mapping{'src-start'};
	my $mapping-length = %mapping{'length'};
	my $mapping-end = %mapping{'src-start'} + %mapping{'length'} - 1;
	# we'll split differently based on how the ranges overlap
	if ($seeds-start < $mapping-start) {
		if ($seeds-end < $mapping-start) {
			# seeds < mapping, no overlap
			return (%seeds,);
		}
		elsif ($seeds-end <= $mapping-end) {
			# seeds <= mapping, some overlap
			return (
				{
					'src-start' => $seeds-start,
					'length' => $mapping-start - $seeds-start,
				},
				{
					'src-start' => get-mapped-value($mapping-start, (%mapping,)),
					'length' => ($seeds-end + 1) - $mapping-start,
					'mapped' => 1,
				},
			);
		}
		elsif ($seeds-end > $mapping-end) {
			# seeds contains mapping, total overlap
			return (
				{
					'src-start' => $seeds-start,
					'length' => $mapping-start - $seeds-start,
				},
				{
					'src-start' => get-mapped-value($mapping-start, (%mapping,)),
					'length' => $mapping-length,
					'mapped' => 1,
				},
				{
					'src-start' => ($mapping-end + 1),
					'length' => ($seeds-end + 1) - ($mapping-end + 1),
				},
			);
		}
	}
	elsif ($seeds-start >= $mapping-start) {
		if ($seeds-start > $mapping-end) {
			# seeds > mapping, no overlap
			return (%seeds,);
		}
		elsif ($seeds-end <= $mapping-end) {
			# mapping contains seeds, total overlap
			return (
				{
					'src-start' => get-mapped-value($seeds-start, (%mapping,)),
					'length' => $seeds-length,
					'mapped' => 1,
				},
			);
		}
		elsif ($seeds-end > $mapping-end) {
			# seeds >= mapping, some overlap
			return (
				{
					'src-start' => get-mapped-value($seeds-start, (%mapping,)),
					'length' => ($mapping-end + 1) - $seeds-start,
					'mapped' => 1,
				},
				{
					'src-start' => ($mapping-end + 1),
					'length' => ($seeds-end + 1) - ($mapping-end + 1),
				},
			);
		}
	}
};
