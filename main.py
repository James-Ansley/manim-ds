from operator import lt

from manim import *

from manim_ds.scene import BufferedScene
from manim_ds.structures import *


class BubbleSortScene(BufferedScene):
    def bubble_sort(self, data):
        do = self.do
        mlist = self.do(MList.from_iterable(data).create())
        for i in range(len(mlist) - 1):
            for j in range(1, len(mlist) - i):
                comparing = (j, j - 1)
                if do(mlist.compare(lt, *comparing)):
                    do(mlist.swap(j, j - 1))
                do(mlist.uncompare(*comparing))
            do(mlist[len(mlist) - i - 1].shade(GREEN))
        do(mlist[0].shade(GREEN))
        self.do_all(*(e.unshade() for e in mlist))

    def construct(self):
        self.bubble_sort([3, 4, 2, 0, 1])
        self.set_size(7, 3)
        super().construct()


class SelectionSortScene(BufferedScene):
    def selection_sort(self, data):
        do = self.do
        mlist = do(MList.from_iterable(data).create())
        pointer = do(Pointer().next_to(mlist[0], DOWN).create())
        for i in range(len(mlist) - 1):
            min_idx = i
            do(pointer.point_to(mlist[min_idx], mlist))
            for j in range(i + 1, len(mlist)):
                comparing = (j, min_idx)
                if do(mlist.compare(lt, *comparing)):
                    min_idx = j
                    do(pointer.point_to(mlist[min_idx], mlist))
                do(mlist.uncompare(*comparing))
            if i != min_idx:
                do(mlist.swap(i, min_idx))
            do(mlist[i].shade(GREEN))
        self.do_all(
            mlist[-1].shade(GREEN),
            pointer.uncreate(),
        )
        self.do_all(*(elt.unshade() for elt in mlist))

    def construct(self):
        self.selection_sort([4, 3, 2, 0, 1])
        self.set_size(7, 3)
        self.camera.frame_center = [0, 0.3, 0]
        super().construct()


class SelectionSortOverviewScene(BufferedScene):
    def selection_sort_overview(self, data):
        do = self.do
        mlist = do(MList.from_iterable(data).create())
        for i in range(len(mlist) - 1):
            min_idx = min(range(i, len(mlist)), key=lambda i: mlist[i].data)
            do(mlist[min_idx].shade(GREEN))
            if i != min_idx:
                do(mlist.swap(i, min_idx))
        do(mlist[-1].shade(GREEN))
        self.do_all(*(elt.unshade() for elt in mlist))

    def construct(self):
        self.selection_sort_overview([4, 3, 2, 0, 1])
        self.set_size(7, 3)
        super().construct()
