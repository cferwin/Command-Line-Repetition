class Slide:
    """ Stores data to be studied. """

    def __init__(self, prompt, answer):
        self.prompt = prompt
        self.answer = answer

    def __str__(self):
        return self.prompt
