import random
import time

from colorama import Fore

from progress_table import ProgressTable

progress = ProgressTable(["step"], print_row_on_setitem=False)
progress.add_column("x", color=Fore.RED)
progress.add_column("x mean", color=Fore.RED, aggregate="mean")
progress.add_column("x sum", color=Fore.RED, aggregate="sum")
progress.add_column("x root", color=Fore.RED)

for step in range(20):
    progress["step"] = step

    for _ in progress(range(10), prefix="TRAIN, "):
        x = random.randint(0, 200)

        progress["x"] = x
        progress["x mean"] = x
        progress["x sum"] = x

        time.sleep(0.1)  # artificial work
    for _ in progress(range(10), prefix="VALID, "):
        x = random.randint(0, 200)

        progress["x"] = x
        progress["x mean"] = x
        progress["x sum"] = x

        time.sleep(0.1)  # artificial work
    time.sleep(1)

    progress.next_row()

progress.close()
