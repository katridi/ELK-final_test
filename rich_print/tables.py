from typing import Iterable

from rich.console import Console
from rich.table import Table


class ConsoleTable(Table):
    def __init__(self) -> None:
        super().__init__()
        self._set_columns()
        self.console = Console()

    def _set_columns(self) -> None:
        pass

    def populate_row(self, row: Iterable) -> None:
        # to make string
        str_row = [str(x) for x in row]
        self.add_row(*str_row)

    def print(self) -> None:
        self.console.print(self)


class TopMoviesConsoleTable(ConsoleTable):
    def _set_columns(self) -> None:
        self.add_column("#", style="cyan", no_wrap=True)
        self.add_column("Title 📽️", style="white", no_wrap=True)
        self.add_column("Year ⌛", style="cyan", no_wrap=True)
        self.add_column("Avg ⭐", style="red", justify="center", no_wrap=True)
        self.add_column("Genres", style="cyan", no_wrap=True)
        self.add_column("Votes", style="magenta", no_wrap=True)
        self.add_column("ImdbID", style="cyan", no_wrap=True)
