import abc
from itertools import chain

from manim import Scene, config

from manim_ds.action import Action
from manim_ds.config import CONFIG


def _hoist(action):
    if not isinstance(action, Action):
        action = Action(action, value=None)
    return action


class BufferedScene(Scene, abc.ABC):
    def __init__(self):
        super().__init__()
        self.buffer = []

    def do(self, action):
        action = _hoist(action)
        self.buffer.append(action.animations)
        return action.value

    def do_all(self, *actions):
        self.buffer.append(chain(*(_hoist(a).animations for a in actions)))
        return (a.value for a in actions)

    def set_size(self, width, height):
        pixel_width = CONFIG["pixelsPerUnit"] * width
        pixel_height = CONFIG["pixelsPerUnit"] * height
        config.pixel_width = pixel_width
        config.pixel_height = pixel_height
        self.camera.frame_width = width
        self.camera.frame_height = height
        self.camera.pixel_width = pixel_width
        self.camera.pixel_height = pixel_height

    def construct(self):
        self.camera.background_color = CONFIG["background"]
        self._construct()
        for animations in self.buffer:
            self.play(*(a() for a in animations))

    @abc.abstractmethod
    def _construct(self):
        ...
