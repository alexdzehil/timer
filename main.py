import time
import logging
from dataclasses import dataclass, field
from typing import Callable, ClassVar, Dict, Optional
from reader import feed


class TimerError(Exception):
    'A custom exception used to report errors in use of timer class'


@dataclass
class NewTimer:
    timers: ClassVar[Dict[str, float]] = {}
    name: Optional[str] = None
    text: str = 'Elapsed time: {:0.4f} seconds'
    logger: Optional[Callable[[str], None]] = print
    _start_time: Optional[float] = field(default=None, init=False, repr=False)

    def __post_init__(self) -> None:
        """Initialization: add timer to dict of timers"""
        if self.name is not None:
            self.timers.setdefault(self.name, 0)

    
    def start(self) -> None:
        """Start a new timer"""
        if self._start_time is not None:
            raise TimerError(f'Timer is running. Use .stop() to stop it')

        self._start_time = time.perf_counter()

    def stop(self) -> float:
        """Stop the timer, and report the elapsed time"""
        if self._start_time is None:
            raise TimerError(f'Timer is not running. Use .start() to start')

        # Calculate elapsed time
        elapsed_time = time.perf_counter() - self._start_time
        self._start_time = None

        # Report elapsed time
        if self.logger:
            self.logger(self.text.format(elapsed_time))
        if self.name:
            self.timers[self.name] += elapsed_time

        return elapsed_time

class Timer:
    timers = {}
    
    def __init__(
                 self,
                 name=None,
                 text='Elapsed time: {:0.4f} seconds',
                 logger=print
    ):
        self._start_time = None
        self.name = name
        self.text = text
        self.logger = logger

        
        # Add new named timers to dictionary of timers
        if name:
            self.timers.setdefault(name, 0)

    def start(self):
        """Start a new timer"""
        if self._start_time is not None:
            raise TimerError(f'Timer is running. Use .stop() to stop it')

        self._start_time = time.perf_counter()

    def stop(self):
        """Stop the timer, and report the elapsed time"""
        if self._start_time is None:
            raise TimerError(f'Timer is not running. Use .start() to start')

        elapsed_time = time.perf_counter() - self._start_time
        self._start_time = None

        if self.logger:
            self.logger(self.text.format(elapsed_time))
        if self.name:
            self.timers[self.name] += elapsed_time

        return elapsed_time

def main():
    """Download and print the latest tutorial from Real Python"""
    #tic = time.perf_counter()
    tutorial = feed.get_article(0)
    #toc = time.perf_counter()
    #print(f'Downloaded the tutorial in {toc - tic:0.4f} seconds')
    #print(tutorial)


timer = NewTimer()

print(timer)

if __name__ == '__main__':
    for tutorial_num in range(10):
        timer.start()
        main()
        timer.stop()

