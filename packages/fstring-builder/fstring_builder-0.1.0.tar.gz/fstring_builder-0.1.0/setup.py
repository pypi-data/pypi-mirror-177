# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fstring_builder']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'fstring-builder',
    'version': '0.1.0',
    'description': 'A human friendly format string builder',
    'long_description': '# FString Builder\n\nA simple Python library to enhance the API of the native Python f-string syntax.  \n\nThis came about from needing to often refer back to the native [format string syntax](https://docs.python.org/3/library/string.html#format-string-syntax).  \nI found that configuring formatting options within the program was tricky and tedious.  \n\nFor example, if I wanted a user-defined width for a given line, it was awkward to include it in every instance of \nthat field.  Many mistakes were made.\n\nThe API so far is what resulted after prototyping out the idea on a couple personal projects.  This ended up working \nreally well for the line formatting portions, I think it could be useful to others.  \n\n## Installation\n\nInstall via pip: \n\n\n```\n$ pip install fstring-builder\n```\n\n## Interface\n\nThe idea is to have a main `FormatString` object that is able to collect and manage items comprising that ultimate \nstring.  This object can build a format-ready string from its items.   \n\nEach item is either a simple string-like object that gets concatenated in place, or it is a `ReplacementField`, \ntraditionally noted in f-strings with a format spec inside curly braces `{<format_syntax>}`.\n\nThe `ReplacementField` accepts all the options from a normal format string.  By default, they are all `None`:\n\n| **Name**     | **Type**               | **Description**                                      |\n| ------------ | ---------------------- | ---------------------------------------------------- |\n| `name`       | `str`                  | Keyword name variable for the field                  |\n| `conversion` | `[\'s\', \'r\', \'a\']`      | Convert the field to a string, repr, or ascii format |\n| `fill`       | `str`                  | Single string character to use as a fill             |\n| `align`      | `[\'<\', \'>\', \'^\', \'=\']` | Align text left, right, center, or numeric-padded    |\n| `sign`       | `[\'+\', \'-\', \' \']`      | Sign characters for numeric types                    |\n| `z`          | `bool`                 | Coerce floating point numbers to positive 0          |\n| `hashtag`    | `bool`                 | Use \'alternate\' form for conversion                  |\n| `zero`       | `bool`                 | Pad numeric numbers with `0`                         |\n| `width`      | `int`                  | Set a character width value for the field            |\n| `grouping`   | `[\',\', \'_\']`           | Set the numeric grouping characters                  |\n| `precision`  | `int`                  | Floating point precision value                       |\n| `type`       | `str`                  | Format type characters, i.e. `d`, `n`, or `f`        |\n\nOnce your field parameters are set, each field can be built using the `.build()` method.  Alternatively, each `FormatString` can build all its elements using its own `.build()`.\n\nThe result of a `.build()` is a *format-ready* string, ie a string that you can call `.format(**kwargs)` on.  The `FormatString` object has a convenience function `.format(**kwargs)` that builds and formats itself with any parameters passed.\n\n## Example\n\nThe following example creates a format ready string for a monetary currency.  It could be expanded to provide for a more generic locale-aware currency formatter \n\n```python\nimport fstring_builder as fsb\n\n# Simple currency format string\n# f`${qty:>12,.2f}`\n\ncurrency_fmt = fsb.FormatString(\n    "$", \n    fsb.ReplacementField(\n        name="qty",\n        grouping=",",\n        align="right",\n        width=12,\n        precision=2,\n        type="float"\n    )\n)\n\nprint(currency_fmt)                     # "${qty:>12,.2f}"\nprint(currency_fmt.format(qty=312.5))   # "$      312.50"\nprint(currency_fmt.format(qty=15324))   # "$   15,324.00"\n\ncurrency_fmt._width = 10\nprint(currency_fmt.format(qty=15324))   # "$ 15,324.00"\n```\n\n### Chainable Methods\n\nThe parameters for `ReplacementField` objects can also be set after construction via methods.  They are all chainable, allowing for something like:\n\n```python\nimport fstring_builder as fsb\n\ncurrency_fmt = fsb.FormatString("$",\n    fsb.ReplacementField(name="qty")\n        .align(fsb.Align.RIGHT)\n        .grouping(fsb.Grouping.COMMA)\n        .width(12)\n        .precision(2)\n        .type(fsb.Type.Float.NUMERIC)\n)\n\ncurrency_fmt.build()\n\nprint(currency_fmt.format(qty=15324))       # "$   15,324.00"\nprint(currency_fmt.format(qty=-2157.25))    # "$   -2,157.25"\nprint(currency_fmt.format(qty=0))           # "$        0.00"\n```',
    'author': 'Tim van Boxtel',
    'author_email': 'tim@vanboxtel.ca',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
