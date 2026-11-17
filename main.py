def mac(pattern, filter_):
    """패턴과 필터를 같은 위치끼리 곱해서 모두 더한 점수를 돌려준다."""
    n = len(pattern)
    total = 0.0
    for i in range(n):
        for j in range(n):
            total += pattern[i][j] * filter_[i][j]
    return total


# ---- 테스트 ----
cross = [[0, 1, 0],
         [1, 1, 1],
         [0, 1, 0]]
x = [[1, 0, 1],
     [0, 1, 0],
     [1, 0, 1]]

print("십자가 x 십자가 필터:", mac(cross, cross))
print("십자가 x X 필터:", mac(cross, x))