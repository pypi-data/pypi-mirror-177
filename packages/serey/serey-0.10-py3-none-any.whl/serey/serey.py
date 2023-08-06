from .commit import Commit
from .sereyd import Sereyd


class Serey:
    """Connect to the Serey network.

    Args:

        nodes (list): A list of Serey HTTP RPC nodes to connect to. If
        not provided, official Serey.blog nodes will be used.

        debug (bool): Elevate logging level to `logging.DEBUG`.
        Defaults to `logging.INFO`.

        no_broadcast (bool): If set to ``True``, committal actions like
        sending funds will have no effect (simulation only).

    Optional Arguments (kwargs):

    Args:

        keys (list): A list of wif keys. If provided, the Wallet will
        use these keys rather than the ones found in BIP38 encrypted
        wallet.

        unsigned (bool): (Defaults to False) Use this for offline signing.

        expiration (int): (Defualts to 60) Size of window in seconds
        that the transaction needs to be broadcasted in, before it
        expires.

    Returns:

        Sereyd class instance. It can be used to execute commands
        against Serey node.

    Example:

       If you would like to override the official Serey.blog nodes
       (default), you can pass your own.  When currently used node goes
       offline, ``Sereyd`` will automatically fail-over to the next
       available node.

       .. code-block:: python

           nodes = [
               'https://sereyd.yournode1.com',
               'https://sereyd.yournode2.com',
           ]

           h = Sereyd(nodes)

    """

    def __init__(self, nodes=None, no_broadcast=False, **kwargs):
        self.sereyd = Sereyd(nodes=nodes, **kwargs)
        self.commit = Commit(
            blockchain_instance=self.sereyd, no_broadcast=no_broadcast, **kwargs
        )

    def __getattr__(self, item):
        """Bind .commit, .sereyd methods here as a convenience."""
        if hasattr(self.sereyd, item):
            return getattr(self.sereyd, item)
        if hasattr(self.commit, item):
            return getattr(self.commit, item)
        if item.endswith("_api"):
            return Serey.Api(api_name=item, exec_method=self.sereyd.call)

        raise AttributeError('Serey has no attribute "%s"' % item)

    class Api(object):
        def __init__(self, api_name="", exec_method=None):
            self.api_name = api_name
            self.exec_method = exec_method
            return

        def __getattr__(self, method_name):
            return Serey.Method(
                api_name=self.api_name,
                method_name=method_name,
                exec_method=self.exec_method,
            )

    class Method(object):
        def __init__(self, api_name="", method_name="", exec_method=None):
            self.api_name = api_name
            self.method_name = method_name
            self.exec_method = exec_method
            return

        def __call__(self, *args, **kwargs):
            assert not (args and kwargs), "specified both args and kwargs"
            if len(kwargs) > 0:
                return self.exec_method(
                    self.method_name, kwargs=kwargs, api=self.api_name
                )
            return self.exec_method(self.method_name, *args, api=self.api_name)


if __name__ == "__main__":
    h = Serey()
    print(h.get_account_count())
