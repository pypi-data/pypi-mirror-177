from .instance import shared_blockchain_instance

from sereybase.exceptions import WitnessDoesNotExistsException


class Witness(dict):
    """Read data about a witness in the chain

    :param str witness: Name of the witness
    :param Sereyd blockchain_instance: Hived() instance to use when
    accessing a RPC

    """

    def __init__(self, witness, blockchain_instance=None):
        self.sereyd = blockchain_instance or shared_blockchain_instance()
        self.witness_name = witness
        self.witness = None
        self.refresh()

    def refresh(self):
        witness = self.sereyd.get_witness_by_account(self.witness_name)
        if not witness:
            raise WitnessDoesNotExistsException
        super(Witness, self).__init__(witness)

    def __getitem__(self, key):
        return super(Witness, self).__getitem__(key)

    def items(self):
        return super(Witness, self).items()
