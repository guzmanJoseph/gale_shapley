import os
import random
import subprocess
import sys
import tempfile
import time

import matplotlib.pyplot as plt

# Generate numbers to test
NS = [2**x for x in range(0, 10)]


# Generate random input based on size
def generate_instance(n, rng):
    lines = [str(n)]
    base = list(range(1, n + 1))

    # Hospital preference list
    for _ in range(n):
        arr = base[:]
        rng.shuffle(arr)
        lines.append(" ".join(map(str, arr)))

    # Student preference list
    for _ in range(n):
        arr = base[:]
        rng.shuffle(arr)
        lines.append(" ".join(map(str, arr)))

    return "\n".join(lines) + "\n"


def main():

    if len(sys.argv) < 3:
        print("Error: invalid input")
        sys.exit(1)

    matching_engine = sys.argv[1]
    verifier = sys.argv[2]

    rng = random.Random(0)

    match_times = []
    verify_times = []

    with tempfile.TemporaryDirectory() as tmpdir:
        for n in NS:
            instance = generate_instance(n, rng)
            prefs_path = os.path.join(tmpdir, f"prefs_{n}.txt")
            match_path = os.path.join(tmpdir, f"match_{n}.txt")

            with open(prefs_path, "w") as f:
                f.write(instance)

            # Time matching engine
            t0 = time.perf_counter()
            proc = subprocess.run(
                [sys.executable, matching_engine, prefs_path],
                stdout=subprocess.PIPE,
                text=True,
            )
            t1 = time.perf_counter()

            with open(match_path, "w") as f:
                f.write(proc.stdout)

            match_time = t1 - t0

            # Time verifier
            t0 = time.perf_counter()
            subprocess.run(
                [sys.executable, verifier, prefs_path, match_path],
                stdout=subprocess.PIPE,
                text=True,
            )
            t1 = time.perf_counter()

            verify_time = t1 - t0

            match_times.append(match_time)
            verify_times.append(verify_time)

            print(f"n={n} match={match_time:.6f}s verify={verify_time:.6f}s")

    # Plot
    plt.figure()
    plt.plot(NS, match_times, marker="o")
    plt.xlabel("n")
    plt.ylabel("Time (seconds)")
    plt.title("Matching Engine Runtime")
    plt.grid(True)
    plt.savefig("data/matching_runtime.png")

    plt.figure()
    plt.plot(NS, verify_times, marker="o")
    plt.xlabel("n")
    plt.ylabel("Time (seconds)")
    plt.title("Verifier Runtime")
    plt.grid(True)
    plt.savefig("data/verifier_runtime.png")


if __name__ == "__main__":
    main()
