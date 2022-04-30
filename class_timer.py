import time

from reader import feed


class TimerError(Exception):
    """A custom exceprion used to report errors in use of Timer class"""


class Timer:
    def __init__(self):
        self._start_timer = None

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
        print(f'Elapsed time: {elapsed_time:0.4f} seconds\n')


def main():
    """Print the latest tutorial from Real Python"""
    t = Timer()
    t.start()
    tutorial = feed.get_article(0)
    t.stop()

    print(tutorial)


if __name__ == '__main__':
    main()
