#!/usr/bin/env perl6

my @numbers = parse-numbers('input.txt'.IO.lines);
say 'part 1: ' ~ filter-part-nums(@numbers).sum;
say 'part 2: ' ~ get-gear-ratios(@numbers).sum;

#| get the positions and values of all part numbers in the engine, as well as their adjacent symbols
sub parse-numbers (@lines) {
	my @numbers;
	for @lines.kv -> $row, $line {
		my $start = -1;
		for $line.comb.kv -> $col, $char {
			# if we hit a number, keep track of where we started
			if $char ~~ rx/\d/ {
				$start = $col if $start == -1;
			}
			# if we hit anything else and we were tracking a number, store its data
			elsif $start > -1 {
				@numbers.push({ 'row' => $row, 'col' => $start, 'value' => substr($line, $start .. $col - 1).Int });
				$start = -1;
			}
		}
		# if we hit the end of the line and we were tracking a number, store its data
		@numbers.push({ 'row' => $row, 'col' => $start, 'value' => substr($line, $start .. $line.chars - 1).Int }) if $start > -1;
	}
	for @numbers -> $number {
		# start a row/col earlier and end a row/col later so we're looking at the surrounding chars
		for max($number{'row'} - 1, 0) .. min($number{'row'} + 1, @lines.elems - 1) -> $row {
			my @line = @lines[$row].comb;
			for max($number{'col'} - 1, 0) .. min($number{'col'} + $number{'value'}.Str.chars, @line.elems - 1) -> $col {
				if @line[$col] ~~ rx/<[ @ # $ % & * \- + = / ]>/ {
					$number{'symbols'}{$/}.push(($row ~ ',' ~ $col));
				}
			}
		}
	}
	return @numbers;
};

#| get the values of the part numbers that border any symbol
sub filter-part-nums (@numbers) {
	return @numbers.grep({ $_{'symbols'} }).map({ $_{'value'} });
};

#| get the products of the part numbers where two of them border the same *
sub get-gear-ratios (@numbers) {
	my %gears;
	for @numbers -> $number {
		if $number{'symbols'}{'*'}:exists {
			for $number{'symbols'}{'*'} -> $pos {
				%gears{$pos}.push($number{'value'});
			}
		}
	}
	return %gears.values.grep({ $_.elems == 2 }).map({ [*] $_.Array });
};
