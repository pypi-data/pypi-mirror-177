# pylint: disable = missing-module-docstring

import pydrumscore.core.song as api
from pydrumscore.core.beats import MONEY_BEAT

metadata = api.Metadata(
    workTitle = "Hi-hat open permutations",
    )

measures = []

hho_perms = api.note_range(1, api.END, 0.5)
for p in hho_perms:
    m = api.Measure(MONEY_BEAT)

    m.hh.remove(p)
    m.ho += [p]

    measures += m
    measures += MONEY_BEAT

    if p is not hho_perms[-1]:
        measures[-1].has_line_break = True
