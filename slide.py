import time

class Slide:
    """ Stores data to be studied. """

    def __init__(self, prompt, answer):
        self.prompt = prompt
        self.answer = answer

        # Times in seconds for spaced repetition algorithm
        self.previous_wait_time = 5
        self.current_wait_time = 5
        self._next_time = time.time()

    def __str__(self):
        return self.prompt

    def set_new_wait_time(self, new_time):
        """ Set the time until the slide is due to be studied. Time measured in
            seconds.
        """
        self.previous_wait_time = self.current_wait_time
        self.current_wait_time = new_time
        self._next_time = time.time() + self.current_wait_time

    def get_elapsed_wait_time(self):
        """ Get the amount of time in seconds since the last time the slide was
        reviewed.
        """
        return self._next_time - time.time()
