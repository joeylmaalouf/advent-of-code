#!/usr/bin/env perl6

my @stones = 'input.txt'.IO.slurp.trim.split(rx/\s+/);
say 'part 1: ' ~ count-stones-after-blinks(@stones.clone, 25);
say 'part 2: ' ~ count-stones-after-blinks(@stones.clone, 75);

#| count how many stones we have after blinking
sub count-stones-after-blinks (@stones, $steps) {
    my %cache;
    for 0 ..^ $steps -> $blink {
        @stones = @stones.map({
            %cache{$_} = get-next-step($_) unless %cache{$_}:exists;
            %cache{$_}
        });
    };
    return @stones.elems;
};

#| gets the next step in how the stones change on blink
sub get-next-step ($stone) {
    if $stone == 0 { return 1; };
    if $stone.chars % 2 == 0 { return (
        $stone.substr(0 ..^ $stone.chars / 2).Int,
        $stone.substr($stone.chars / 2 .. *).Int,
    ).Slip; };
    return $stone * 2024;
};

# TODO: even beyond the cache, I need some sort of additional optimization for part 2
# maybe take the initial set and do each in parallel? since they don't rely on each other in any way
# or is there some sort of formula I can use instead of actually stepping through each stone?
