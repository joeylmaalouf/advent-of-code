#!/usr/bin/env perl6

my @numbers = 'input.txt'.IO.slurp.trim.split(rx/\s+/);
my @list1 = @numbers[0, 2 ... *].sort;
my @list2 = @numbers[1, 3 ... *].sort;
say 'part 1: ' ~ get-distance(@list1, @list2);
say 'part 2: ' ~ get-similarity(@list1, @list2);

#| gets the distance between two lists by summing the differences between their values
sub get-distance (@list1, @list2) {
    return ((@list1 Z @list2).map: {
        ($_[0] - $_[1]).abs
    }).sum;
};

#| gets the similarity between two lists by checking repetition counts
sub get-similarity (@list1, @list2) {
    my %occurrences;
    for @list2 -> $value {
        ++%occurrences{$value};
    }
    return (@list1.map: {
        $_ * (%occurrences{$_} || 0)
    }).sum;
};
