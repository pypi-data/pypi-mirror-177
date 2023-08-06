# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vermils',
 'vermils.asynctools',
 'vermils.collections',
 'vermils.gadgets',
 'vermils.gadgets.sidelogging',
 'vermils.io',
 'vermils.io.aio',
 'vermils.io.puller',
 'vermils.react',
 'vermils.tensorflow',
 'vermils.tensorflow.callbacks',
 'vermils.tensorflow.inspect',
 'vermils.tensorflow.layers',
 'vermils.tensorflow.metrics',
 'vermils.tensorflow.models']

package_data = \
{'': ['*']}

install_requires = \
['nest-asyncio>=1.5.6,<2.0.0']

setup_kwargs = {
    'name': 'vermils',
    'version': '0.0.1',
    'description': '',
    'long_description': "# Vermils Magic Pocket 4 Python\n\n## Installation\n\n### Basic\n\n```Bash\npip install vermils\n```\n\n### With HTTP support\n\nRequired by `vermils.io.puller`\n\n```Bash\npip install vermils[http]\n```\n\n### With full support\n\n```Bash\npip install vermils[all]\n```\n\n## Importing\n\n```Python\nimport vermils\n```\n\n## Table of Contents\n\n**Most of the codes are easy to understand or well documented, the documentation is only for the more complex ones.**\n\n### `vermils.asynctools`\n\nTools for asynchronous programming.\n\n- `sync_await`: Run async functions in a sync environment.\n- `ensure_async`: Wraps a function/generator into an async function if it's a sync one.\n- `to_async`: Wraps a function into an async function blindly.\n- `to_async_gen`: Wraps a generator into an async generator blindly.\n- `get_create_loop`: Get the current event loop or create a new one if there isn't one. Works in another thread unlike `asyncio.get_event_loop`.\n- `async_run`: Run sync functions asynchronously in another thread without wrapping first.\n- `AsinkRunner`: A class that runs sync functions asynchronously and sequentially in another thread.\n\nDocumentation: [vermils.asynctools](./Python/docs/asynctools.md)\n\n### `vermils.collections`\n\nCollections of useful classes.\n\n- `fridge`: Make things immutable and hashable.\n  - `FrozenDict`: A dict that is immutable and hashable.\n  - `FrozenList`: A list that is immutable and hashable. Basically a tuple but can be compared with lists.\n  - `freeze`: Recursively freeze a object.\n- `StrChain`: A simple way to create strings. Extremely useful.\n- `ObjDict`: A dict that can be accessed like an object.\n\nDocumentation: [vermils.asynctools](./Python/docs/collections.md)\n\n### `vermils.gadgets`\n\nSnippets of code that I am too lazy to categorize.\n\n- `sidelogging.SideLogger`: Move any `LoggerLike` into another thread.\n- `MonoLogger`: Log different levels of messages to different files.\n- `stringify_keys`: Recursively convert all keys in a dict to strings.\n- `supports_in`: Check if an object supports `in`.\n- `mimics`: A decorator that makes a function mimic another function.\n- `sort_class`: Sort class by inheritance, child classes first.\n- `str_to_object`: Convert a string to an object.\n- `real_dir`: Get the real directory of a file. Auto expand `~` and env vars.\n- `real_path`: Get the real path of a file. Auto expand `~` and env vars.\n- `version_cmp`: Compare two SemVer strings.\n- `to_ordinal`: Convert an integer to its ordinal form.\n- `selenium_cookies_to_jar`: Convert Selenium cookies to a `http.cookiejar.CookieJar` object.\n\nDocumentation: [vermils.gadgets](./Python/docs/gadgets.md)\n\n### `vermils.io`\n\nTools for I/O.\n\n- `aio`: Async IO\n  - `os`: Async version of some `os` functions.\n    - `fsync`\n    - `link`\n    - `symlink`\n    - `mkdir`\n    - `makedirs`\n    - `remove`\n    - ... and more\n  - `path`: Async version of some `os.path` functions\n    - `exists`\n    - `isdir`\n    - `isfile`\n    - `islink`\n    - ... and more\n- `puller`: A multithread async downloader module\n  - `AsyncPuller`: A class that downloads files asynchronously.\n  - `Modifier`: A class that modifies the behavior of the puller, e.g show progress bar.\n- `DummyFileStream`: A dummy file stream that does nothing.\n- `DummyAioFileStream`: A dummy async file stream that does nothing.\n\nDocumentation: [vermils.io](./Python/docs/io.md)\n\n### `vermils.react`\n\nA simple event system.\n\n- `ActionChain`: A chain of functions that can be executed in order or in parallel.\n- `ActionCentipede`: The output of a function becomes the input of the next function.\n- `EventHook`: A simple event hook, binds events to chains of functions.\n\nDocumentation: [vermils.react](./Python/docs/react.md)\n\n### `vermils.tensorflow`\n\nTensorFlow related tools.\n\n- `inspect`\n- `callbacks`\n- `layers`\n- `metrics`\n- `models`\n\nDocumentation: [vermils.tensorflow](./Python/docs/tensorflow.md)\n",
    'author': 'VermiIIi0n',
    'author_email': 'dungeon.behind0t@icloud.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/VermiIIi0n/VermilsMagicPocket',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
