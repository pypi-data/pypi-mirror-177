# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['together_web3']

package_data = \
{'': ['*']}

install_requires = \
['dacite>=1.6.0,<2.0.0', 'web3>=5.30.0,<6.0.0']

setup_kwargs = {
    'name': 'together-web3',
    'version': '0.1.0',
    'description': '',
    'long_description': '# @togethercomputer/together-web3.py [![build](https://github.com/togethercomputer/together-web3.py/actions/workflows/build.yml/badge.svg)](https://github.com/togethercomputer/together-web3.py/actions/workflows/build.yml)\n\n```python\nfrom together_web3.computer import LanguageModelInferenceRequest\nfrom together_web3.together import TogetherWeb3\n\ntogether_web3 = TogetherWeb3()\nresult = await together_web3.language_model_inference(\n    from_dict(\n        data_class=LanguageModelInferenceRequest,\n        data={\n            "model": "gpt2",\n            "prompt": "George Washington was the first",\n        }\n    ),\n)\nprint("result", result)\n```\n\nSee [examples/example.py](examples/example.py)\n\n### Generate an image\n\n```console\npython examples/example.py "Rainbow unicorn" "StableDiffusion" \\\n  | grep image_base64 | cut -d\\" -f4 | base64 -d > x.jpg && open x.jpg\n```\n\n',
    'author': 'together',
    'author_email': 'together@together.xyz',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/togethercomputer/web3.py',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.2,<3.11',
}


setup(**setup_kwargs)
