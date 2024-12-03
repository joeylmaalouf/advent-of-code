#!/usr/bin/env perl6

my @instructions = 'input.txt'.IO.slurp.trim ~~ m:g/(do)(n\'t)?\(\)|(mul)\((\d**1..3)\,(\d**1..3)\)/;
# 0 is either 'do' (in which case 1 is 'n\'t' or undef) or 'mul' (in which case 1 and 2 are numbers)

say 'part 1: ' ~ @instructions.grep({ $_[0] eq 'mul' }).map({ $_[1] * $_[2] }).sum;

my $enabled = True;
say 'part 2: ' ~ @instructions.grep({
    if $_[0] eq 'do' { $enabled = !defined $_[1] };
    $enabled && $_[0] eq 'mul'
}).map({ $_[1] * $_[2] }).sum;
