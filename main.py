import json
import time

EPSILON = 1e-9  # 이 값보다 차이가 작으면 동점으로 본다
DATA_FILE = "data.json"
REPEAT = 10     # 성능 측정 반복 횟수


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

def measure_mac_ms(pattern, filter_, repeat=REPEAT):
    """mac을 repeat번 실행해 1회 평균 시간(ms)을 돌려준다."""
    start = time.perf_counter()
    for _ in range(repeat):
        mac(pattern, filter_)
    end = time.perf_counter()
    return (end - start) * 1000 / repeat


def make_cross(n):
    """n x n 십자가 패턴을 만든다. (가운데 줄과 가운데 칸이 1)"""
    mid = n // 2
    matrix = []
    for i in range(n):
        row = []
        for j in range(n):
            if i == mid or j == mid:
                row.append(1.0)
            else:
                row.append(0.0)
        matrix.append(row)
    return matrix


def make_x(n):
    """n x n X 패턴을 만든다. (두 대각선이 1)"""
    matrix = []
    for i in range(n):
        row = []
        for j in range(n):
            if i == j or i + j == n - 1:
                row.append(1.0)
            else:
                row.append(0.0)
        matrix.append(row)
    return matrix


def print_performance(sizes):
    """크기별 MAC 평균 시간과 연산 횟수(N²) 표를 출력한다."""
    print("\n#---------------------------------------")
    print(f"# [3] 성능 분석 (평균/{REPEAT}회)")
    print("#---------------------------------------")
    print("크기        평균 시간(ms)    연산 횟수(N²)")
    print("-" * 42)
    for n in sizes:
        ms = measure_mac_ms(make_cross(n), make_x(n))
        size_text = f"{n}×{n}"
        print(f"{size_text:<10}{ms:>14.4f}{n * n:>14}")

def read_matrix(name, n=3):
    """n줄을 입력받아 n x n 배열로 돌려준다. 형식이 틀린 줄은 다시 입력받는다."""
    print(f"{name} ({n}줄 입력, 공백 구분)")
    matrix = []
    while len(matrix) < n:
        line = input(f"  {len(matrix) + 1}번째 줄: ")
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
    print_performance([3])


def normalize_label(label):
    """여러 표기('+', 'cross', 'x' 등)를 표준 라벨 Cross / X로 바꾼다. 모르는 값이면 None."""
    text = str(label).strip().lower()
    if text in ("+", "cross"):
        return "Cross"
    if text == "x":
        return "X"
    return None


def load_json(path):
    """JSON 파일을 읽어 돌려준다. 실패하면 이유를 출력하고 None."""
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"✗ 파일을 찾을 수 없습니다: {path}")
    except json.JSONDecodeError as e:
        print(f"✗ JSON 형식 오류: {e}")
    return None


def load_filters(data):
    """filters 부분을 읽어 {'size_5': {'Cross': 배열, 'X': 배열}, ...} 형태로 만든다."""
    filters = {}
    for size_key, raw in data.get("filters", {}).items():
        pair = {}
        for name, matrix in raw.items():
            label = normalize_label(name)
            if label is not None:
                pair[label] = matrix
        if "Cross" in pair and "X" in pair:
            filters[size_key] = pair
            print(f"✓ {size_key} 필터 로드 완료 (Cross, X)")
        else:
            print(f"✗ {size_key} 필터 로드 실패: cross / x 중 빠진 것이 있음")
    return filters


def get_size_from_key(key):
    """'size_13_2' 같은 키에서 13을 꺼낸다. 형식이 틀리면 None."""
    parts = key.split("_")
    if len(parts) != 3 or parts[0] != "size":
        return None
    try:
        return int(parts[1])
    except ValueError:
        return None


def is_square(matrix, n):
    """matrix가 정확히 n x n 인지 확인한다."""
    if not isinstance(matrix, list) or len(matrix) != n:
        return False
    for row in matrix:
        if not isinstance(row, list) or len(row) != n:
            return False
    return True


def fail(reason):
    """검증 실패를 출력하고 (False, 이유)를 돌려준다."""
    print(f"FAIL: {reason}")
    return False, reason


def analyze_case(key, case, filters):
    """패턴 1개를 판정한다. (PASS 여부, 실패 이유)를 돌려준다."""
    print(f"--- {key} ---")

    n = get_size_from_key(key)
    if n is None:
        return fail("키 형식 오류 (size_N_번호 형태가 아님)")

    pair = filters.get(f"size_{n}")
    if pair is None:
        return fail(f"size_{n} 필터가 없음")

    expected = normalize_label(case.get("expected", ""))
    if expected is None:
        return fail(f"expected 라벨을 해석할 수 없음: {case.get('expected')}")

    pattern = case.get("input")
    if not is_square(pattern, n):
        return fail(f"패턴 크기 불일치 ({n}x{n}이 아님)")
    if not is_square(pair["Cross"], n) or not is_square(pair["X"], n):
        return fail(f"필터 크기 불일치 ({n}x{n}이 아님)")

    score_cross = mac(pattern, pair["Cross"])
    score_x = mac(pattern, pair["X"])
    result = judge(score_cross, score_x, "Cross", "X")

    print("Cross 점수:", score_cross)
    print("X 점수:", score_x)

    if result == expected:
        print(f"판정: {result} | expected: {expected} | PASS")
        return True, ""
    if result == "UNDECIDED":
        reason = "동점(UNDECIDED) 처리 규칙에 따라 FAIL"
    else:
        reason = f"판정 {result}이(가) expected {expected}와 다름"
    print(f"판정: {result} | expected: {expected} | FAIL ({reason})")
    return False, reason


def run_mode2():
    """모드 2: data.json의 패턴을 모두 판정하고 결과를 요약한다."""
    print("\n#---------------------------------------")
    print("# [1] 필터 로드")
    print("#---------------------------------------")
    data = load_json(DATA_FILE)
    if data is None:
        return
    filters = load_filters(data)

    print("\n#---------------------------------------")
    print("# [2] 패턴 분석 (라벨 정규화 적용)")
    print("#---------------------------------------")
    total = 0
    passed = 0
    failures = []
    for key, case in data.get("patterns", {}).items():
        total += 1
        ok, reason = analyze_case(key, case, filters)
        if ok:
            passed += 1
        else:
            failures.append((key, reason))
            
    print_performance([3, 5, 13, 25])

    print("\n#---------------------------------------")
    print("# [4] 결과 요약")
    print("#---------------------------------------")
    print(f"총 테스트: {total}개")
    print(f"통과: {passed}개")
    print(f"실패: {len(failures)}개")
    if failures:
        print("\n실패 케이스:")
        for key, reason in failures:
            print(f"- {key}: {reason}")

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
            run_mode2()
            break
        else:
            print("1 또는 2를 입력하세요.")


if __name__ == "__main__":
    main()