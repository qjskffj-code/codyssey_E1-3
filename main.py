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


# ---- 테스트 ----
print(judge(5.0, 1.0, "Cross", "X"))            # Cross가 큼
print(judge(1.0, 5.0, "Cross", "X"))            # X가 큼

score_cross = 0.9
score_x = 0.1 + 0.1 + 0.1 + 0.1 + 0.1 + 0.1 + 0.1 + 0.1 + 0.1
print("X 점수:", score_x)
print("그냥 비교:", score_cross > score_x)       # 엡실론 없이 비교하면?
print(judge(score_cross, score_x, "Cross", "X"))  # 엡실론으로 비교하면?