EPSILON = 1e-9  # 이 값보다 차이가 작으면 동점으로 본다


def mac(pattern, filter_):
    """패턴과 필터를 같은 위치끼리 곱해서 모두 더한 점수를 돌려준다."""
    n = len(pattern)
    total = 0.0
    for i in range(n):
        for j in range(n):
            total += pattern[i][j] * filter_[i][j]
    return total


def judge(score_a, score_b, label_a, label_b):
    """두 점수를 비교해 이긴 쪽 라벨을 돌려준다. 거의 같으면 UNDECIDED."""
    if abs(score_a - score_b) < EPSILON:
        return "UNDECIDED"
    if score_a > score_b:
        return label_a
    return label_b

def read_matrix(name, n=3):
    """n줄을 입력받아 n x n 배열로 돌려준다. 형식이 틀린 줄은 다시 입력받는다."""
    print(f"{name} ({n}줄 입력, 공백 구분)")
    matrix = []
    while len(matrix) < n:
        line = input()
        parts = line.split()

        if len(parts) != n:
            print(f"입력 형식 오류: 각 줄에 {n}개의 숫자를 공백으로 구분해 입력하세요.")
            continue

        try:
            row = []
            for p in parts:
                row.append(float(p))
        except ValueError:
            print("입력 형식 오류: 숫자만 입력하세요. (예: 0 1 0)")
            continue

        matrix.append(row)
    return matrix


# ---- 테스트 ----
filter_a = read_matrix("필터 A")
print("저장된 필터 A:", filter_a)