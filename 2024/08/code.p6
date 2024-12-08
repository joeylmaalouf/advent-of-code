#!/usr/bin/env perl6

my @map = 'input.txt'.IO.slurp.trim.lines.map({ $_.comb });
say 'part 1: ' ~ get-antinodes-on-map(@map).map({ $_.join(',') }).unique.elems;
say 'part 2: ' ~ get-antinodes-on-map(@map, True).map({ $_.join(',') }).unique.elems;

#| get the antinodes that are present in a given map
sub get-antinodes-on-map (@map, $repeat = False) {
    my $height = @map.elems;
    my $width = @map[0].elems;
    my %antennas;
    for ((0 ..^ $height) X (0 ..^ $width)) -> ($y, $x) {
        unless @map[$y][$x] eq '.' { %antennas{@map[$y][$x]}.push(($y, $x)); };
    };
    my @antinodes;
    for %antennas.kv -> $frequency, @positions {
        for @positions.combinations(2) -> (@point_a, @point_b) {
            @antinodes.append(get-antinodes-for-pair(@point_a, @point_b, $height, $width, $repeat));
        };
    };
    return @antinodes;
};

#| get the antinodes for a given pair
sub get-antinodes-for-pair (@point_a, @point_b, $height, $width, $repeat) {
    # get the diff between the two points in the pair,
    # then apply that same diff in the outer directions
    my $dy = @point_a[0] - @point_b[0];
    my $dx = @point_a[1] - @point_b[1];
    return (
        extend-point(@point_a, $dy, $dx, $height, $width, $repeat),
        extend-point(@point_b, -$dy, -$dx, $height, $width, $repeat),
    ).flat;
};

#| apply movement to the given point unless it ends up out of bounds, potentially repeating
sub extend-point (@point, $dy, $dx, $height, $width, $repeat) {
    my @points; if $repeat { @points.push(@point); }; # if repeating, we'll also add the i = 0 case that we already start with
    my $i = 1;
    # if the extension is in bounds, add it to the list
    # if we aren't repeating, just stop there
    # otherwise, repeat the extension until we go out of bounds
    repeat {
        my @new = (@point[0] + $dy * $i, @point[1] + $dx * $i); 
        if (0 <= @new[0]) && (@new[0] < $height) && (0 <= @new[1]) && (@new[1] < $width) {
            @points.push(@new);
        } else {
            last;
        };
        $i++;
    } while $repeat;
    return @points;
};
