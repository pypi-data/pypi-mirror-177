#!/usr/bin/env python
import os
from typing import *
import itertools
import functools
import re

from plover.engine import StenoEngine
from plover.translation import Translator, Stroke, Translation
from plover.formatting import _Context, _Action, _atom_to_action, _translation_to_actions
from plover.macro.undo import undo
from plover.oslayer.config import CONFIG_DIR
from plover.steno_dictionary import StenoDictionaryCollection
import json

directories_home = CONFIG_DIR + "/"


def split_previous(translator: Translator, stroke: Stroke, cmdline: str):
    translation: Translation(
        outline, translation) = translator.get_state().prev()[-1]
    latest_stroke = translation.rtfcre[-1]

    undo(translator, stroke, cmdline)

    translator.translate_stroke(Stroke("ß"))
    translator.translate_stroke(Stroke(latest_stroke))

    # newstroke = stroke.steno_keys[0:-1]
    newstroke = "".join(stroke.steno_keys[0:-1]).replace("ß", "")
    if not "".join(newstroke) == "*":
        translator.translate_stroke(
            Stroke(newstroke))
    else:
        print("found undo")


def space_or_split(translator: Translator, stroke: Stroke, cmdline: str):
    if len(stroke.steno_keys) > 1:
        # is a stroke
        split_previous(translator, stroke, cmdline)
    else:
        # is a space
        translator.translate_stroke(Stroke("*À"))


def find_homophone(translator: Translator, stroke: Stroke, cmdline: str):
    prev = translator.get_state().prev()[-1]
    current_word = prev.english

    dicts: StenoDictionaryCollection = translator.get_dictionary()
    homophones: List[Tuple[string, string]
                     ] = dicts.lookup_from_all(prev.rtfcre)

    homophones_list = list(
        set(map(lambda word_tuple: word_tuple[0], homophones)))

    next_position = homophones_list.index(current_word)+1
    if next_position > len(homophones_list)-1:
        next_position = 0

    t = Translation(list(map(lambda x: Stroke(x), prev.rtfcre)), ''.join(
        homophones_list[next_position]))

    t.replaced = [translator.get_state().translations[-1]]
    t.is_retrospective_command = True
    translator.translate_translation(t)
