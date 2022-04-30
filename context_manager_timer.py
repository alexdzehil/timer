import logging
import time
from dataclasses import dataclass, field
from typing import ClassVar, Dict, Optional, Callable

from reader import feed


class TimerError(Exception):
    """A custom exceprion used to report errors in use of Timer class"""


@dataclass
class Timer:
    timers: ClassVar[Dict[str, float]] = {}
    name: Optional[str] = None
    text: str = 'Elapsed time: {:0.4f} seconds'
    logger: Optional[Callable[[str], None]] = print
    _start_timer: Optional[float] = field(default=None, init=False, repr=False)

    def __post_init__(self) -> None:
        """Add timer to dict of timers after initialization"""
        if self.name:
            self.timers.setdefault(self.name, 0)

    def __enter__(self):
        """Start a new timer as a context manager"""
        self.start()
        return self

    def __exit__(self, *exc_info):
        """Stop the context manager timer"""
        self.stop()

    def start(self) -> None:
        """Start a new timer"""
        if self._start_timer is not None:
            raise TimerError(f'Timer is running. Use .stop() to stop it')

        self._start_timer = time.perf_counter()

    def stop(self) -> float:
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
    with Timer():
        tutorial = feed.get_article(0)

    print(tutorial)


if __name__ == '__main__':
    main()
