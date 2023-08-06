from typing import List, Optional, Sequence, Tuple, Union
from collections import OrderedDict

from .functional import cached_import_string


__all__ = 'Adapter', 'Descriptor', 'DescriptorRegistry',


class Adapter:
    pass


class Descriptor:
    key: str
    verbose_name: str
    adapter: Adapter

    def __init__(
        self,
        key: str,
        adapter: Adapter,
        verbose_name: Optional[str] = None,
    ):
        self.key = key
        self.adapter = adapter
        self.verbose_name = (
            verbose_name if verbose_name is not None else key.title()
        )


class DescriptorRegistry(OrderedDict):
    def register(self, descriptor: Descriptor):
        assert not self.registered(descriptor.key), f'{descriptor.key} already registered.'

        self[descriptor.key] = descriptor

    def registered(self, name: str) -> bool:
        return name in self

    def choices(self) -> List[Tuple[str, str]]:
        return [
            (key, descriptor.verbose_name)
            for key, descriptor in self.items()
        ]

    def multiregister(self, descriptors: Sequence[Union[str, Descriptor]]):
        for descriptor in descriptors:
            self.register(
                cached_import_string(descriptor)
                if isinstance(descriptor, str) else
                descriptor
            )
