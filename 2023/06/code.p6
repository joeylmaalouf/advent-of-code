#!/usr/bin/env perl6

my @lines = 'input.txt'.IO.lines;
say 'part 1: ' ~ get-margin-of-error(parse-races(@lines));
say 'part 2: ' ~ get-margin-of-error(parse-races(remove-whitespace(@lines)));

#| join the race numbers together for parsing as a single race
sub remove-whitespace (@lines) {
	return @lines.map({ $_.subst(rx/\s/, '', :g) });
};

#| get the list of race times and distances
sub parse-races (@lines) {
	my @times = @lines[0] ~~ m:g/(\d+)/;
	my @distances = @lines[1] ~~ m:g/(\d+)/;
	return (0 .. @times.elems - 1).map({%(
		'time' => @times[$_].Int,
		'distance' => @distances[$_].Int,
	)});
};

#| get the product of the number of ways to beat each record
sub get-margin-of-error (@races) {
	return [*] @races.map(&get-record-timing-count);
};

#| get the number of button-holding durations that would beat the race's record
sub get-record-timing-count (%race) {
	# return (0 .. %race{'time'}).map({ $_ * (%race{'time'} - $_) }).grep({ $_ > %race{'distance'}}).elems;
	for 0 .. %race{'time'} -> $i {
		if $i * (%race{'time'} - $i) > %race{'distance'} {
			return (%race{'time'} + 1) - ($i * 2);
		}
	}
};
