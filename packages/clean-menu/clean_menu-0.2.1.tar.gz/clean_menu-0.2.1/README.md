# Clean Menu

## Table of content
- [table of content](#Table-of-content)
- [Installation](#Installation)
- [Note](#Note)
    - [Known issues](#Known-issues-)
- [Use](#Use)
    - [Create an instance](#Create-an-instance)
    - [Bind actions to options](#Bind-actions-to-options)
    - [Use the menu](#Use-the-menu)

## Installation
You can install the package by running the following command :
```python3 -m pip install --upgrade clean-menu``` 

## Note 
**Please note** that the package is currently in **beta** version and may encounter **bugs** or **unexpected behaviours** for which **I am not responsible**.

#### Known issues : 
**Linux :**
- The keys are captured but not intercepted
- navigate in the menu browse your terminal history
- when you press `enter` to validate, it can trigger one of your previous commands

I tried the same fix than windows but I haven't tested it yet.


**Windows :**
- To disable key propagation, I set up a filter using the `win32_event_filter` kwarg
- It will block `arrows up and down`, `enter`, and `space` (only if you use the `space` key to validate)
These issues are all related, and a safe way to use it would be to override the default `validation_key` and set it to `space`.

**MacOS :**
I actually don't have a mac to test it, but I think it won't work as expected, because filters are not the same as windows. Furthermore, keyboard monitoring requires elevated (*root*) privileges.

## Use 

### Create an instance 
Simply import the `Menu` object from the package into your script and start use it.
```py
from clean_menu import Menu

menu = Menu(title,  # menu title
            options,  # list of options
            subtitle="",  # menu subtitle
            subtitle_color=None,  # subtitle color
            exit_text="Exit",  # exit text
            exit_function=sys.exit,  # exit function called when
            art_title=True,  # enable/disable ascii art title
            title_font="",  # ascii art title font
            default_pointer_index=0,  # default option index in option list
            margin="    ",  # characters before options, better result when longer than pointer
            title_color="red",  # title color
            text_color="white",  # color for not pointed options
            pointer_style=None,  # pointer style, if None, no pointer
            pointer_color="green",  # pointer color
            pointed_text_color="white",  # pointed option text color
            pointed_background_color="None",  # pointed option background color
            validation_key="enter",  # key to validate an option
            )
```

so the following code :
```py
from clean_menu import Menu

menu = Menu("Test",
            ["Option 1", "Option 2", "Option 3"],
            title_font="rounded",
            title_color="blue",
            margin="        ",
            pointer_style=["==>", "<=="],
            pointer_color="red",
            pointed_background_color="white",
            pointed_text_color="green",
            exit_text="Quit me forever...",
            text_color="magenta",
            validation_key="enter",
            )
```
will render this :


[Click to see the image (redirection)](http://home.petchou.ovh/test1.png)

### Bind actions to options:
You can attach a function or method to each action in the menu, except for the `exit`, which is  handled by the parameter `exit_function`.
To do so, you just have to call the `bind()` method, with the index of the option and the function as parameters.

```py
menu.bind(0, lambda: print("Option 1"))
menu.bind(1, lambda: print("Option 2"))
menu.bind(2, lambda: print("Option 3"))
```

in case the given index is not handled, you will get an error like this :

```py
menu.bind(3, lambda: print("Option 4"))
=======================================
Bind Error: Index out of range
List of available options to assign functions :
0 : Option 1                                    # you will see all the options
1 : Option 2                                    # available for binding and their
2 : Option 3                                    # index to specify as parameter
Traceback (most recent call last):
  File "c:\Users\mathe\Documents\code\cleanMenu\clean-menu\main.py", line 158, in <module>
    example()
  File "c:\Users\mathe\Documents\code\cleanMenu\clean-menu\main.py", line 152, in example
    menu.bind(3, lambda: print("Option 4"))
  File "c:\Users\mathe\Documents\code\cleanMenu\clean-menu\main.py", line 114, in bind
    raise IndexError
IndexError
```

### Use the menu
You have to options to use the menu :
- You can bind functions to options and let the menu execute them with the  `run` method
- you can just execute the menu screen to get the index of the selected option

examples :

```python
menu.run() # and that's pretty much all you need to do...
index = menu.get_index() # will return the index of the selected option	
print(menu.options[index]) # should display the option you selected
```
