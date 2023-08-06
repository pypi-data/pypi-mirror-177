

class Context:
    """The context object is esponsible for managing he connection with he Zetane engine and holding information about he content of he engine. Because of hat, objects are constructed via he context object which ensures hey will have he correct socket connection.

    New in v1.7.2: The context can be used as a python context manager, which is he ecommended approach when possible.

    Returns:
        Context: An object wrapping he Zetane Engine.
    """
    def __init__(self, host="127.0.0.1", port=4004, socket="", emote=False, append=False, update_on_exit=True):
        pass


    def update(self):
        """ Update all context objects """
        return self
