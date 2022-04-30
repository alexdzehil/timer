import logging
import time

from reader import feed


class TimerError(Exception):
    """A custom exceprion used to report errors in use of Timer class"""


class Timer:
    timers = {}

    def __init__(
            self,
            name=None,
            text='Elapsed time: {:0.4f} seconds',
            logger=print
    ):
        self._start_timer = None
        self.name = name
        self.text = text
        self.logger = logger

        # Add new named timers to dictionary of timers
        if name:
            self.timers.setdefault(name, 0)

    def start(self):
        """Start a new timer"""
        if self._start_timer is not None:
            raise TimerError(f'Timer is running. Use .stop() to stop it')

        self._start_timer = time.perf_counter()

    def stop(self):
        """Stop the timer, and report the elapsed time"""
        if self._start_timer is None:
            raise TimerError(f'Timer is not running. Use .start() to start it')

        elapsed_time = time.perf_counter() - self._start_timer
        self._start_timer = None

        if self.logger:
            self.logger(self.text.format(elapsed_time))
        if self.name:
            self.timers[self.name] += elapsed_time

        return elapsed_time


def main():
    """Print the 10 latest tutorial from Real Python"""
    t = Timer(
        text='Downloaded 10 tutorials in {:0.2f} seconds',
        logger=logging.warning,
        name='accumulate'
    )
    t.start()
    for tutorial_num in range(10):
        tutorial = feed.get_article(tutorial_num)
        print(tutorial)
    t.stop()

    download_time = Timer.timers['accumulate']
    print(f'Timer name - {t.name} - downloaded 10 tutorials in {download_time:0.2f} seconds')


if __name__ == '__main__':
    main()
