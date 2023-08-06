
class GObject(object):
    """
        A generic object.

        Args:
            class_name (str): Object name.
            kwargs: All kwargs represents attributes/items of the class.
    """
    def __init__(self, class_name='GenericObj', **kwargs):
        self.class_name = class_name
        self.kwargs = kwargs

    def all(self):
        """ Return all attributes/items names. """
        return list(self.kwargs.keys())

    def __repr__(self):
        return f"<class '{self.class_name}'>"

    def __getattr__(self, item):
        return self.kwargs[item]

    def __getitem__(self, item):
        return self.kwargs[item]

    def get(self, item, default=None):
        """ Return the value for key if key is in the items, else default. """
        return self.kwargs.get(item, default)

    def to_dict(self):
        """ Return kwargs dictionary. """
        return self.kwargs
