# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['clean_menu']

package_data = \
{'': ['*']}

install_requires = \
['art>=5.7,<6.0',
 'colorama>=0.4.6,<0.5.0',
 'pynput>=1.7.6,<2.0.0',
 'termcolor>=2.1.0,<3.0.0']

setup_kwargs = {
    'name': 'clean-menu',
    'version': '0.1.2',
    'description': 'Minimal library fot making menus within the console',
    'long_description': '# Clean Menu\n\n## Table of content\n- [table of content](#Table-of-content)\n- [Installation](#Installation)\n- [Note](#Note)\n    - [Known issues](#Known-issues-)\n- [Use](#Use)\n    - [Create an instance](#Create-an-instance)\n    - [Bind actions to options](#Bind-actions-to-options)\n    - [Use the menu](#Use-the-menu)\n\n## Installation\nYou can install the package by running the following command :\n```python3 -m pip install --upgrade clean-menu``` \n\n## Note \n**Please note** that the package is currently in **beta** version and may encounter **bugs** or **unexpected behaviours** for which **I am not responsible**.\n\n#### Known issues : \n**Linux :**\n- The keys are captured but not intercepted\n- navigate in the menu browse your terminal history\n- when you press `enter` to validate, it can trigger one of your previous commands\n\nI tried the same fix than windows but I haven\'t tested it yet.\n\n\n**Windows :**\n- To disable key propagation, I set up a filter using the `win32_event_filter` kwarg\n- It will block `arrows up and down`, `enter`, and `space` (only if you use the `space` key to validate)\nThese issues are all related, and a safe way to use it would be to override the default `validation_key` and set it to `space`.\n\n**MacOS :**\nI actually don\'t have a mac to test it, but I think it won\'t work as expected, because filters are not the same as windows. Furthermore, keyboard monitoring requires elevated (*root*) privileges.\n\n## Use \n\n### Create an instance \nSimply import the `Menu` object from the package into your script and start use it.\n```py\nfrom clean_menu import Menu\n\nmenu = Menu(title,  # menu title\n            options,  # list of options\n            subtilte,  # menu subtitle\n            subtitle_color=None,  # subtitle color\n            exit_text="Exit",  # exit text\n            exit_function=sys.exit,  # exit function called when\n            art_title=True,  # enable/disable ascii art title\n            title_font="",  # ascii art title font\n            default_pointer_index=0,  # default option index in option list\n            margin="    ",  # characters before options, better result when longer than pointer\n            title_color="red",  # title color\n            text_color="white",  # color for not pointed options\n            pointer_style=None,  # pointer style, if None, no pointer\n            pointer_color="green",  # pointer color\n            pointed_text_color="white",  # pointed option text color\n            pointed_background_color="None",  # pointed option background color\n            validation_key="enter",  # key to validate an option\n            )\n```\n\nso the following code :\n```py\nfrom clean_menu import Menu\n\nmenu = Menu("Test",\n            ["Option 1", "Option 2", "Option 3"],\n            title_font="rounded",\n            title_color="blue",\n            margin="        ",\n            pointer_style=["==>", "<=="],\n            pointer_color="red",\n            pointed_background_color="white",\n            pointed_text_color="green",\n            exit_text="Quit me forever...",\n            text_color="magenta",\n            validation_key="enter",\n            )\n```\nwill render this :\n\n\n[Click to see the image (redirection)](http://home.petchou.ovh/test1.png)\n\n### Bind actions to options:\nYou can attach a function or method to each action in the menu, except for the `exit`, which is  handled by the parameter `exit_function`.\nTo do so, you just have to call the `bind()` method, with the index of the option and the function as parameters.\n\n```py\nmenu.bind(0, lambda: print("Option 1"))\nmenu.bind(1, lambda: print("Option 2"))\nmenu.bind(2, lambda: print("Option 3"))\n```\n\nin case the given index is not handled, you will get an error like this :\n\n```py\nmenu.bind(3, lambda: print("Option 4"))\n=======================================\nBind Error: Index out of range\nList of available options to assign functions :\n0 : Option 1                                    # you will see all the options\n1 : Option 2                                    # available for binding and their\n2 : Option 3                                    # index to specify as parameter\nTraceback (most recent call last):\n  File "c:\\Users\\mathe\\Documents\\code\\cleanMenu\\clean-menu\\main.py", line 158, in <module>\n    example()\n  File "c:\\Users\\mathe\\Documents\\code\\cleanMenu\\clean-menu\\main.py", line 152, in example\n    menu.bind(3, lambda: print("Option 4"))\n  File "c:\\Users\\mathe\\Documents\\code\\cleanMenu\\clean-menu\\main.py", line 114, in bind\n    raise IndexError\nIndexError\n```\n\n### Use the menu\nYou have to options to use the menu :\n- You can bind functions to options and let the menu execute them with the  `run` method\n- you can just execute the menu screen to get the index of the selected option\n\nexamples :\n\n```python\nmenu.run() # and that\'s pretty much all you need to do...\nindex = menu.get_index() # will return the index of the selected option\t\nprint(menu.options[index]) # should display the option you selected\n```\n',
    'author': 'PetchouDev',
    'author_email': 'petchou91d@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/PetchouDev/cleanMenu',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
