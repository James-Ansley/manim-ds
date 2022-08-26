class Action:
    def __init__(self, value, *animations):
        self.value = value
        temp_animations = []
        for animation in animations:
            if isinstance(animation, Action):
                temp_animations.extend(animation.animations)
            else:
                temp_animations.append(animation)
        self.animations = tuple(temp_animations)

    def then(self, animation, *args):
        self.animations = (
            lambda new=animation, a=a: getattr(a(), new)(*args)
            for a in self.animations
        )
        return self

    def __iter__(self):
        yield self.value
        yield self.animations