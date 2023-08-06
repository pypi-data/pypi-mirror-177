# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['crossandra']

package_data = \
{'': ['*']}

install_requires = \
['result>=0.8.0,<0.9.0']

setup_kwargs = {
    'name': 'crossandra',
    'version': '1.2.0',
    'description': 'A simple tokenizer operating on enums with a decent amount of configuration',
    'long_description': '# Crossandra\nCrossandra is a simple tokenizer operating on enums with a decent amount of configuration.\n\n## Installation\nCrossandra is available on PyPI and can be installed with pip, or any other Python package manager:\n```sh\n$ pip install crossandra\n```\n(Some systems may require you to use `pip3`, `python -m pip`, or `py -m pip` instead)\n\n## License\nCrossandra is licensed under the MIT License.\n\n## Reference\n### `Crossandra`\n```py\nCrossandra(\n    token_source: type[Enum] = Empty,\n    *,\n    ignore_whitespace: bool = False,\n    ignored_characters: str = "",\n    suppress_unknown: bool = False,\n    rules: list[Rule | RuleGroup] | None = None\n)\n```\n- `token_source`: an enum containing all possible tokens (defaults to an empty enum)\n- `ignore_whitespace`: whether spaces, tabs, newlines etc. should be ignored\n- `ignored_characters`: characters to skip during tokenization\n- `suppress_unknown`: whether unknown tokens should continue without throwing an error\n- `rules`: a list of additional rules to use\n\nThe enum takes priority over the rule list.\n\n---\n\nWhen all tokens are of length 1 and there are no additional rules, Crossandra will use a simpler tokenization method (the so called Fast Mode).\n\n> **Example:** Tokenizing noisy Brainfuck code *(tested on MacBook Air M1 (256/16))*\n\n```py\n# Setup\nfrom random import choices\nfrom string import punctuation\n\nprogram = "".join(choices(punctuation, k=...))\n```\n\nk      | Default  | Fast Mode | Speedup\n:---:  | :---:    | :---:     | :---:\n10     | 0.00004s | 0.00002s  | 2x\n100    | 0.00016s | 0.00003s  | 5.3x\n1000   | 0.0015s  | 0.00013s  | 11.5x\n10000  | 0.014s   | 0.0009s   | 15.6x\n100000 | 0.29s    | 0.009s    | 32.2x\n\n\n### `Rule`\n```py\nRule[T](\n    pattern: str,\n    converter: Callable[[str], T] | bool = True,\n    flags: RegexFlag | int = 0\n)\n```\nUsed for defining custom rules. `pattern` is a regex pattern to match (`flags` can be supplied).  \nWhen `converter` is a callable, it\'s used on the matched substring.  \nWhen `converter` is `True`, it will directly return the matched substring.  \nWhen `converter` is `False`, it will not include the matched substring in the token list.\n\n### `RuleGroup`\n```py\nRuleGroup(rules: tuple[Rule[Any], ...])\n```\nUsed for storing multiple Rules in one object. Can be constructed by ORing two or more Rules.\n\n### `common`\nThe `common` submodule is a collection of commonly used patterns.\n\nRules:\n- CHAR (e.g. `\'h\'`)\n- LETTER (e.g. `m`)\n- WORD (e.g. `ball`)\n- SINGLE_QUOTED_STRING (e.g. `\'nice fish\'`)\n- DOUBLE_QUOTED_STRING (e.g. `"hello there"`)\n- C_NAME (e.g. `crossandra_rocks`)\n- NEWLINE (`\\n`; `\\r\\n` is converted to `\\n` before tokenization)\n- DIGIT (e.g. `7`)\n- HEXDIGIT (e.g. `c`)\n- DECIMAL (e.g. `3.14`)\n- INT (e.g. `2137`)\n- SIGNED_INT (e.g. `-1`)\n- FLOAT (e.g. `1e3`)\n- SIGNED_FLOAT (e.g. `+4.3`)\n\nRuleGroups:\n- STRING (`SINGLE_QUOTED_STRING | DOUBLE_QUOTED_STRING`)\n- NUMBER (`INT | FLOAT`)\n- SIGNED_NUMBER (`SIGNED_INT | SIGNED_FLOAT`)\n\n\n## Examples\n```py\nfrom enum import Enum\nfrom crossandra import Crossandra\n\nclass Brainfuck(Enum):\n    ADD = "+"\n    SUB = "-"\n    LEFT = "<"\n    RIGHT = ">"\n    READ = ","\n    WRITE = "."\n    BEGIN_LOOP = "["\n    END_LOOP = "]"\n\nbf = Crossandra(Brainfuck, suppress_unknown=True)\nprint(*bf.tokenize("cat program: ,[.,]"), sep="\\n")\n# Brainfuck.READ\n# Brainfuck.BEGIN_LOOP\n# Brainfuck.WRITE\n# Brainfuck.READ\n# Brainfuck.END_LOOP\n```\n```py\nfrom crossandra import Crossandra, Rule, common\n\ndef hex2rgb(hex_color: str) -> tuple[int, int, int]:\n    r, g, b = (int(hex_color[i:i+2], 16) for i in range(1, 6, 2))\n    return r, g, b\n\nt = Crossandra(\n    ignore_whitespace=True,\n    rules=[\n        Rule(r"#[0-9a-fA-F]+", hex2rgb),\n        common.WORD\n    ]\n)\n\ntext = "My favorite color is #facade"\nprint(t.tokenize(text))\n# [\'My\', \'favorite\', \'color\', \'is\', (250, 202, 222)]\n```\n```py\n# Supporting Samarium\'s numbers and arithmetic operators\nfrom enum import Enum\nfrom crossandra import Crossandra, Rule\n\ndef sm_int(string: str) -> int:\n    return int(string.replace("/", "1").replace("\\\\", "0"), 2)\n\nclass Op(Enum):\n    ADD = "+"\n    SUB = "-"\n    MUL = "++"\n    DIV = "--"\n    POW = "+++"\n    MOD = "---"\n\nsm = Crossandra(\n    Op,\n    ignore_whitespace=True,\n    rules=[Rule(r"(?:\\\\|/)+", sm_int)]\n)\n\nprint(*sm.tokenize(r"//\\ ++ /\\\\/ --- /\\/\\/ - ///"))\n# 6 Op.MUL 9 Op.MOD 21 Op.SUB 7\n```',
    'author': 'trag1c',
    'author_email': 'trag1cdev@yahoo.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/trag1c/crossandra',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}
from _build import *
build(setup_kwargs)

setup(**setup_kwargs)
