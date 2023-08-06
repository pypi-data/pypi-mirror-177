#!/usr/bin/env python
from typing import *
import itertools
import functools
import re

from plover.engine import StenoEngine
from plover.translation import Translator, Stroke, Translation
from plover.formatting import _Context, _Action, _atom_to_action, _translation_to_actions
import os

def split_word_at_apostrophe(translator: Translator, stroke: Stroke, cmdline: str):
    apostrophe_postition = stroke.steno_keys.index("H")
    if apostrophe_postition > -1:
        translator.translate_stroke(
            Stroke(stroke.steno_keys[0:apostrophe_postition+1]))
        translator.translate_stroke(
            Stroke(stroke.steno_keys[apostrophe_postition+1:]))
