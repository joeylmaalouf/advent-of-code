#!/usr/bin/env perl6

my @disk_map = 'input.txt'.IO.slurp.trim.comb;
say 'part 1: ' ~ get-checksum(get-consolidated-blocks(get-block-layout(@disk_map)));
say 'part 2: ' ~ get-checksum(get-consolidated-files(get-file-layout(@disk_map)));

#| gets the file block layout from the disk map
sub get-block-layout (@disk_map) {
    my @file_blocks;
    my $is_file = True;
    my $file_id = 0;
    for @disk_map -> $value {
        @file_blocks.append(($is_file ?? $file_id !! '.') xx $value);
        if ($is_file) { $file_id++; };
        $is_file = !$is_file;
    };
    return @file_blocks;
};

#| consolidates the file blocks into the free spaces
sub get-consolidated-blocks (@file_blocks) {
    my $lindex = 0;
    my $rindex = @file_blocks.elems;
    for @file_blocks -> $block {
        if $block eq '.' {
            my $moved;
            repeat {
                $moved = @file_blocks.pop();
                $rindex--;
            } while $moved eq '.' && $lindex < $rindex;
            @file_blocks[$lindex] = $moved;
            if $lindex >= $rindex { last; };
        };
        $lindex++;
    };
    return @file_blocks;
};

#| gets the whole file layout from the disk map
sub get-file-layout (@disk_map) {
    my @whole_files;
    my $is_file = True;
    my $file_id = 0;
    for @disk_map -> $value {
        unless $value == 0 {
            @whole_files.push([$is_file ?? $file_id.clone !! '.', $value]);
        };
        if ($is_file) { $file_id++; };
        $is_file = !$is_file;
    };
    return @whole_files;
};

#| consolidates the whole files into the free spaces
sub get-consolidated-files (@whole_files) {
    my $lindex = 0;
    my $rindex = @whole_files.elems - 1;
    # for each file from end to start,
    for @whole_files.grep({ $_[0] ne '.' }).reverse -> ($moving_file_id, $moving_file_size) {
        while @whole_files[$rindex][0] eq '.' || @whole_files[$rindex][0] != $moving_file_id { $rindex--; };
        $lindex = 0;
        # look from start to that file's old location for an empty space that can fit it
        for @whole_files -> ($replacing_file_id, $replacing_file_size) {
            if $replacing_file_id eq '.' && $replacing_file_size >= $moving_file_size && $lindex < $rindex {
                # if found, replace the source file with empty space
                @whole_files[$rindex][0] = '.';
                # and replace that destination space with the file plus any leftover space
                my @replacement;
                @replacement.push(($moving_file_id, $moving_file_size));
                if $replacing_file_size > $moving_file_size {
                    @replacement.push(('.', $replacing_file_size - $moving_file_size ));
                };
                @whole_files.splice($lindex, 1, @replacement);
                last;
            };
            $lindex++;
        };
        # combine any adjacent empty spaces that our replacing could have resulted in
        my $zindex = 0;
        while $zindex < @whole_files.elems - 1 {
            if @whole_files[$zindex][0] eq '.' && @whole_files[$zindex + 1][0] eq '.' {
                my @combination; @combination.push(('.', @whole_files[$zindex][1] + @whole_files[$zindex + 1][1]));
                @whole_files.splice($zindex, 2, @combination);
                if $rindex > $zindex { $rindex--; };
            };
            $zindex++;
        };
    };
    # convert the whole files to the file block form that we use everywhere else
    return @whole_files.map({ $_[0] xx $_[1] }).flat;
};

#| calculates the given filesystem's checksum
sub get-checksum (@file_blocks) {
    my $index = -1;
    return @file_blocks.map({
        $index++;
        $_ eq '.' ?? 0 !! ($_ * $index)
    }).sum;
};
