""" Stores functions for rendering menus with curses. Most functions require a
    curses screen as an argument.
"""

import curses

# Global variable to control screen updates
_refresh = False

def main(screen, exit_key='q'):
    # Menu options
    # (selection key, function, description)
    options = [('1', study_collection, "1 - Study Collection")
              ,('2', new_collection, "2 - New Collection")
              ]

    # Draw the menu
    screen.border()
    screen.move(5, 5)
    i = 0
    for option in options:
        i += 1
        screen.move(i, 5)
        screen.addstr(option[2])
    _refresh = True

    while True:
        # Check for the exit key
        char = screen.getch()
        if char == ord(exit_key):
            break

        for option in options:
            if char == ord(option[0]):
                option[1](screen)

        if _refresh:
            screen.refresh()
            _refresh = False

def study_collection(screen):
    pass

def new_collection(screen):
    pass

def new_slide(screen):
    pass

def remove_slide(screen):
    pass

def edit_slide(screen):
    pass

def remove_collection(screen):
    pass
