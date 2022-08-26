from contextlib import contextmanager
from typing import ContextManager

from manim import Scene, config

from .colours import BACKGROUND


class _GlobalAnimationBuffer:
    def __init__(self):
        self._animations = []
        self._staged = []
        self._should_stage = False

    def push(self, *animations):
        if self._should_stage:
            self._staged.extend(animations)
        else:
            self._animations.append(animations)

    def __iter__(self):
        for animation_group in self._animations:
            yield (animation() for animation in animation_group)

    @contextmanager
    def grouped(self) -> ContextManager[None]:
        if self._should_stage:
            return
        try:
            self._should_stage = True
            yield
        finally:
            self._animations.append(self._staged)
            self._staged = []
            self._should_stage = False


GLOBAL_ANIMATION_BUFFER = _GlobalAnimationBuffer()


class BufferedScene(Scene):
    unit_pixels = 274

    def set_size(self, width, height):
        pixel_width = self.unit_pixels * width
        pixel_height = self.unit_pixels * height
        config.pixel_width = pixel_width
        config.pixel_height = pixel_height
        self.camera.frame_width = width
        self.camera.frame_height = height
        self.camera.pixel_width = pixel_width
        self.camera.pixel_height = pixel_height

    def construct(self):
        self.camera.background_color = BACKGROUND
        for animations in GLOBAL_ANIMATION_BUFFER:
            self.play(*animations)
