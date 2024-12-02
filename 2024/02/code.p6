#!/usr/bin/env perl6

my @reports = 'input.txt'.IO.slurp.trim.lines.map: { $_.split(rx/\s+/) };
say 'part 1: ' ~ filter-safe(@reports).elems;
say 'part 2: ' ~ filter-safe(@reports, True).elems;

#| gets the subset of reports that are safe
sub filter-safe (@reports, $dampener = False) {
    return @reports.grep: {
        my @report = @$_;
        if $dampener {
            # if we have the dampener, we should also consider the potential alternative reports
            # e.g. for 1 2 3 4, we should also consider 2 3 4, 1 3 4, 1 2 4, 1 2 3
            my @variants;
            @variants.push(@report);
            for 0 ..^ @report.elems -> $index {
                @variants.push(@report[flat (0 ..^ $index), ($index ^..^ @report.elems)]);
            }
            (@variants.map: { is-safe(@$_) }).any
        }
        else {
            is-safe(@report)
        }
    };
};

#| checks whether a report is safe
sub is-safe (@report) {
    my $safe = True;
    my $sign;
    for @report[0 ..^ * - 1] Z @report[1 ..^ *] -> [$value1, $value2] {
        my $difference = $value1 - $value2;
        $sign = $difference.sign if (!defined $sign);
        # all subsequent diffs must have the same sign as the first
        # all diffs must step by 1-3
        if ($difference.sign != $sign) || ($difference.abs > 3) || ($difference.abs < 1) {
            $safe = False;
            last;
        }
    }
    return $safe;
};
