#!/usr/bin/env perl6

my @letters = 'input.txt'.IO.slurp.trim.lines;
say 'part 1: ' ~ count-matches(@letters.clone, 'XMAS');
say 'part 2: ' ~ count-xmatches(@letters.clone, 'M', 'A', 'S');

#| count how many occurrences the given word search block has of the given string (or its reverse)
sub count-matches (@letters, $string) {
    return get-rotated-views(@letters).map({
        $_.indices($string).elems
        + $_.indices($string.flip).elems
    }).sum;
};

#| get the lines representing the letter block at various rotations
sub get-rotated-views (@letters) {
    my @lines;
    # rotated 0 degrees, to find W-E and reverse
    @lines.append(@letters);
    # rotated 90 degrees, to find N-S and reverse
    @letters = @letters.map({ $_.comb });
    my $max_x = @letters[0].elems - 1;
    my $max_y = @letters.elems - 1;
    my $line;
    for $max_x ... 0 -> $x {
        $line = '';
        for 0 ... $max_y -> $y {
            $line ~= @letters[$y][$x];
        }
        @lines.push($line);
    }
    # rotated 45 degrees, to find NW-SE and reverse
    my @starts = ($max_x ... 0).map({ ($_, 0) });
    @starts.append((1 ... $max_y).map({ (0, $_) }));
    for @starts -> @start {
        my ($x, $y) = @start;
        $line = '';
        while $x <= $max_x && $y <= $max_y {
            $line ~= @letters[$y][$x];
            $x++; $y++;
        };
        @lines.push($line);
    };
    # rotated 135 degrees, to find NE-SW and reverse
    @starts = ($max_y ... 0).map({ ($max_x, $_) });
    @starts.append(($max_x - 1 ... 0).map({ ($_, 0) }));
    for @starts -> @start {
        my ($x, $y) = @start;
        $line = '';
        while 0 <= $x && $y <= $max_y {
            $line ~= @letters[$y][$x];
            $x--; $y++;
        };
        @lines.push($line);
    };
    return @lines;
};

#| count how many occurrences the given word search block has of the given characters in an x shape
sub count-xmatches (@letters, $char_l, $char_m, $char_r) {
    @letters = @letters.map({ $_.comb });
    # we'll search for the middle character through the whole letter block (minus the edges)
    # and check whether the characters at (-1, -1) (-1, +1) (+1, -1) (+1, +1) around each M are
    # LLRR/LRLR/RRLL/RLRL (but not LRRL/RLLR, since that would have the same letter across the X)
    my @valid = (
        ($char_l, $char_l, $char_r, $char_r).join,
        ($char_l, $char_r, $char_l, $char_r).join,
        ($char_r, $char_r, $char_l, $char_l).join,
        ($char_r, $char_l, $char_r, $char_l).join,
    );
    return ((1 .. @letters.elems - 2) X (1 .. @letters[0].elems - 2)).grep({
        @letters[$_[0]][$_[1]] eq $char_m
        && @valid.grep((
            @letters[$_[0] - 1][$_[1] - 1],
            @letters[$_[0] - 1][$_[1] + 1],
            @letters[$_[0] + 1][$_[1] - 1],
            @letters[$_[0] + 1][$_[1] + 1]
        ).join)
    }).elems;
};
