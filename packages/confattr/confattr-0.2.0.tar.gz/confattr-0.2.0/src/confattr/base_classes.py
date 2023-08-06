#!./runmodule.sh

import abc
import typing

class Logger(typing.Protocol):

	def show_info(self, msg: str) -> None:
		pass

	def show_error(self, msg: 'str|BaseException') -> None:
		pass
