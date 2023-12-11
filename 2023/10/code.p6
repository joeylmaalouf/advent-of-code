#!/usr/bin/env perl6

say 'part 1: ' ~ get-distances('input.txt'.IO.lines.map(*.comb.Array)).values.max;
say 'part 2: ' ~ count-enclosed('input.txt'.IO.lines.map(*.comb.Array));

#| get the number of steps for any tile reachable from the starting point
sub get-distances (@tiles) {
	my %start = find-start(@tiles);
	@tiles[%start{'y'}][%start{'x'}] = %start{'pipe'};
	my %distances = (%start{'x'} ~ ',' ~ %start{'y'} => 0);
	# step in each of the 2 valid directions until we get back to the start
	# the distance for each tile is the lower of its 2 potential step counts
	for get-connections(%start{'pipe'}).List -> $connection {
		my %next = (
			'x' => %start{'x'},
			'y' => %start{'y'},
			'out-dir' => $connection,
		);
		my $steps = 0;
		repeat {
			%next = take-step(@tiles, %next{'x'}, %next{'y'}, %next{'out-dir'});
			++$steps;
			my $key = %next{'x'} ~ ',' ~ %next{'y'};
			%distances{$key} = min(%distances{$key}, $steps);
		} while %next{'x'} != %start{'x'} or %next{'y'} != %start{'y'};
	};
	return %distances;
};

#| get the starting pipe's coordinates and shape
sub find-start (@tiles) {
	my %start;
	for @tiles.kv -> $y, @row {
		for @row.kv -> $x, $tile {
			if $tile eq 'S' {
				my @connections;
				@connections.push('N') if $y > 0                && get-connections(@tiles[$y - 1][$x]).grep(get-opposite('N'));
				@connections.push('S') if $y < @tiles.elems - 1 && get-connections(@tiles[$y + 1][$x]).grep(get-opposite('S'));
				@connections.push('W') if $x > 0                && get-connections(@tiles[$y][$x - 1]).grep(get-opposite('W'));
				@connections.push('E') if $x < @row.elems - 1   && get-connections(@tiles[$y][$x + 1]).grep(get-opposite('E'));
				%start = (
					'x' => $x,
					'y' => $y,
					'pipe' => get-pipe-shape(@connections),
				);
			};
		};
	};
	return %start;
};

#| get the opposite direction for a given direction
sub get-opposite ($direction) {
	return %(
		'N' => 'S',
		'S' => 'N',
		'W' => 'E',
		'E' => 'W',
	){$direction};
};

#| get the pipe shape for a given set of connecting directions
sub get-pipe-shape (@directions) {
	return %(
		'NS' => '|',
		'EW' => '-',
		'EN' => 'L',
		'NW' => 'J',
		'SW' => '7',
		'ES' => 'F',
	){@directions.sort.join};
};

#| get the connecting directions for a given pipe shape
sub get-connections ($shape) {
	return %(
		'|' => ['N', 'S'],
		'-' => ['W', 'E'],
		'L' => ['N', 'E'],
		'J' => ['N', 'W'],
		'7' => ['W', 'S'],
		'F' => ['E', 'S'],
	){$shape};
};

#| get the results of taking a step in the given direction
sub take-step (@tiles, $x, $y, $direction) {
	my $nx = $x + %('N' => 0, 'S' => 0, 'W' => -1, 'E' => 1){$direction};
	my $ny = $y + %('N' => -1, 'S' => 1, 'W' => 0, 'E' => 0){$direction};
	my $in-dir = get-opposite($direction);
	return %(
		'x' => $nx,
		'y' => $ny,
		'out-dir' => get-connections(@tiles[$ny][$nx]).grep(* ne $in-dir).head,
	);
};

#| get the number of tiles enclosed by the pipe loop
sub count-enclosed (@tiles) {
	# traverse the path and note which tiles are part of the loop
	my %loop-tiles;
	my %start = find-start(@tiles);
	@tiles[%start{'y'}][%start{'x'}] = %start{'pipe'};
	my %next = (
		'x' => %start{'x'},
		'y' => %start{'y'},
		'out-dir' => get-connections(%start{'pipe'}).List.head,
	);
	repeat {
		%next = take-step(@tiles, %next{'x'}, %next{'y'}, %next{'out-dir'});
		%loop-tiles{%next{'x'} ~ ',' ~ %next{'y'}} = 1;
	} while %next{'x'} != %start{'x'} or %next{'y'} != %start{'y'};
	# then iterate through the tiles, changing whether we're within the loop each time we cross it
	# thank you /r/adventofcode for the hint that crossing the loop = toggling inside-ness
	my $enclosed = 0;
	for @tiles.kv -> $y, @row {
		# since we're iterating across horizontal rows, I'm pretty sure that we can define crossing the loop
		# as passing some number of part-of-loop tiles that include a north and a south direction (e.g. '|' or 'L--7')
		my $haveN = my $haveS = False;
		my $within = False;
		for @row.kv -> $x, $tile {
			if %loop-tiles{$x ~ ',' ~ $y} {
				my @connections = get-connections(@tiles[$y][$x]).List;
				$haveN = !$haveN if @connections.grep('N');
				$haveS = !$haveS if @connections.grep('S');
				if $haveN && $haveS {
					$within = !$within;
					$haveN = $haveS = False;
				};
			}
			elsif $within {
				# while inside the loop, we can count how many not-part-of-loop tiles we see until we cross back out of the loop
				++$enclosed;
			};
		};
	};
	return $enclosed;
};
