#!/usr/bin/env perl6

my @cards = parse-cards('input.txt'.IO.lines);
say 'part 1: ' ~ score-cards(@cards).sum;
say 'part 2: ' ~ count-cards(@cards).sum;

#| get the number lists on each card
sub parse-cards (@lines) {
	my @cards = @lines.map: {%(
		'winning' => (($_ ~~ rx/\:(<[\s\d]>+)/).Str ~~ m:g/(\d+)/).map({ .Int }),
		'actual' => (($_ ~~ rx/\|(<[\s\d]>+)/).Str ~~ m:g/(\d+)/).map({ .Int }),
	)};
	$_{'overlap'} = ($_{'winning'} (&) $_{'actual'}).elems for @cards;
	return @cards;
};

#| calculate the score for each card
sub score-cards (@cards) {
	return @cards.map: { (2 ** ($_{'overlap'} - 1)).floor };
};

#| count how many of each card we end up with
sub count-cards (@cards) {
	my @counts = (1 for @cards);
	for @cards.kv -> $i, $card {
		if $card{'overlap'} {
			for $i + 1 .. $i + $card{'overlap'} -> $j {
				@counts[$j] += @counts[$i];
			}
		}
	}
	return @counts;
};
