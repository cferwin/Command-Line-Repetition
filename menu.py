""" Stores functions for rendering menus with curses.
"""

import curses

# ----------------------------------------
# Menu Logic and Rendering Functions
# ----------------------------------------

# Use this function to enter into the menu system. Handles input and
# navigation through the system. Requires an initialized Curses screen.
def init(screen, exit_key='q'):
    _refresh = None     # Used for determining when to update the _screen.
    global _screen
    _screen = screen

    main()

    while True:
        # Check for the exit key
        char = _screen.getch()
        if char == ord(exit_key):
            break

        # Handle option input
        option = get_option(char)
        if option:
            option[1]()

        # Refresh the screen if necessary
        if _refresh:
            _screen.refresh()
            _refresh = False

# The main menu. Use init() to enter the menu system.
def main():
    set_refresh()

    clear_options()
    add_option('1', study_collection, "1 - Study Collection")
    add_option('2', new_collection, "2 - New Collection")

    print_options(0, 5)

def study_collection():
    set_refresh()

    # Initialize options
    clear_options()
    add_option('1', main, "1 - Go Back")
    add_option('2', main, "2 - Test Collection")

    # Draw the menu
    print_options(0, 5)

def new_collection():
    pass

def new_slide():
    pass

def remove_slide():
    pass

def edit_slide():
    pass

def remove_collection():
    pass

def print_options(y, x):
    i = 0
    for option in _options:
        i += 1
        _screen.move(y+i, x)
        _screen.addstr(option[2])

def set_refresh():
    _screen.clear()
    _screen.border()
    _refresh = True

# **********************************************
# * Internal Functions -- Don't use elsewhere. *
# **********************************************

# The Curses screen being drawn to. This should be set once when the main
# function is entered. Don't change it unless you really mean it.
_screen = None

# ----------------------------------------
# Menu Options
# ----------------------------------------

# Do not set this manually. Use the functions below.
# (selection key, function, description)
_options = []

# Add a menu option
def add_option(key, function, description):
    _options.append( (key, function, description) )

# Remove all menu options
def clear_options():
    _options.clear()

# Returns the option tuple for a given key. Returns None if there is no
# option associated with the key.
def get_option(key):
    for option in _options:
        if key == ord(option[0]):
            return option

    return None
