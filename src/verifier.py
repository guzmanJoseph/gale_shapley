import sys

def main():
    prefs_file = sys.argv[1]
    matching_file = sys.argv[2]

    # Reads preferences
    lines = open(prefs_file).readlines()
    n = int(lines[0])

    hospital_preferences = [[] for i in range(n + 1)]
    student_preferences = [[] for i in range(n + 1)]

    for hospital in range(1, n + 1):
        hospital_preferences[hospital] = list(map(int, lines[hospital].split()))

    for student in range(1, n + 1):
        student_preferences[student] = list(map(int, lines[n + student].split()))

    # Reads matching
    match_lines = open(matching_file).readlines()
    if len(match_lines) != n:
        print(f"INVALID: expected {n} lines")
        return

    hospital_match = [0] * (n + 1)
    student_match = [0] * (n + 1)
    used_hospital = [False] * (n + 1)
    used_student = [False] * (n + 1)

    # Check basic validity
    for line in match_lines:
        parts = line.split()
        hospital = int(parts[0])
        student = int(parts[1])

        if hospital < 1 or hospital > n or student < 1 or student > n:
            print("INVALID: id out of range")
            return

        if used_hospital[hospital]:
            print(f"INVALID: hospital {hospital} repeated")
            return
        
        if used_student[student]:
            print(f"INVALID: student {student} repeated")
            return

        used_hospital[hospital] = True
        used_student[student] = True
        hospital_match[hospital] = student
        student_match[student] = hospital

    # Make sure everyone is matched
    for hospital in range(1, n + 1):
        if hospital_match[hospital] == 0:
            print(f"INVALID: hospital {hospital} unmatched")
            return

    for student in range(1, n + 1):
        if student_match[student] == 0:
            print(f"INVALID: student {student} unmatched")
            return

    # Build ranking tables
    rank_hospital = [[0] * (n + 1) for i in range(n + 1)]
    rank_student = [[0] * (n + 1) for i in range(n + 1)]

    for hospital in range(1, n + 1):
        for rank, student in enumerate(hospital_preferences[hospital]):
            rank_hospital[hospital][student] = rank

    for student in range(1, n + 1):
        for rank, hospital in enumerate(student_preferences[student]):
            rank_student[student][hospital] = rank

    # Check for blocking pairs
    for hospital in range(1, n + 1):
        current_student = hospital_match[hospital]
        current_rank = rank_hospital[hospital][current_student]

        for student in range(1, n + 1):
            if rank_hospital[hospital][student] < current_rank:
                current_hospital = student_match[student]
                if rank_student[student][hospital] < rank_student[student][current_hospital]:
                    print(f"UNSTABLE: blocking pair ({hospital}, {student})")
                    return

    print("VALID STABLE")

if __name__ == "__main__":
    main()