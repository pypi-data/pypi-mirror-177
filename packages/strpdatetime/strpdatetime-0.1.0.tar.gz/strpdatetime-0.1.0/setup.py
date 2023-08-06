# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['strpdatetime']
install_requires = \
['textX>=3.0.0,<4.0.0']

setup_kwargs = {
    'name': 'strpdatetime',
    'version': '0.1.0',
    'description': "Parse strings into Python datetime objects; extends Python's datetime.strptime() with additional features.",
    'long_description': '# strpdatetime\n\nA replacement for `datetime.datetime.strptime` with super powers. `strpdatetime` is a drop-in replacement for `datetime.datetime.strptime` that adds a simplified regex-like syntax for finding and extracting date and time information from strings.\n\n## Why this package?\n\nA common use case is parsing date/time information from strings, for example filenames with\nthe date and time embedded in them. The standard library\'s `datetime.datetime.strptime` works\nwell if the string perfectly matches the format string, but does not work if the string\ncontains additional characters. For example, `datetime.datetime.strptime("IMG_1234_2022_11_20.jpeg", "%Y_%m_%d")` will fail with `ValueError: time data \'IMG_1234_2022_11_20.jpeg\' does not match format \'%Y_%m_%d\'`. To use `datetime.datetime.strptime` in this case, you would need to first parse the string to remove the extra characters.\n\nThird-party packages such as [dateutil](https://github.com/dateutil/dateutil) and [datefinder](https://github.com/akoumjian/datefinder) are more flexible but still fail to find the date in the above example and other common filename date/time formats.\n\n`strpdatetime` can find the date in the above example using `strpdatetime("IMG_1234_2022_11_20.jpeg", "^IMG_*_%Y_%m_%d")`\n\n## Installation\n\n`pip install strpdatetime`\n\nTo install from source, clone the repository, `pip install poetry`, and run `poetry install`.\n\n## Source Code\n\nThe source code is available on [GitHub](https://github.com/RhetTbull/strpdatetime).\n\n## Usage\n\n```pycon\n>>> import datetime\n>>> from strpdatetime import strpdatetime\n>>> dt = strpdatetime("IMG_1234_2022_11_20.jpeg","^IMG_*_%Y_%m_%d.*")\n>>> assert dt == datetime.datetime(2022,11,20)\n>>>\n```\n\n## Syntax\n\nIn addition to the standard `strptime` [format codes](https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes), `strpdatetime` supports the following:\n\n- *: Match any number of characters\n- ^: Match the beginning of the string\n- $: Match the end of the string\n- {n}: Match exactly n characters\n- {n,}: Match at least n characters\n- {n,m}: Match at least n characters and at most m characters\n- In addition to `%%` for a literal `%`, the following format codes are supported:\n    `%^`, `%$`, `%*`, `%|`, `%{`, `%}` for `^`, `$`, `*`, `|`, `{`, `}` respectively\n- |: join multiple format codes; each code is tried in order until one matches\n- Unlike the standard library, the leading zero is not optional for %d, %m, %H, %I, %M, %S, %j, %U, %W, and %V\n- For optional leading zero, use %-d, %-m, %-H, %-I, %-M, %-S, %-j, %-U, %-W, and %-V\n\n## Examples\n\n```pycon\n>>> from strpdatetime import strpdatetime\n>>> strpdatetime("IMG_1234_2022_11_20.jpg","^IMG_{4}_%Y_%m_%d")\ndatetime.datetime(2022, 11, 20, 0, 0)\n>>> strpdatetime("IMG_1234_2022_11_20.jpg","IMG_*_%Y_%m_%d")\ndatetime.datetime(2022, 11, 20, 0, 0)\n>>> strpdatetime("1234_05_06_2022_11_20","%Y_%m_%d$")\ndatetime.datetime(2022, 11, 20, 0, 0)\n>>> strpdatetime("1234_05_06_2022_11_20","IMG_*_%Y_%m_%d|%Y_%m_%d$")\ndatetime.datetime(2022, 11, 20, 0, 0)\n>>>\n```\n\n## Command Line\n\n`strpdatetime` includes a very simple command line interface. It can be used to test the regex-like syntax.\n\n```bash\n$ python -m strpdatetime "IMG_*_%Y_%m_%d" *.jpg\nIMG_2131_2022_11_20.jpg: 2022-11-20 00:00:00\nIMG_2132.jpg: time data \'IMG_2132.jpg\' does not match format \'IMG_*_%Y_%m_%d\'\nIMG_2134_2022_11_20.jpg: 2022-11-20 00:00:00\n```\n\n## License\n\nTo ensure backwards compatibility with the Python standard library, `strpdatetime` makes use of original code from the standard library and is thus licensed under the Python Software Foundation License, just as Python itself is.\n\n## Contributing\n\nContributions of all kinds are welcome! Please open an issue or pull request on [GitHub](https://github.com/RhetTbull/strpdatetime).\n',
    'author': 'Rhet Turnbull',
    'author_email': 'rturnbull+git@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
