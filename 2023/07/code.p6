#!/usr/bin/env perl6

my @hands = parse-hands('input.txt'.IO.lines);
say 'part 1: ' ~ get-winnings(@hands, False).sum;
say 'part 2: ' ~ get-winnings(@hands, True).sum;

#| get the list of hands
sub parse-hands (@lines) {
	return @lines.map: {
		my @parts = $_.split(rx/\s/);
		{
			'cards' => @parts[0].comb.List,
			'bid' => @parts[1].Int,
		}
	};
};

#| get the list of hand winnings
sub get-winnings (@hands, $use-joker) {
	my @sorted = @hands.sort(-> $a, $b { compare-hands($a, $b, $use-joker) });
	return @sorted.keys.map: { ($_ + 1) * @sorted[$_]{'bid'} };
};

#| compare two given hands
sub compare-hands (%a, %b, $use-joker) {
	my @a = %a{'cards'}.List;
	my @b = %b{'cards'}.List;
	# compare the strengths of the hand types
	my $compare = get-hand-strength(@a, $use-joker) <=> get-hand-strength(@b, $use-joker);
	return $compare if $compare;
	# if they're the same, compare the strengths of the individual cards
	for 0 .. (@a.elems - 1) -> $i {
		$compare = get-card-strength(@a[$i], $use-joker) <=> get-card-strength(@b[$i], $use-joker);
		return $compare if $compare;
	}
	# if they're still the same, then they're identical
	return Order::Same;
};

#| get the strength of the given cards' hand type
sub get-hand-strength (@cards, $use-joker) {
	my %counts; ++%counts{$_} for @cards;
	my $strength = {
		'1 1 1 1 1' => 1, # high card
		'1 1 1 2' => 2, # one pair
		'1 2 2' => 3, # two pair
		'1 1 3' => 4, # three of a kind
		'2 3' => 5, # full house
		'1 4' => 6, # four of a kind
		'5' => 7, # five of a kind
	}{%counts.values.sort.Str};
	if $use-joker {
		# if we have jokers being be the optimal card, we should adjust the strength
		# depending on what hand type we currently have and how many jokers we have to work with
		$strength = {
			1 => { 0 => 1, 1 => 2, },
			2 => { 0 => 2, 2 => 4, 1 => 4, },
			3 => { 0 => 3, 2 => 6, 1 => 5, },
			4 => { 0 => 4, 3 => 6, 1 => 6, },
			5 => { 0 => 5, 3 => 7, 2 => 7, },
			6 => { 0 => 6, 4 => 7, 1 => 7, },
			7 => { 0 => 7, 5 => 7, },
		}{$strength}{%counts{'J'} || 0};
	}
	return $strength;
};

#| get the strength of a given card
sub get-card-strength ($c, $use-joker) {
	return ($use-joker ?? 'J23456789TQKA' !! '23456789TJQKA').index($c);
};
