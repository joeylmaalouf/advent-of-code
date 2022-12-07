#!/usr/bin/python3


def main (filepath):
	filesystem = construct_filesystem(parse_input(filepath))
	print('part 1:', sum(find_dirs_between(filesystem, 0, 100000)))
	print('part 2:', min(find_dirs_between(filesystem, 30000000 - (70000000 - filesystem.get_size()), 70000000)))


class File:
	def __init__ (self, name, parent, size):
		self.name = name
		self.parent = parent
		self.size = size
	def get_size (self):
		return self.size


class Folder(File):
	def __init__ (self, name, parent, children):
		self.name = name
		self.parent = parent
		self.children = children
	def add_child (self, child):
		child.parent = self
		self.children[child.name] = child
	def get_size (self):
		return sum(child.get_size() for child in self.children.values())


def parse_input (filepath):
	with open(filepath, 'r') as filehandle:
		# the input is a list of commands with 1 input line and 0+ output lines
		commands = []
		for command in filehandle.read().strip().split('$ ')[1 :]:
			inpt, outpt = command.split('\n')[0], [line for line in command.split('\n')[1 :] if line]
			operation, *arguments = inpt.split()
			results = [{'size': line.split()[0], 'name': line.split()[1]} for line in outpt]
			commands.append({'input': {'operation': operation, 'arguments': arguments}, 'output': results})
		return commands


def construct_filesystem (commands):
	# the filesystem is made up of folders and files whose structure and sizes we can determine from the given commands
	filesystem = Folder('', None, {})
	current_dir = filesystem
	for command in commands:
		if command['input']['operation'] == 'cd':
			directory = command['input']['arguments'][0]
			if directory == '..':
				current_dir = current_dir.parent
			else:
				if directory not in current_dir.children.keys():
					current_dir.add_child(Folder(directory, current_dir, {}))
				current_dir = current_dir.children[directory]
		elif command['input']['operation'] == 'ls':
			for result in command['output']:
				if result['size'] == 'dir':
					current_dir.add_child(Folder(result['name'], current_dir, {}))
				else:
					current_dir.add_child(File(result['name'], current_dir, int(result['size'])))
	return filesystem.children['/']


def find_dirs_between (filesystem, lower_bound, upper_bound):
	# we can recurse through directories to find ones that meet our thresholds
	dir_sizes = []
	dir_size = filesystem.get_size()
	if dir_size > lower_bound and dir_size <= upper_bound:
		dir_sizes.append(dir_size)
	for child in filesystem.children.values():
		if isinstance(child, Folder):
			dir_sizes.extend(find_dirs_between(child, lower_bound, upper_bound))
	return dir_sizes


if __name__ == '__main__':
	main('input.txt')
