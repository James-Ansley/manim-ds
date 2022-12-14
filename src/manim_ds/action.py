from itertools import chain


class Action:
    def __init__(self, *animations, value=None):
        self.value = value
        self.animations = chain(*(_hoist(a) for a in animations))

    def then(self, animation, *args, **kwargs):
        # ToDo - There has to be a better way
        self.animations = (
            getattr(a, animation)(*args, **kwargs) for a in self.animations
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
