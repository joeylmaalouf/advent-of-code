#!/usr/bin/env perl6

my @lines = 'input.txt'.IO.lines;
say 'part 1: ' ~ sum-calib-values(@lines);
say 'part 2: ' ~ sum-calib-values(@lines, {
	'zero' => 0, 'one' => 1, 'two' => 2, 'three' => 3, 'four' => 4,
	'five' => 5, 'six' => 6, 'seven' => 7, 'eight' => 8, 'nine' => 9,
});

#| sum the calibration values parsed from each line
sub sum-calib-values (@lines, %replacements = {}) {
	return (get-calib-value($_, %replacements) for @lines).sum;
};

#| parse a calibration value from the line, accounting for any optional mapping beyond basic digits
sub get-calib-value ($line, %replacements) {
	my $pattern = '\d';
	$pattern ~= '||' ~ %replacements.keys.join('||') if %replacements;
	my @matches = $line.match(rx/(<$pattern>)/, :exhaustive);
	my $first = %replacements{@matches.head} // @matches.head;
	my $last = %replacements{@matches.tail} // @matches.tail;
	return ($first ~ $last).Int;
};
