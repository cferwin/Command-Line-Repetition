import curses
from slide import Slide
from collection import Collection
import menu

# ----------------------------------------
# TEST DATA
# TODO: Move into data files later.
# ----------------------------------------

# Test collections
collections = [ Collection("Vocabulary")
         , Collection("Jokes")
         ]

# Test slides
slides = [ Slide("What is this?", "A slide")
         , Slide("Knock knock", "Who's there?")
         ]

# Load test collections with slides
for collection in collections:
    collection.slides = slides

# ----------------------------------------

if __name__ == "__main__":
    # Set up a Curses screen
    screen = curses.initscr()

    curses.noecho()
    curses.halfdelay(1)
    screen.keypad(True)
    curses.cbreak()

    # Enter the main menu
    menu.main(screen)

    # Clean up
    curses.nocbreak()
    screen.keypad(False)
    curses.echo()

    curses.endwin()
