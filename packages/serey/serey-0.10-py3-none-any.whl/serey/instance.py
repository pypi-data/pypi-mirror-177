import serey as hve
import sys

_shared_blockchain_instance = None


def get_config_node_list():
    from sereybase.storage import configStorage

    nodes = configStorage.get("nodes", None)
    if nodes:
        return nodes.split(",")


def shared_blockchain_instance():
    """This method will initialize _shared_blockchain_instance and return it.
    The purpose of this method is to have offer single default Hive
    instance that can be reused by multiple classes."""

    global _shared_blockchain_instance
    if not _shared_blockchain_instance:
        if sys.version >= "3.0":
            _shared_blockchain_instance = hve.sereyd.Sereyd(nodes=get_config_node_list())
        else:
            _shared_blockchain_instance = hve.Sereyd(nodes=get_config_node_list())
    return _shared_blockchain_instance


def set_shared_blockchain_instance(blockchain_instance):
    """This method allows us to override default hive instance for all
    users of _shared_blockchain_instance."""

    global _shared_blockchain_instance
    _shared_blockchain_instance = blockchain_instance
