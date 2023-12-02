#!/usr/bin/env perl6

my %games = parse-games('input.txt'.IO.lines);
say 'part 1: ' ~ sum-possible-ids(%games, { 'red' => 12, 'green' => 13, 'blue' => 14 });
say 'part 2: ' ~ sum-needed-power(%games);

sub parse-games (@lines) {
	my %games;
	for @lines -> $line {
		my @parts = $line.split(': ');
		my $game-id = (@parts.head ~~ m/Game\s(\d+)/).list[0].Int;
		my %maximums;
		my @sets = @parts.tail ~~ m:g/(\d+)\s(\w+)/;
		for @sets -> $set {
			my $number = $set.list[0].Int;
			my $color = $set.list[1];
			if %maximums{$color}:!exists || $number > %maximums{$color} {
				%maximums{$color} = $number;
			}
		}
		%games{$game-id} = %maximums;
	}
	return %games;
};

sub sum-possible-ids (%games, %contents) {
	return (%games.keys.grep: {
		my $possible = True;
		for %contents.keys -> $color {
			$possible = False if %games{$_}{$color}:exists && %games{$_}{$color} > %contents{$color};
		}
		$possible
	}).sum;
}

sub sum-needed-power (%games) {
	return (%games.values.map: {
		my $product = 1;
		for $_.values -> $value {
			$product *= $value;
		}
		$product
	}).sum;
}
