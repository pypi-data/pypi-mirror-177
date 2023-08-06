import random
import time

from colorama import Fore

from progress_table import ProgressTable

progress = ProgressTable(columns=["step", "x", "x squared"], default_column_width=2)
progress.add_column("x root", color=Fore.RED)

for step in range(20):
    progress["step"] = step

    for _ in progress(range(10)):
        time.sleep(0.1)  # artificial work

    x = random.randint(0, 100)
    progress["x"] = x
    progress["x squared"] = x**2
    progress["x root"] = x**0.5
    progress.next_row()

progress.close()
