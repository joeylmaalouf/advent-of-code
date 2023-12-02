#!/usr/bin/env perl6

my %games = parse-games('input.txt'.IO.lines);
say 'part 1: ' ~ sum-possible-ids(%games, { 'red' => 12, 'green' => 13, 'blue' => 14, });
say 'part 2: ' ~ sum-needed-power(%games);

#| keep track of the maximum number of cubes of each color shown in each game
sub parse-games (@lines) {
	my %games;
	for @lines -> $line {
		my $game-id = ($line ~~ m/Game\s(\d+)/)[0].Int;
		my @sets = $line ~~ m:g/(\d+)\s(\w+)/;
		my %maximums;
		for @sets -> $set {
			%maximums{$set[1]} = max(%maximums{$set[1]}, $set[0].Int);
		}
		%games{$game-id} = %maximums;
	}
	return %games;
};

#| sum the game IDs of all the games where the bag contains enough of each color cube
sub sum-possible-ids (%games, %bag) {
	return (%games.keys.grep: {
		my %game = %games{$_};
		(%game.keys.map: {
			%bag{$_}:exists && %bag{$_} >= %game{$_}
		}).reduce: &infix:<&>
	}).sum;
}

#| sum the power values (products of the required cube counts) calculated from each game
sub sum-needed-power (%games) {
	return (%games.values.map: { [*] $_.values }).sum;
}
