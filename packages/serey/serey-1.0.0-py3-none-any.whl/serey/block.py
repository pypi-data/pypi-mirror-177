from sereybase.exceptions import BlockDoesNotExistsException

from .instance import shared_blockchain_instance
from .utils import parse_time


class Block(dict):
    """Read a single block from the chain

    :param int block: block number
    :param Sereyd blockchain_instance: Hived() instance to use when
        accessing a RPC

    """

    def __init__(self, block, blockchain_instance=None):
        self.sereyd = blockchain_instance or shared_blockchain_instance()
        self.block = block

        if isinstance(block, Block):
            super(Block, self).__init__(block)
        else:
            self.refresh()

    def refresh(self):
        block = self.sereyd.get_block(self.block)
        if not block:
            raise BlockDoesNotExistsException
        super(Block, self).__init__(block)

    def __getitem__(self, key):
        return super(Block, self).__getitem__(key)

    def items(self):
        return super(Block, self).items()

    def time(self):
        return parse_time(self["timestamp"])
