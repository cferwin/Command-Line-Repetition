import urwid
from slide import Slide
from collection import Collection
from menu import Menu

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
    # Enter the main menu
    menu = Menu(collections)
    menu.run()
