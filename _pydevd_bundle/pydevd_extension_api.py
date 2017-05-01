import abc


# borrowed from from six
def _with_metaclass(meta, *bases):
    """Create a base class with a metaclass."""

    class metaclass(meta):
        def __new__(cls, name, this_bases, d):
            return meta(name, bases, d)

    return type.__new__(metaclass, 'temporary_class', (), {})


# =======================================================================================================================
# AbstractResolver
# =======================================================================================================================
class _AbstractResolver(_with_metaclass(abc.ABCMeta)):
    """
        This class exists only for documentation purposes to explain how to create a resolver.

        Some examples on how to resolve things:
        - list: get_dictionary could return a dict with index->item and use the index to resolve it later
        - set: get_dictionary could return a dict with id(object)->object and reiterate in that array to resolve it later
        - arbitrary instance: get_dictionary could return dict with attr_name->attr and use getattr to resolve it later
    """

    # In addition to the following methods it is also possible to define boolean: use_value_repr_instead_of_str in
    # the class which is used to define if str() or repr() should be used to get the representation of the object.
    # The default is using to use 'str' (same as use_value_repr_instead_of_str = False)

    @abc.abstractmethod
    def resolve(self, var, attribute):
        """
            In this method, we'll resolve some child item given the string representation of the item in the key
            representing the previously asked dictionary.

            @param var: this is the actual variable to be resolved.
            @param attribute: this is the string representation of a key previously returned in get_dictionary.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_dictionary(self, var):
        """
            @param var: this is the variable that should have its children gotten.

            @return: a dictionary where each pair key, value should be shown to the user as children items
            in the variables view for the given var.
        """
        raise NotImplementedError


class _AbstractProvider(_with_metaclass(abc.ABCMeta)):
    @abc.abstractmethod
    def can_provide(self, type_object, type_name):
        raise NotImplementedError


# =======================================================================================================================
# API CLASSES:
# =======================================================================================================================

class TypeResolveProvider(_AbstractResolver, _AbstractProvider):
    """
        Implement this in an extension to provide a custom resolver, see _AbstractResolver
    """


class StrPresentationProvider(_AbstractProvider):
    """
    Implement this in an extension to provide a str presentation for a type
    """

    @abc.abstractmethod
    def get_str(self, val):
        raise NotImplementedError


class DebuggerEventHandler(_with_metaclass(abc.ABCMeta)):
    """
    Implement this to receive lifecycle events from the debugger
    """

    def on_debugger_modules_loaded(self, **kwargs):
        """
        This method invoked after all debugger modules are loaded. Useful for importing and/or patching debugger
        modules at a safe time
        :param kwargs: This is intended to be flexible dict passed from the debugger.
        Currently passes the debugger version
        """
