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


def print_matrix(matrix):
    """배열을 한 줄씩 보기 좋게 출력한다."""
    for row in matrix:
        print("  ", row)


def run_mode1():
    """모드 1: 3x3 필터 2개와 패턴을 직접 입력받아 판정한다."""
    print("\n#---------------------------------------")
    print("# [1] 필터 입력")
    print("#---------------------------------------")
    filter_a = read_matrix("필터 A")
    filter_b = read_matrix("필터 B")

    print("\n✓ 필터 저장 완료")
    print("필터 A:")
    print_matrix(filter_a)
    print("필터 B:")
    print_matrix(filter_b)

    print("\n#---------------------------------------")
    print("# [2] 패턴 입력")
    print("#---------------------------------------")
    pattern = read_matrix("패턴")

    score_a = mac(pattern, filter_a)
    score_b = mac(pattern, filter_b)
    result = judge(score_a, score_b, "A", "B")

    print("\n#---------------------------------------")
    print("# [3] MAC 결과")
    print("#---------------------------------------")
    print("A 점수:", score_a)
    print("B 점수:", score_b)
    if result == "UNDECIDED":
        print(f"판정: 판정 불가 (|A-B| < {EPSILON})")
    else:
        print("판정:", result)


def main():
    """프로그램 시작점: 모드를 선택한다."""
    print("=== Mini NPU Simulator ===")
    while True:
        print("\n[모드 선택]")
        print("1. 사용자 입력 (3x3)")
        print("2. data.json 분석")
        choice = input("선택: ").strip()

        if choice == "1":
            run_mode1()
            break
        elif choice == "2":
            print("data.json 분석은 준비 중입니다.")
            break
        else:
            print("1 또는 2를 입력하세요.")


if __name__ == "__main__":
    main()