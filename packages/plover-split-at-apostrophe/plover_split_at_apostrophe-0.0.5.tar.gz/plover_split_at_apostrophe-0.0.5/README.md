# Plover Split at Apostrophe

Companion plugin for BépoSténo - split words at the apostrophe key.


# The premise:
For certain languages, articles that go placed before a noun or adjective that starts with a vowel (eg. `le appétit`) can get contracted (into `l'appétit`).
This means that contracting an expression like `l'appétit` would take the steno strokes from `L{apostropheKey}/A/PE/TI` (pronounced `le appétit`) to `L{apostropheKey}A/PE/TI`. Given that french and italian are full of these little contractions, it would save a lot of keystrokes to be able to have contracted articles *and* vowel-starting words into a single stroke. A few more examples:
`L{apostropheKey}An`: `l'an` (tr: the year)
`J{apostropheKey}A/T*Or`: `j'adore`


# functionality:
Having apostrophe-separated strokes assumes the following:
1. *The apostrophe-key must act as a word-boundary at its position in the steno-order*. Using my current steno-order: `S K P M T F * R N L {apostropheKey} Y O ^ E È A À U I l É n $ B D C # ß` - any stroke following the pattern: `[SKPMTFRNL]{apostropheKey}[YO^EÈAÀUIlÉn$BDC#ß]` would be interpreted by plover as `[SKPMTFRNL]{apostropheKey}{^}[YO^EÈAÀUIlÉn$BDC#ß]`.
2. *The strokes on the left-side of the apostrophe-key terminate a word, the ones on the right-side start a new one*. 
2. *Plover needs a notation to represent the keys on either side of the apostrophe-key as strokes*. This is similar to the current way of handling conditionals that plover has (`{=REGEXP/TRANSLATION_IF_MATCH/TRANSLATION_IF_NOT}`) - with the notable difference that capture groups from the `=REGEXP` would have to be re-usable in the `TRANSLATION_IF_MATCH`.

## Usage 

Choose a key to be your apostrophe key. Set it in your `system.py` in the steno order. In most syllabic steno systems, such as GrandJean, that would be after the attack consonants, and before the vowels.
From there, any stroke that you want to split at the apostrophe key needs to call the plugin, using the following format in the dictionnary:
```
"<start_of_stroke><apostrophe_key><rest_of_stroke>": "=split_word_at_apostrophe",
```
This is less than ideal, as it forces the user to write up every stroke that will have to be split into to the dictionnary. Luckily though, I've found through experience that there are not so many strokes that will require this.
