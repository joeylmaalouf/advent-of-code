#!/usr/bin/python3
import hashlib


def main (filepath):
	key = parse_input(filepath)
	print('part 1:', get_key_suffix(key, 5))
	print('part 2:', get_key_suffix(key, 6))


def parse_input (filepath):
	with open(filepath, 'r') as filehandle:
		return filehandle.read().strip()


def get_key_suffix (key, zeroes):
	i = 1;
	while True:
		md5 = hashlib.md5((key + str(i)).encode('utf-8')).hexdigest()
		if md5.startswith('0' * zeroes):
			break;
		i += 1
	return i;


if __name__ == '__main__':
	main('input.txt')
