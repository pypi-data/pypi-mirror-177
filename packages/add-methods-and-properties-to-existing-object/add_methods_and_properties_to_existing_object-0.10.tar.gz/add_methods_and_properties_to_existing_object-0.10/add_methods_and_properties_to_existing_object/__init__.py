import inspect
import re
from copy import deepcopy
from string import ascii_letters


def copy_func(f):
    if callable(f):
        if inspect.ismethod(f) or inspect.isfunction(f):
            g = lambda *args, **kwargs: f(*args, **kwargs)
            t = list(filter(lambda prop: not ("__" in prop), dir(f)))
            i = 0
            while i < len(t):
                setattr(g, t[i], getattr(f, t[i]))
                i += 1
            return g
    dcoi = deepcopy([f])
    return dcoi[0]


class FlexiblePartial:
    def __init__(self, func, this_args_first, *args, **kwargs):

        try:
            self.f = copy_func(func)  # create a copy of the function
        except Exception:
            self.f = func
        self.this_args_first = this_args_first  # where should the other (optional) arguments be that are passed when the function is called
        try:
            self.modulename = args[0].__class__.__name__  # to make repr look good
        except Exception:
            self.modulename = "self"

        try:
            self.functionname = func.__name__  # to make repr look good
        except Exception:
            try:
                self.functionname = func.__qualname__  # to make repr look good
            except Exception:
                self.functionname = "func"

        self.args = args
        self.kwargs = kwargs

        self.name_to_print = self._create_name()  # to make repr look good

    def _create_name(self):
        stra = self.modulename + "." + self.functionname + "(self, "
        for _ in self.args[1:]:
            stra = stra + repr(_) + ", "
        for key, item in self.kwargs.items():
            stra = stra + str(key) + "=" + repr(item) + ", "
        stra = stra.rstrip().rstrip(",")
        stra += ")"
        if len(stra) > 100:
            stra = stra[:95] + "...)"
        return stra

    def __call__(self, *args, **kwargs):
        newdic = {}
        newdic.update(self.kwargs)
        newdic.update(kwargs)
        if self.this_args_first:
            return self.f(*self.args[1:], *args, **newdic)

        else:

            return self.f(*args, *self.args[1:], **newdic)

    def __str__(self):
        return self.name_to_print

    def __repr__(self):
        return self.__str__()


class AddMethodsAndProperties:
    def add_methods(self, dict_to_add):
        for key_, item in dict_to_add.items():
            key = re.sub(rf"[^{ascii_letters}]+", "_", str(key_)).rstrip("_")
            if isinstance(item, dict):
                if "function" in item:  # for adding methods
                    if not isinstance(
                        item["function"], str
                    ):  # for external functions that are not part of the class
                        setattr(
                            self,
                            key,
                            FlexiblePartial(
                                item["function"],
                                item["this_args_first"],
                                self,
                                *item["args"],
                                **item["kwargs"],
                            ),
                        )

                    else:
                        setattr(
                            self,
                            key,
                            FlexiblePartial(
                                getattr(
                                    self, item["function"]
                                ),  # for internal functions - part of the class
                                item["this_args_first"],
                                self,
                                *item["args"],
                                **item["kwargs"],
                            ),
                        )
            else:  # for adding props
                setattr(self, key, item)
