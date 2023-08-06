'''	Copyright © 2022 mightbesimon.com
	All rights reserved.

	Material belonging to others may have been
	used under Creative Commons Licence or with
	explicit or implicit permission.
'''

from __future__ import annotations
from typing import Any
from .metadeco import metadeco

################################################################
#######                    metaclass                     #######
################################################################
@metadeco
class meta(type):
	'''	metaclass for metaclasses 🍾\n
		what an invention! 🎉\n
		allows subsequent metaclasses to use the decorator
		creation syntax.\n
		When making metaclasses, this syntax super powerful!

		example:
		```python
		@meta
		class enum(type): ...

		@enum	# decorator creation syntax
		class Palette1: ...

		# normal metaclass syntax
		class Palette2(metaclass=enum): ...
		```
	'''
	def __new__(cls:type,
		name:str,
		bases:tuple[type],
		attrs:dict[str, Any],
	) -> type:
		created_metaclass: type = super().__new__(cls, name, bases, attrs)
		created_metaclass.__repr__ = meta.__repr__
		return metadeco(created_metaclass)

	def __repr__(cls) -> str:
		'''	example:
			```plaintext
			<meta 'meta'>
			<meta 'enum'>
			<enum 'Palette'>
			```
		'''
		return f'<{cls.__class__.__name__} \'{cls.__module__}.{cls.__name__}\'>'


################################################################

# self-decorate meta metaclass
meta = meta(meta)
