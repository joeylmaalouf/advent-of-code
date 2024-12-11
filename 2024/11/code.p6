#!/usr/bin/env perl6

my @stones = 'input.txt'.IO.slurp.trim.split(rx/\s+/);
# shoutout to the /r/adventofcode hint that order doesn't matter at all
# since that means we can store counts instead of a list of all the values
# so instead of going through every value (even with the caching I had set up),
# we can just step through unique values
my %stones; @stones.map({ %stones{$_}++ });
say 'part 1: ' ~ count-after-blinks(%stones.clone, 25);
say 'part 2: ' ~ count-after-blinks(%stones.clone, 75);

#| counts how many stones we have after blinking
sub count-after-blinks (%stones, $steps) {
    my %new;
    for 0 ^.. $steps -> $step {
        for %stones.kv -> $stone, $count {
            for get-next($stone) -> $next {
                %new{$next} += $count;
            };
        };
        %stones = %new.clone;
        %new = ();
    };
    return %stones.values.sum;
};

#| gets the next step in how the stones change on blink
sub get-next ($stone) {
    if $stone == 0 { return 1; };
    if $stone.chars % 2 == 0 { return (
        $stone.substr(0 ..^ $stone.chars / 2).Int,
        $stone.substr($stone.chars / 2 .. *).Int,
    ).Slip; };
    return $stone * 2024;
};
