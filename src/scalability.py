import os
import random
import sys
import tempfile

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

    rng = random.Random(0)

    with tempfile.TemporaryDirectory() as tmpdir:
        for n in NS:
            instance = generate_instance(n, rng)
            prefs_path = os.path.join(tmpdir, f"prefs_{n}.txt")
            with open(prefs_path, "w") as f:
                f.write(instance)

                print(f"Generated instance for n={n}")


if __name__ == "__main__":
    main()
