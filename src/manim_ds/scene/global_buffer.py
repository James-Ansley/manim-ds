from contextlib import contextmanager
from typing import ContextManager

import manim

from manim_ds.config import CONFIG


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
            yield [animation() for animation in animation_group]

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
