#!/usr/bin/env perl6

my ($rules, $updates) = 'input.txt'.IO.slurp.trim.split(rx/\n\n/);
my %rules;
for $rules.lines.map({ $_.split(rx/\|/) }) -> @rule {
    %rules{'FOLLOWS'}{@rule[0]}.append(@rule[1]);
    %rules{'LEADS'}{@rule[1]}.append(@rule[0]);
};
my @updates = $updates.lines.map({ $_.split(rx/\,/) });
say 'part 1: ' ~ @updates.grep({ is-ordered-correctly(%rules, $_) }).map({ $_[* / 2] }).sum;
say 'part 2: ' ~ @updates.grep({ !is-ordered-correctly(%rules, $_) }).map({ get-fixed-update(%rules, $_.Array) }).map({ $_[* / 2] }).sum;

#| check whether an update is ordered correctly
sub is-ordered-correctly (%rules, @update) {
    my $index = 0;
    for @update -> $page {
        # look at all of the pages that come before this one in the update
        # and fail if any of the pages that must come after this one are there
        if @update[0 ..^ $index] (&) %rules{'FOLLOWS'}{$page} { return False; }
        $index++;
    };
    return True;
};

#| reorder an update to follow the rules
sub get-fixed-update (%rules, @update) {
    repeat {
        my $index = 0;
        for @update -> $page {
        # look at all of the pages that come after this one in the update
        # and adjust if any of the pages that must come before this one are there
            if @update[$index ^.. *] (&) %rules{'LEADS'}{$page} {
                @update = (@update[0 ..^ $index], @update[$index ^.. *], $page).flat; # move the $page from $index to the end
                last; # recheck correctness right away
            }
            $index++;
        };
    } while !is-ordered-correctly(%rules, @update);
    return @update;
};
