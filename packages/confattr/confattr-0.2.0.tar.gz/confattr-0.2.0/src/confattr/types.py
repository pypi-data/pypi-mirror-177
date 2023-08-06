#!/usr/bin/env python3

import os
import shutil
import shlex
import enum
import functools
import typing
from collections.abc import Sequence, Callable, Mapping, MutableMapping

from .subprocess_pipe import run_and_pipe, CompletedProcess


TYPE_CONTEXT: 'typing.TypeAlias' = 'Callable[[Command], typing.ContextManager[Command]] | None'


class Path:

	'''
	This is the path as it is stored in the config file.
	It may contain stuff like ~/... and device UUIDs to be mounted.
	In order to use it it needs to be converted with lsblk.mounter.expand_path.
	'''

	type_name = 'path'
	help = '''
	The path to a directory.
	You can use "~/" as an abbreviation for your home directory.
	The path may start with "UUID:.../", then the file system is mounted automatically.
	If the file system is on an encrypted partition you can use "UNLOCK:...,UUID:.../".
	'''

	def __init__(self, value: str) -> None:
		self.raw = value

	def __str__(self) -> str:
		return self.raw

	def __repr__(self) -> str:
		return '%s(%r)' % (type(self).__name__, self.raw)

	def __bool__(self) -> bool:
		return bool(self.raw)


class Regex(str):

	type_name = 'regular expression'
	help = 'https://docs.python.org/3/library/re.html#regular-expression-syntax'


class Command:

	type_name = 'command'

	python_callbacks: 'MutableMapping[str, Callable[[Command, TYPE_CONTEXT], None]]' = {}

	@classmethod
	def register_python_callback(cls, name: str, func: 'Callable[[Command, TYPE_CONTEXT], None]') -> None:
		cls.python_callbacks[name] = func

	@classmethod
	def unregister_python_callback(cls, name: str) -> None:
		del cls.python_callbacks[name]

	@classmethod
	def has_python_callback(cls, name: str) -> bool:
		return name in cls.python_callbacks


	def __init__(self, arg: 'Command|Sequence[str]|str', *, env: 'Mapping[str, str]|None' = None) -> None:
		self.cmd: 'Sequence[str]'
		self.env: 'Mapping[str, str]|None'
		if isinstance(arg, str):
			assert env is None
			self.parse_str(arg)
		elif isinstance(arg, Command):
			self.cmd = list(arg.cmd)
			self.env = dict(arg.env) if arg.env else None
			if env:
				if self.env:
					self.env.update(env)
				else:
					self.env = env
		else:
			self.cmd = list(arg)
			self.env = env

	def parse_str(self, arg: str) -> None:
		'''
		parses a string as returned by __str__

		example:
			if the input is arg = 'ENVVAR1=val ENVVAR2= cmd --arg1 --arg2'
			this function sets
				self.env = {'ENVVAR1' : 'val', 'ENVVAR2' : ''}
				self.cmd = ['cmd', '--arg1', '--arg2']

		raises ValueError if cmd is invalid
		'''
		if not arg:
			raise ValueError('cmd is empty')

		cmd = shlex.split(arg)

		self.env = {}
		for i in range(len(cmd)):
			if '=' in cmd[i]:
				var, val = cmd[i].split('=', 1)
				self.env[var] = val
			else:
				self.cmd = cmd[i:]
				if not self.env:
					self.env = None
				return

		raise ValueError('cmd consists of environment variables only, there is no command to be executed')

	# ------- compare -------

	def __eq__(self, other: typing.Any) -> bool:
		if isinstance(other, Command):
			return self.cmd == other.cmd and self.env == other.env
		return NotImplemented

	# ------- custom methods -------

	def replace(self, wildcard: str, replacement: str) -> 'Command':
		return Command([replacement if word == wildcard else word for word in self.cmd], env=self.env)

	def run(self, *, context: 'TYPE_CONTEXT|None') -> 'CompletedProcess[bytes]|None':
		'''
		Runs this command and returns when the command is finished.

		:param context: returns a context manager which can be used to stop and start an urwid screen.
		It takes the command to be executed so that it can log the command
		and it returns the command to be executed so that it can modify the command,
		e.g. processing and intercepting some environment variables.

		:return: The completed process
		:raises OSError: e.g. if the program was not found
		:raises CalledProcessError: if the called program failed
		'''
		if self.cmd[0] in self.python_callbacks:
			self.python_callbacks[self.cmd[0]](self, context)
			return None

		if context is None:
			return run_and_pipe(self.cmd, env=self._add_os_environ(self.env))

		with context(self) as command:
			return run_and_pipe(command.cmd, env=self._add_os_environ(command.env))

	@staticmethod
	def _add_os_environ(env: 'Mapping[str, str]|None') -> 'Mapping[str, str]|None':
		if env is None:
			return env
		return dict(os.environ, **env)

	def is_installed(self) -> bool:
		return self.cmd[0] in self.python_callbacks or bool(shutil.which(self.cmd[0]))

	# ------- to str -------

	def __str__(self) -> str:
		if self.env:
			env = ' '.join('%s=%s' % (var, shlex.quote(val)) for var, val in self.env.items())
			env += ' '
		else:
			env = ''
		return env + ' '.join(shlex.quote(word) for word in self.cmd)

	def __repr__(self) -> str:
		return '%s(%r, env=%r)' % (type(self).__name__, self.cmd, self.env)

class CommandWithAlternatives:

	type_name = 'command with alternatives'
	help = '''
	One or more commands separated by ||.
	The first command where the program is installed is executed. The other commands are ignored.
	The command is executed without a shell so setting environment variables and redirection are not possible but piping works anyway.
	If you need a shell write the command to a file, insert an appropriate shebang line, make the file executable and set this value to the file.
	'''

	SEP = '||'

	def get_preferred_command(self) -> Command:
		for cmd in self.commands:
			if cmd.is_installed():
				return cmd

		raise FileNotFoundError('none of the commands is installed: %s' % self)


	def __init__(self, commands: 'Sequence[Command|Sequence[str]|str]|str') -> None:
		if isinstance(commands, str):
			self.commands = [Command(cmd) for cmd in commands.split(self.SEP)]
		else:
			self.commands = [Command(cmd) for cmd in commands]


	def __str__(self) -> str:
		return self.SEP.join(str(cmd) for cmd in self.commands)

	def __repr__(self) -> str:
		return '%s(%s)' % (type(self).__name__, self.commands)


	def replace(self, wildcard: str, replacement: str) -> Command:
		return self.get_preferred_command().replace(wildcard, replacement)

	def run(self, context: 'TYPE_CONTEXT|None' = None) -> 'CompletedProcess[bytes]|None':
		return self.get_preferred_command().run(context=context)


@functools.total_ordering
class SortedEnum(enum.Enum):

	def __lt__(self, other: typing.Any) -> bool:
		if self.__class__ is other.__class__:
			l: 'Sequence[SortedEnum]' = list(type(self))
			return l.index(self) < l.index(other)
		return NotImplemented
