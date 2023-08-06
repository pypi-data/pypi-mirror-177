# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['popcatapiwrapper', 'popcatapiwrapper.objects']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.7.2,<4.0.0', 'furo>=2022.9.29,<2023.0.0']

setup_kwargs = {
    'name': 'popcatapiwrapper',
    'version': '0.0.7',
    'description': 'PopCatWrapper is an asynchronous wrapper for https://popcat.xyz/api',
    'long_description': "\n\nAn async API wrapper around [popcat-api](https://popcat.xyz/api)\n\n\n### Get started || [Documentation](https://popcat-api.readthedocs.io/en/latest/)\n\n#### to get started, type this in your terminal\n```\npip install -U popcatapiwrapper\n```\n\n#### or to install the main branch\n```\npip install -U git+https://github.com/Infernum1/PopCatWrapper\n```\n###### (make sure you have [git](https://gitforwindows.org) installed)\n### Examples\n#### For a list of examples of each endpoint, take a look at the [examples directory](https://github.com/Infernum1/PopCatWrapper/tree/main/examples)\n\n\n##### If you plan to use the lib in a discord bot\n\n```py\nimport discord\nimport PopCatWrapper\n\nclient = PopCatWrapper.PopCatAPI()\nbot = discord.ext.commands.Bot()\n\n@bot.command()\nasync def element(element: str): #you can feed either the atomic number, symbol, or element name\n  image = await client.get_element_info(element)\n  await ctx.send(content=element.summary)\n```\n\n###### these are just examples! it's upto you how you want to use this lib.\n\n### Add `Infernum#7041` on discord for help\n\n#### You're welcome to make a Pull Request if you feel something can be improved :)\n",
    'author': 'Infernum1',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Infernum1/PopCatWrapper',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10',
}


setup(**setup_kwargs)
