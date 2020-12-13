#!/usr/bin/python

import re

filepath = 'input.txt'
required = {
	'byr': lambda x: True if re.match(r'^\d{4}$', x) and (1920 <= int(x) <= 2002) else False,
	'iyr': lambda x: True if re.match(r'^\d{4}$', x) and (2010 <= int(x) <= 2020) else False,
	'eyr': lambda x: True if re.match(r'^\d{4}$', x) and (2020 <= int(x) <= 2030) else False,
	'hgt': lambda x: True if re.match(r'^\d{2,3}(?:cm|in)$', x) and (
			('cm' in x and (150 <= int(''.join([c for c in x if c.isdigit()])) <= 193))
			or ('in' in x and (59 <= int(''.join([c for c in x if c.isdigit()])) <= 76))
		) else False,
	'hcl': lambda x: True if re.match(r'^#[0-9a-f]{6}$', x) else False,
	'ecl': lambda x: True if x in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'] else False,
	'pid': lambda x: True if re.match(r'^\d{9}$', x) else False
}
optional = ['cid']
v2 = False # change to True if doing the second version of the puzzle

filehandle = open(filepath, 'r')
passports = filehandle.read().strip().split('\n\n')
filehandle.close()

valid = 0
for passport in passports:
	pairs = [pair.split(':') for pair in passport.replace('\n', ' ').split()]
	fieldspresent = all(key in [pair[0] for pair in pairs] for key in required.keys())
	fieldsvalid = True if not v2 else all(pair[0] in optional or required[pair[0]](pair[1]) for pair in pairs)
	if fieldspresent and fieldsvalid:
		valid += 1
print valid
