import random

class Collection:
    """ A collection of information to be practiced. """

    def __init__(self, name):
        self.name = name
        self.slides = []

    def __str__(self):
        return self.name

    def add_slide(self, slide):
        """ Add a slide to the collection. """
        self.slides.append(slide)

    def remove_slide(self, slide):
        """ Remove a slide from the collection. """
        self.slides.remove(slide)

    def get_random_slides(self, n, rand=random):
        """ Return a list of randomly selected slides.

            Variables:
            n       int     Number of slides to return
            rand    object  Source of randomness. Defaults to "random".
        """

        return rand.sample(self.slides, n)
