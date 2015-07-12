"""
RUNNABLE
"""
import thread
import time


class Runnable(object):
    """
    RUNNABLE
    Provide a simple run, stop and tick looping framework.
    """
    RUNNABLE_DELAY = 0.01

    def __init__(self):
        self.running = False

    def run(self, count=None, delay=None):
        """ Start running loop. """
        self.running = True

        if delay is None:
            delay = self.RUNNABLE_DELAY

        iterations = 0
        max_iterations_reached = False
        while self.running and not max_iterations_reached:
            iterations += 1

            self.tick()

            max_iterations_reached = count and iterations >= count
            if not max_iterations_reached:
                time.sleep(delay)

    def run_async(self, *args, **kwargs):
        """ Start running loop in new thread. """
        return thread.start_new_thread(self.run, args, kwargs)

    def tick(self):
        """ Tick a running loop. """
        pass

    def stop(self):
        """ Stop running loop. """
        self.running = False
