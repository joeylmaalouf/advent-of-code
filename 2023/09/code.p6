#!/usr/bin/env perl6

my @histories = parse-histories('input.txt'.IO.lines);
my @predictions = @histories.map(&predict-values);
say 'part 1: ' ~ @predictions.map(*{'next'}).sum;
say 'part 2: ' ~ @predictions.map(*{'previous'}).sum;

#| get the list of value histories
sub parse-histories (@lines) {
	return @lines.map: { $_.split(rx/\s/).map(*.Int).Array };
};

#| predict the previous and next values for a given value history
sub predict-values (@history) {
	my @steps-forwards;
	my @steps-backwards;
	my @differences = @history;
	while (@differences.map(* != 0).any) {
		for @differences.kv -> $i, $difference {
			@differences[$i] = @differences[$i + 1] - @differences[$i] if $i < @differences.elems - 1;
		};
		@differences.pop;
		@steps-backwards.push(@differences.head);
		@steps-forwards.push(@differences.tail);
	};
	return {
		'previous' => @history.head - @steps-backwards.reverse.reduce(-> $x, $n { $n - $x }), # we need [-] but with the operands flipped
		'next' => @history.tail + @steps-forwards.sum,
	};
};
