#!/usr/bin/env perl6

my @map = 'input.txt'.IO.slurp.trim.lines.map({ $_.comb });
my %directions = (
    'U' => (-1, 0, 'R'),
    'R' => (0, 1, 'D'),
    'D' => (1, 0, 'L'),
    'L' => (0, -1, 'U'),
);
my @guard;
for ((0 ..^ @map.elems) X (0 ..^ @map[0].elems)) -> ($y, $x) {
    if @map[$y][$x] eq '^' { @guard = ($y, $x, 'U'); last; };
};
my @unique_path = get-traversed(@map, %directions, @guard.clone).map({ $_.join(',') }).unique.map({ $_.split(rx/\,/) });
say 'part 1: ' ~ @unique_path.elems;
say 'part 2: ' ~ get-potential-loops(@map, %directions, @guard.clone, @unique_path).elems;

#| get the list of positions that the guard traverses before leaving (or Nil if he's stuck in a loop)
sub get-traversed (@map, %directions, @guard, @object = ()) {
    my @path;
    my %visited;
    @path.push([@guard[0], @guard[1]]);
    %visited{@guard.join(',')} = True;
    loop {
        my @next = (@guard[0] + %directions{@guard[2]}[0], @guard[1] + %directions{@guard[2]}[1]);
        # if the next step is out of bounds, finish
        if (@next[0] < 0) || (@map.elems <= @next[0])
        || (@next[1] < 0) || (@map[0].elems <= @next[1]) {
            return @path;
        }
        # if the next step is an obstacle (including the potential new one), turn in place
        elsif (@map[@next[0]][@next[1]] eq '#') || (@object && (@next[0] == @object[0] && @next[1] == @object[1])) {
            @guard[2] = %directions{@guard[2]}[2];
        }
        # if the next step is open, step forward
        else {
            @guard[0 .. 1] = @next;
            @path.push(@next);
            # if he's already been in this position/orientation, he's hit a loop
            if %visited{@guard.join(',')} { return Nil; };
            %visited{@guard.join(',')} = True;
        };
    };
};

#| get the list of positions along the path that, if given an obstacle, would make the guard loop
sub get-potential-loops (@map, %directions, @guard, @path) {
    my @loop_causers;
    my @start = @guard.clone;
    for @path[1 .. *] -> @object { # we can't put an obstacle where the guard starts
        my %visited;
        %visited{@start.join(',')} = True;
        if get-traversed(@map, %directions, @start.clone, @object) === Nil {
            @loop_causers.push(@object);
        };
    };
    return @loop_causers;
};
