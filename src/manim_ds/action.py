from itertools import chain


class Action:
    def __init__(self, value, *animations):
        self.value = value
        self.animations = chain(*(_hoist(a) for a in animations))

    def then(self, animation, *args):
        self.animations = (
            # lambda new=animation, a=a: getattr(a(), new)(*args)
            lambda new=animation, a=a: new(a(), *args)
            for a in self.animations
        )
        return self

    def __iter__(self):
        yield self.value
        yield self.animations


def _hoist(animation):
    if isinstance(animation, Action):
        return animation.animations
    else:
        return animation,
