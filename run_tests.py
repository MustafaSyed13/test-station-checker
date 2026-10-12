
import os
import sys
import time
import shutil
import subprocess
import datetime
import psutil

# Testing limits
ROUNDS = 5
MAX_RAM = 90
MAX_CPU = 90
MIN_STORAGE = 10

# Choose the C++ executable
MEMTEST = "./memtest"

if os.name == "nt":
    MEMTEST = "memtest.exe"

# Let the user choose the number of rounds
if len(sys.argv) > 1:
    ROUNDS = int(sys.argv[1])

disk = shutil.disk_usage("/")
free = disk.free / disk.total * 100

print("Free storage:", round(free), "%")

if free < MIN_STORAGE:
    print("STATION NOT READY")
    sys.exit(1)

# Run tests
failed = 0

with open("results.log", "a") as log:

    for i in range(1, ROUNDS + 1):

        # Run C++ memory test
        start = time.time()

        mem = subprocess.run(
            [MEMTEST, "100000"],
            capture_output=True,
            text=True
        )

        seconds = time.time() - start

        # Check RAM and CPU
        ram = psutil.virtual_memory().percent
        cpu = psutil.cpu_percent(interval=1)

        # Check for problems
        problems = []

        if mem.returncode != 0:
            problems.append("Memory test failed")

        if ram > MAX_RAM:
            problems.append("RAM too high")

        if cpu > MAX_CPU:
            problems.append("CPU too high")

        # Decide PASS or FAIL
        if len(problems) == 0:#check if empty 
            status = "PASS"
        else:
            status = "FAIL"
            failed += 1

        # Save test results
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        line = f"{now} Round {i}: {status} | RAM={ram}% CPU={cpu}% Time={seconds:.3f}s | {' '.join(problems)}"

        print(line)
        log.write(line + "\n")

# Final result
print(f"{failed} out of {ROUNDS} rounds failed")

if failed > 0:
    print("STATION FAILED")
    sys.exit(1)
else:
    print("STATION PASSED")
    sys.exit(0)
