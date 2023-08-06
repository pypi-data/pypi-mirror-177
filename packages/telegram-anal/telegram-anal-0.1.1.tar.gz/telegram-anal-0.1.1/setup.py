# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['telenal']

package_data = \
{'': ['*']}

install_requires = \
['Pyrogram>=2.0.59,<3.0.0',
 'TgCrypto>=1.2.4,<2.0.0',
 'matplotlib>=3.6.1,<4.0.0',
 'nltk>=3.7,<4.0',
 'numpy>=1.23.4,<2.0.0',
 'pandas>=1.5.1,<2.0.0',
 'python-dotenv>=0.21.0,<0.22.0',
 'scipy>=1.9.3,<2.0.0',
 'stop-words>=2018.7.23,<2019.0.0',
 'wordcloud>=1.8.2,<2.0.0']

setup_kwargs = {
    'name': 'telegram-anal',
    'version': '0.1.1',
    'description': 'A fun tool to play with Telegram chats',
    'long_description': '# Telegram analysis ✨ \n\nTelegram analysis is a python package that helps you have fun and make sense of different chat data you have. \nBased on pyrogram, its mission is to help you have fun with Telegram and it\'s functions.\nWhether it is about playing with your group chat dialogs or analysing the group dynamic of your business, personal chats or even your saved messages.\n\nBe creative and build on top of ready solutions! 🧠\n\nCurrent functionality (version 0.1.1):\n\n✨🌠 `wordcloud_json()`Create fun wordclouds out of chats \n\n💬🗣 `who_breaks_silence_json()` Analyze who tends to break the silence in the chats and write first\n\n🤍❤ `measure_top_reactions()` measure who\'s messages are most reacted to and choose specific reactions!\n\n\n___\n### Installation:\n```\npip install telegram-anal\n```\n\n### 🛠 Setup:\n\nThis library uses Pyrogram for handling Telegram, so you will need to authenticate standardly by:\n1. Create an app and copy your api_id and api_hash from https://my.telegram.org/\n\n### Example:\n```python\nimport asyncio\nfrom telenal.client import Client\nfrom telenal.reactions import measure_top_reactions\nfrom telenal.teleplotter import plot_bars_from_dict\n\n\nasync def main():\n    client = Client("my_account", "your_api_id", "your_api_hash")\n    tops = await measure_top_reactions(\n        client,\n        chat_name="Family chat :)",\n        search_emojis=["😁", "💪", "👍"],\n    )\n    plot_bars_from_dict(tops)  # <-- get a bar chart out of the box\n\n\nif __name__ == "__main__":\n    asyncio.run(main())\n\n```\n\nThe library is newly born and needs creative and energetic support. Feel free to contribute!\n\nIdeas for future functionality:\n\n1. Analyze your activity based on sent chatting to identify your chatting patterns\n2. Save messages deleted by someone that texted you and save the secret they wanted to hide\n3. Measure user profiles to identify persons\' most popular tones (NLP may be needed)\n4. Predict when a user is prone to leave a community based on real cases (ML)\n\nRemember to have fun! :)\n\nThis software is made purely for fun. Any illegal or amoral misuse of the software does not make the authors responsible for the consequences. \n\nYours,\nVlad Bilyk\n',
    'author': 'Vladyslav Bilyk',
    'author_email': 'vladozeransky2k@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Salz0/Telegram-anal',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
