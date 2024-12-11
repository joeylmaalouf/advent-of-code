#!/usr/bin/env perl6

my @stones = 'input.txt'.IO.slurp.trim.split(rx/\s+/);
say 'part 1: ' ~ count-stones-after-blinks(@stones.clone, 25).elems;
say 'part 2: ' ~ count-stones-after-blinks(@stones.clone, 75).elems;

#| counts how many stones we have after blinking
sub count-stones-after-blinks (@stones, $blinks, %cache = {}) {
    return @stones if $blinks == 0;
    my @new_stones = @stones.map({ get-next($_) }).map({
        my $next_blink = $blinks - 1;
        if %cache{$(@$_, $next_blink)}:exists {
            %cache{$(@$_, $next_blink)}.Slip
        }
        else {
            count-stones-after-blinks(@$_, $next_blink, %cache).Slip
        }
    });
    %cache{$(@stones, $blinks)} = @new_stones.clone;
    return @new_stones;
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
