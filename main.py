from operator import lt
from pathlib import Path

from manim import DOWN

from manim_ds.scene import ActionScene
from manim_ds.structures import MList, Pointer
from manim_ds.config import CONFIG, load


load(Path("custom_config.toml"))


class BubbleSortScene(ActionScene):
    def __init__(self):
        super().__init__()
        self.set_size(7, 3)

    def construct(self):
        mlist = MList([3, 4, 2, 0, 1])
        do = self.do
        do_all = self.do_all

        self.do(mlist.create())
        for i in range(len(mlist) - 1):
            for j in range(1, len(mlist) - i):
                comparing = (j, j - 1)
                if do(mlist.compare(lt, *comparing)):
                    do(mlist.swap(j, j - 1))
                do(mlist.uncompare(*comparing))
            do(mlist[len(mlist) - i - 1].shade(CONFIG["primary"]))
        do(mlist[0].shade(CONFIG["primary"]))
        do_all(*(e.unshade() for e in mlist))


class SelectionSortScene(ActionScene):
    def __init__(self):
        super().__init__()
        self.set_size(7, 3)

    def construct(self):
        do = self.do
        do_all = self.do_all

        mlist = MList([4, 3, 2, 0, 1]).shift(DOWN / 3)
        pointer = Pointer().next_to(mlist[0], DOWN)

        do_all(mlist.create(), pointer.create())
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
            do(mlist[i].shade(CONFIG["primary"]))
        do_all(mlist[-1].shade(CONFIG["primary"]), pointer.uncreate())
        do_all(*(elt.unshade() for elt in mlist))


class SelectionSortOverviewScene(ActionScene):
    def __init__(self):
        super().__init__()
        self.set_size(7, 3)

    def construct(self):
        do = self.do
        do_all = self.do_all

        mlist = MList([4, 3, 2, 0, 1])

        do(mlist.create())
        for i in range(len(mlist) - 1):
            min_idx = min(range(i, len(mlist)), key=lambda j: mlist[j].data)
            do(mlist[min_idx].shade(CONFIG["primary"]))
            if i != min_idx:
                do(mlist.swap(i, min_idx))
        do(mlist[-1].shade(CONFIG["primary"]))
        do_all(*(elt.unshade() for elt in mlist))
