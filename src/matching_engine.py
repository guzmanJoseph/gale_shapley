import sys

def main():
    print("RUNNING")
    lines = open(sys.argv[1]).readlines()
    n = int(lines[0])

    # Preferences (1-based indexing)
    hospital_preferences = [[] for i in range(n + 1)]
    student_preferences = [[] for i in range(n + 1)]

    for i in range(1, n + 1):
        hospital_preferences[i] = list(map(int, lines[i].split()))

    for i in range(1, n + 1):
        student_preferences[i] = list(map(int, lines[n + i].split()))

    # rank[s][h] = how much student s prefers hospital h (lower is better)
    rank = [[0] * (n + 1) for i in range(n + 1)]
    for s in range(1, n + 1):
        for r, h in enumerate(student_preferences[s]):
            rank[s][h] = r

    hospital_match = [0] * (n + 1)   # hospital -> student
    student_match = [0] * (n + 1)    # student -> hospital
    next_proposal = [0] * (n + 1)    # next student each hospital proposes to

    free_hospitals = list(range(1, n + 1))

    while free_hospitals:
        h = free_hospitals.pop(0)
        s = hospital_preferences[h][next_proposal[h]]
        next_proposal[h] += 1

        if student_match[s] == 0:
            student_match[s] = h
            hospital_match[h] = s
        else:
            current_hospital = student_match[s]
            if rank[s][h] < rank[s][current_hospital]:
                student_match[s] = h
                hospital_match[h] = s
                hospital_match[current_hospital] = 0
                free_hospitals.append(current_hospital)
            else:
                free_hospitals.append(h)

    # Output result
    for h in range(1, n + 1):
        print(h, hospital_match[h])

if __name__ == "__main__":
    main()
