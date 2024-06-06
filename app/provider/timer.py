
import time


class TimerProvider:
    def __init__(self) -> None:
        self.timer = time
        self.time_start: float = None
        self.time_finish: float = None

    def start(self) -> None:
        self.time_start = self.timer.time()

    def finish(self) -> None:
        self.time_finish = self.timer.time()

    def log(self) -> None:
        print(f'Application finished in {self.time_finish - self.time_start}')