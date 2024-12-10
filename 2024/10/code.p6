#!/usr/bin/env perl6

my @heights = 'input.txt'.IO.slurp.trim.lines.map(*.comb);
say 'part 1: ' ~ get-topography(@heights).values.map({ $_.get-score(0, 9) }).sum;
say 'part 2: ' ~ get-topography(@heights).values.map({ $_.get-rating(0, 9) }).sum;

class Node {
    has $.y;
    has $.x;
    has $.height;
    has @.adjacent;
    # calculate this node's score
    method get-score ($start, $goal, $step = 1, @reached = []) {
        # if we aren't starting at the start value, the score is 0
        return 0 if $!height != $start;
        # the score counts how many unique positions we can reach that have the goal value
        my $position = $!y ~ ',' ~ $!x;
        if $!height == $goal && !@reached.grep($position) {
            @reached.push($position);
            return 1;
        };
        # we'll only consider routes through nodes that consistently increment by the step value
        return @!adjacent.grep({
            $_.height == $!height + $step
        }).map({
            $_.get-score($start + $step, $goal, $step, @reached)
        }).sum;
    };
    # calculate this node's rating
    method get-rating ($start, $goal, $step = 1, $path = '', @routes = []) {
        # if we aren't starting at the start value, the score is 0
        return 0 if $!height != $start;
        # the score counts how many unique routes we can take to get to the goal value
        my $route = $path ~ $!y ~ ',' ~ $!x ~ ';';
        if $!height == $goal && !@routes.grep($route) {
            @routes.push($route);
            return 1;
        };
        # we'll only consider routes through nodes that consistently increment by the step value
        return @!adjacent.grep({
            $_.height == $!height + $step
        }).map({
            $_.get-rating($start + $step, $goal, $step, $route, @routes)
        }).sum;
    };
};

#| get a map of the node values at each coordinate
sub get-topography (@heights) {
    my %map;
    for ((0 ..^ @heights.elems) X (0 ..^ @heights[0].elems)) -> ($y, $x) {
        %map{$y ~ ',' ~ $x} = Node.new(y => $y, x => $x, height => @heights[$y][$x]);
    };
    for %map.keys -> $key {
        my ($y, $x) = $key.split(rx/\,/);
        for (
            ($y - 1, $x), # N
            ($y, $x + 1), # E
            ($y + 1, $x), # S
            ($y, $x - 1), # W
        ) -> ($other_y, $other_x) {
            my $other_key = $other_y ~ ',' ~ $other_x;
            %map{$key}.adjacent.push(%map{$other_key}) if %map{$other_key}:exists;
        };
    };
    return %map;
};
