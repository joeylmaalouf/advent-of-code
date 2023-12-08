#!/usr/bin/env perl6

my %network = parse-network('input.txt'.IO.slurp);
my %nodes = %network{'nodes'};
my @instructions = %network{'instructions'}.List;
say 'part 1: ' ~ find-exit(%nodes, @instructions, 'AAA', 'ZZZ$'){'steps'};
say 'part 2: ' ~ count-simultaneous-steps(%nodes, @instructions, 'A$', 'Z$');

#| get the network layout and instructions
sub parse-network ($text) {
	my @sections = $text.split(rx/\n\n/);
	return {
		'instructions' => @sections[0].comb.List,
		'nodes' => @sections[1].split(rx/\n/).map({
			my @parts = ($_ ~~ m:g/(\w+)/).map(*.Str);
			@parts[0] => { 'L' => @parts[1], 'R' => @parts[2], }
		}).Hash,
	};
};

#| follow the given start until it reaches any end match
sub find-exit (%nodes, @instructions, $start, $end-match) {
	my $position = $start;
	my $instruction-index = 0;
	my $steps = 0;
	# a normal while loop would stop immediately if we're already there,
	# but we want to execute at least once so we can find how many steps
	# it takes to cycle back to where we are (for the simultaneous part)
	repeat {
		$position = %nodes{$position}{@instructions[$instruction-index]};
		$instruction-index = ($instruction-index + 1) % @instructions.elems;
		++$steps;
	} while !($position ~~ m/<$end-match>/);
	return {
		'steps' => $steps,
		'position' => $position,
	};
};

# #| follow the start matches until they all simultaneously reach any end matches
sub count-simultaneous-steps (%nodes, @instructions, $start-match, $end-match) {
	my @positions = %nodes.keys.grep({ m/<$start-match>/ });
	my @cycle-lengths = @positions.map: {
		# once we find an exit for each start, we just need to figure out how many
		# steps it takes for each alternate self to be on those exits at the same time
		my $exit = find-exit(%nodes, @instructions, $_, $end-match){'position'};
		# thank you /r/adventofcode for the hint that this input is guaranteed to create cycles
		# so each alternate self ends up looping around after some number of steps
		find-exit(%nodes, @instructions, $exit,  '^' ~ $exit ~ '$'){'steps'}
	};
	# the least common multiple is the point at which they all finish a cycle on the same step
	return [lcm] @cycle-lengths;
};
