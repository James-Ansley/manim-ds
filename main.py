import operator

from manim import *

from manim_ds.scene import GLOBAL_ANIMATION_BUFFER as BUFFER
from manim_ds.scene import BufferedScene
from manim_ds.structures import *


def bubble_sort(data):
    mlist = MList.from_iterable(data).create()
    for i in range(len(mlist) - 1):
        for j in range(1, len(mlist) - i):
            with mlist.comparing(operator.lt, j, j - 1) as cmp:
                if cmp:
                    mlist.swap(j, j - 1)
        mlist.shade(len(mlist) - i - 1, GREEN)
    mlist.shade(0, GREEN)
    BUFFER.push(*(elt.unshade for elt in mlist))


def selection_sort(data):
    mlist = MList.from_iterable(data).create()
    pointer = Pointer().next_to(mlist[0], DOWN).create()
    for i in range(len(mlist) - 1):
        min_idx = i
        pointer.point_to(mlist[min_idx], mlist)
        for j in range(i + 1, len(mlist)):
            with mlist.comparing(operator.lt, j, min_idx) as cmp:
                if cmp:
                    min_idx = j
                    pointer.point_to(mlist[min_idx], mlist)
        if i != min_idx:
            mlist.swap(i, min_idx)
        mlist.shade(i, GREEN)
    with BUFFER.grouped():
        mlist.shade(len(mlist) - 1, GREEN)
        pointer.uncreate()
    BUFFER.push(*(elt.unshade for elt in mlist))


def selection_sort_overview(data):
    mlist = MList.from_iterable(data).create()
    for i in range(len(mlist) - 1):
        min_idx = min(range(i, len(mlist)), key=lambda i: mlist[i].data)
        mlist.shade(min_idx, GREEN)
        if i != min_idx:
            mlist.swap(i, min_idx)
    mlist.shade(len(mlist) - 1, GREEN)
    BUFFER.push(*(elt.unshade for elt in mlist))


class BubbleSortScene(BufferedScene):
    def construct(self):
        bubble_sort([3, 4, 2, 0, 1])
        self.set_size(7, 3)
        super().construct()


class SelectionSortScene(BufferedScene):
    def construct(self):
        selection_sort([4, 3, 2, 0, 1])
        self.set_size(7, 3)
        self.camera.frame_center = [0, 0.3, 0]
        super().construct()


class SelectionSortOverviewScene(BufferedScene):
    def construct(self):
        selection_sort_overview([4, 3, 2, 0, 1])
        self.set_size(7, 3)
        super().construct()
