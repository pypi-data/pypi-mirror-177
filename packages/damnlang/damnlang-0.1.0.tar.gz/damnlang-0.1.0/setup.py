# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['damn', 'damn.definition', 'damn.lib', 'damn.value']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.3,<4.0.0']

setup_kwargs = {
    'name': 'damnlang',
    'version': '0.1.0',
    'description': 'Damn',
    'long_description': '# damn\n\n**damn** (desperately agonizing math noobs) is a language to help you write knowledge assessment test generators.\n\nLanguage will help you in variables constraints declaration and generate unique pairs of data. Then, the generated pair of variables can be evaluated with the formula (via wolframalpha integration).\n\nSyntax:\n\n```damn\n1 > x > 10\ny in [1, 2, 3]\n(a, b) in [(4, 5), (1, 10)]\n```\n\n## Example\n\nConstraints:\n\n```damn\n10 > a > 20\n(v1, v2) in [(1, 2), (4, 8)]\n```\n\nFormula:\n\n```damn\na = (v2 - v1)/t\n```\n\nMaking a test:\n\n```python\nfrom damn import DefinitionSet, Calculator\nimport asyncio\n\ncalculator = Calculator(["DEMO"])\n\nasync def main():\n    def_set = DefinitionSet.from_expressions([\n        "10 > a > 20", \n        "(v1, v2) in [(1, 2), (4, 8)]"\n    ])\n    data = def_set.get_data()\n    print(\n        "What is delta t if " + \n        ", ".join(\n            (f"{k} = {v.get_common_representation()}" for k, v in data.items())\n        )\n    )\n    result = await calculator.calculate(data, "a = (v2 - v1)/t")\n    answer = float(input("your answer > "))\n    if answer == result.v:\n        print("great!!")\n        return\n    print(f"BAD student. the right answer is {result.v}")\n\nasyncio.run(main())\n```',
    'author': 'timoniq',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
