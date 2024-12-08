#!/usr/bin/env perl6

my @equations = 'input.txt'.IO.slurp.trim.lines.map({ $_.split(rx/\:?\s+/) });
say 'part 1: ' ~ @equations.grep({ can-validate($_[1 .. *], $_[0]) }).map({ $_[0] }).sum;
say 'part 2: ' ~ @equations.grep({ can-validate($_[1 .. *], $_[0], True) }).map({ $_[0] }).sum;

#| check whether the given components can become the given result
sub can-validate (@components, $result, $can_concat = False) {
    # base case: if there's only one component left, see if it's our target result
    # otherwise, combine the first two components in various ways and recurse
    # we can also short-circuit early if we've passed the target value,
    # since addition/multiplication/concatenation will all only ever increase the value
    if @components.elems == 1 { return @components[0] == $result; };
    if @components[0] > $result { return False; };
    my @rest = @components[2 .. *];
    return can-validate((@components[0] + @components[1], @rest).flat, $result, $can_concat)
        || can-validate((@components[0] * @components[1], @rest).flat, $result, $can_concat)
        || ($can_concat && can-validate((@components[0] ~ @components[1], @rest).flat, $result, $can_concat));
};
