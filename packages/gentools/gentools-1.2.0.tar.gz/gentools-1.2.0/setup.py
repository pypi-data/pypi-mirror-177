# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['gentools']

package_data = \
{'': ['*']}

extras_require = \
{':python_version < "3.8"': ['importlib-metadata>=1,<5']}

setup_kwargs = {
    'name': 'gentools',
    'version': '1.2.0',
    'description': 'Tools for generators, generator functions, and generator-based coroutines',
    'long_description': "Gentools\n========\n\n.. image:: https://img.shields.io/pypi/v/gentools.svg?style=flat-square\n    :target: https://pypi.python.org/pypi/gentools\n\n.. image:: https://img.shields.io/pypi/l/gentools.svg?style=flat-square\n    :target: https://pypi.python.org/pypi/gentools\n\n.. image:: https://img.shields.io/pypi/pyversions/gentools.svg?style=flat-square\n    :target: https://pypi.python.org/pypi/gentools\n\n.. image:: https://img.shields.io/travis/ariebovenberg/gentools.svg?style=flat-square\n    :target: https://travis-ci.org/ariebovenberg/gentools\n\n.. image:: https://img.shields.io/codecov/c/github/ariebovenberg/gentools.svg?style=flat-square\n    :target: https://coveralls.io/github/ariebovenberg/gentools?branch=master\n\n.. image:: https://img.shields.io/readthedocs/gentools.svg?style=flat-square\n    :target: http://gentools.readthedocs.io/en/latest/?badge=latest\n\n\nTools for generators, generator functions, and generator-based coroutines.\n\nKey features:\n\n* Create reusable generators\n* Compose generators\n* Build python 2/3-compatible generators (``gentools`` version <1.2 only)\n\nInstallation\n------------\n\n.. code-block:: bash\n\n   pip install gentools\n\nExamples\n--------\n\n- Make generator functions reusable:\n\n.. code-block:: python\n\n   >>> @reusable\n   ... def countdown(value, step):\n   ...     while value > 0:\n   ...         yield value\n   ...         value -= step\n\n   >>> from_3 = countdown(3, step=1)\n   >>> list(from_3)\n   [3, 2, 1]\n   >>> list(from_3)\n   [3, 2, 1]\n   >>> isinstance(from_3, countdown)  # generator func is wrapped in a class\n   True\n   >>> from_3.step  # attribute access to arguments\n   1\n   >>> from_3.replace(value=5)  # create new instance with replaced fields\n   countdown(value=5, step=1)  # descriptive repr()\n\n- map a generator's ``yield``, ``send``, and ``return`` values:\n\n.. code-block:: python\n\n   >>> @map_return('final value: {}'.format)\n   ... @map_send(int)\n   ... @map_yield('the current max is: {}'.format)\n   ... def my_max(value):\n   ...     while value < 100:\n   ...         newvalue = yield value\n   ...         if newvalue > value:\n   ...             value = newvalue\n   ...     return value\n\n   >>> gen = my_max(5)\n   >>> next(gen)\n   'the current max is: 5'\n   >>> gen.send(11.3)\n   'the current max is: 11'\n   >>> gen.send(104)\n   StopIteration('final value: 104')\n\n- relay a generator's yield/send interactions through another generator:\n\n.. code-block:: python\n\n   >>> def try_until_positive(outvalue):\n   ...     value = yield outvalue\n   ...     while value < 0:\n   ...         value = yield 'not positive, try again'\n   ...     return value\n\n   >>> @relay(try_until_positive)\n   ... def my_max(value):\n   ...     while value < 100:\n   ...         newvalue = yield value\n   ...         if newvalue > value:\n   ...             value = newvalue\n   ...     return value\n\n   >>> gen = my_max(5)\n   >>> next(gen)\n   5\n   >>> gen.send(-4)\n   'not positive, try again'\n   >>> gen.send(-1)\n   'not positive, try again'\n   >>> gen.send(8)\n   8\n   >>> gen.send(104)\n   StopIteration(104)\n\n- make python 2/3 compatible generators with ``return``. \n  (`gentools` version <1.2 only)\n\n.. code-block:: python\n\n   >>> @py2_compatible\n   ... def my_max(value):\n   ...     while value < 100:\n   ...         newvalue = yield value\n   ...         if newvalue > value:\n   ...             value = newvalue\n   ...     return_(value)\n",
    'author': 'Arie Bovenberg',
    'author_email': 'a.c.bovenberg@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/ariebovenberg/gentools',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
