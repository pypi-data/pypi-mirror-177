from remotemanager import URL
from remotemanager.storage.sendablemixin import SendableMixin


class BaseComputer(URL):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.shebang = NotImplemented
        self.pragma = NotImplemented

        self.modules = []

        self.extra = None

    def __setattr__(self, key, value):
        """
        If the set `key` attribute is an MPI option, instead set the `value`
        of that attribute

        Args:
            key:
                attribute name to set
            value:
                value to set to

        Returns:
            None
        """
        if key in self.__dict__:
            if isinstance(getattr(self, key), (optional, required)):
                getattr(self, key).value = value
                return

        object.__setattr__(self, key, value)

    @property
    def arguments(self):
        return [k for k, v in self.__dict__.items()
                if isinstance(v, (optional, required))]

    @property
    def argument_dict(self):
        return {k.strip(): getattr(self, k) for k in self.arguments}

    @property
    def required(self):
        """
        Returns the required arguments
        """
        temp = self.__class__()
        return [k for k, v in temp.__dict__.items() if isinstance(v, required)]

    @property
    def missing(self):
        """
        Returns the currently missing arguments
        """
        return [k for k in self.required if not getattr(self, k)]

    @property
    def valid(self):
        return len(self.missing) == 0

    def update_resources(self, **kwargs):
        """
        Set any arguments passed to the script call

        Args:
            **kwargs:
                kwarg updates e.g. mpi=128
        Returns:
            None
        """
        for k, v in kwargs.items():
            setattr(self, k, v)

    def resources_block(self, **kwargs):

        if 'name' in kwargs:
            # Dataset `name` param detected, use as a default
            if not hasattr(self, 'jobname') or 'jobname' not in kwargs:
                kwargs['jobname'] = kwargs.pop('name')

        self.update_resources(**kwargs)

        if not self.valid:
            raise RuntimeError(f'missing required arguments: {self.missing}')

        options = {}
        for k, v in self.argument_dict.items():
            if v:
                options[v.flag] = v.value
            elif hasattr(v, 'default'):
                options[v.flag] = v.default

        return [f'{self.pragma} {k}={v}' for k, v in sorted(options.items()) if v]

    def modules_block(self):
        return ['\nmodule purge'] + [f'module load {m}' for m in self.modules]

    def script(self,
               **kwargs) -> str:
        """
        Takes job arguments and produces a valid jobscript

        Returns:
            (str):
                script
        """
        script = [self.shebang]

        script += self.resources_block(**kwargs)
        script += self.modules_block()

        if hasattr(self, 'postscript') and self.postscript is not None:
            script.append(self.postscript)

        if hasattr(self, 'extra') and self.extra is not None:
            script.append(self.extra)

        return '\n'.join(script)


class placeholder_option(SendableMixin):
    """
    .. warning::
        This class is intended to be subclassed by the optional and required
        placeholders.

    Stub class to sit in place of an option within a computer.

    Args:
        mode (string):
            storage mode, required or optional
        flag (string):
            flag to append value to (`--nodes`, `--walltime`, etc)
    """

    def __init__(self, mode, flag):
        self._mode = mode
        self._flag = flag
        self._value = None
        self._bool = False

    def __hash__(self):
        return hash(self._mode)

    def __str__(self):
        return str(self.value)

    def __bool__(self):
        """
        Makes objects "falsy" if no value has been set, "truthy" otherwise
        """
        return self._bool

    @property
    def flag(self):
        return self._flag

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._bool = True
        self._value = value


class required(placeholder_option):
    """
    .. warning::
        This class is intended to be subclassed by the optional and required
        placeholders.

    Stub class to sit in place of an option within a computer.

    This option is _required_, and should raise an error if no value is found

    Args:
        flag (string):
            flag to append value to (`--nodes`, `--walltime`, etc)
    """

    def __init__(self, flag):
        super().__init__('required', flag)


class optional(placeholder_option):
    """
    .. warning::
        This class is intended to be subclassed by the optional and required
        placeholders.

    Stub class to sit in place of an option within a computer.

    This option is not required, and should have an accessible default if
    no value is found

    Args:
        flag (string):
            flag to append value to (`--nodes`, `--walltime`, etc)
        default:
            default value to use if none is assigned
    """

    def __init__(self, flag, default=None):
        super().__init__('optional', flag)

        self._default = default

    @property
    def default(self):
        return self._default
