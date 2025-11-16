from copy import deepcopy

############################## 
#     1. 관계행렬 입력 기능 
# ############################

# ----------------------------------------------
# 1-1. 관계행렬 수동 입력 함수
# ----------------------------------------------
# 사용자로부터 ５ × ５ 크기의 정방행렬을 행 단위로 입력
def input_relation_matrix(n=5):
    matrix = []
    print("5x5 관계 행렬을 입력하세요 (0 또는 1):")

    for i in range(n):
        # 입력 데이터는 리스트(2차원 배열)로 저장
        row = list(map(int, input(f"행 {i+1}: ").split()))

        # 입력 예외 처리
        if len(row) != n:
            print("⚠️ 5개의 값을 입력해야 합니다.")
            return input_relation_matrix(n)
        
        matrix.append(row)
    return matrix

# ----------------------------------------------
# (추가기능1) 순서쌍 -> 관계행렬 초기화 함수
# ----------------------------------------------
# 사용자가 (1,2), (2,3) 형태의 순서쌍 관계를 입력하면
# 자동으로 5x5 행렬 형태로 변환하여 초기화
def relation_matrix_from_pairs():
    n = 5
    matrix = [[0] * n for _ in range(n)]
    print("관계의 원소를 순서쌍 형태로 입력하세요 (예: 1 2). 종료하려면 'end' 입력:")

    while True:
        data = input("입력: ").strip()
        if data.lower() == "end":
            break
        try:
            a, b = map(int, data.split())
            if 1 <= a <= n and 1 <= b <= n:
                matrix[a - 1][b - 1] = 1
            else:
                print("⚠️ 1~5 범위의 숫자만 입력 가능합니다.")
        except ValueError:
            print("⚠️ 입력 형식 오류! 예: 1 2")
    return matrix


############################## 
#     2. 동치 관계 판별 기능
# ############################

# ----------------------------------------------
# 2-1. 반사， 대칭， 추이 관계를 각각 판별하는 함수
# ----------------------------------------------

# 1) 반사 관계
def is_reflexive(matrix):
    """모든 대각 원소가 1이면 반사 관계"""
    for i in range(len(matrix)):
        if matrix[i][i] != 1:
            return False
    return True

# 2) 대칭 관계
def is_symmetric(matrix):
    """행렬이 전치행렬과 같으면 대칭 관계"""
    n = len(matrix)
    for i in range(n):
        for j in range(n):
            if matrix[i][j] != matrix[j][i]:
                return False
    return True

# 3) 추이 관계
def is_transitive(matrix):
    """(a,b), (b,c) ∈ R이면 (a,c) ∈ R이 되어야 함"""
    n = len(matrix)
    for i in range(n):
        for j in range(n):
            if matrix[i][j]:
                for k in range(n):
                    if matrix[j][k] and not matrix[i][k]:
                        return False
    return True

# ----------------------------------------------
# 2-2. 관계의 성질 판별 결과에 따라 동치 관계 여부에 대한 메시지를 출력
# ----------------------------------------------
def is_equivalence(matrix):
    # 동치 관계 판별
    r = is_reflexive(matrix)
    s = is_symmetric(matrix)
    t = is_transitive(matrix)
    print(f"\n[관계 판별 결과]")
    print(f"반사 관계: {r}")
    print(f"대칭 관계: {s}")
    print(f"추이 관계: {t}")

    # 
    if r and s and t:
        print("이 관계는 동치 관계입니다.")
        return True
    else:
        print("이 관계는 동치 관계가 아닙니다.")
        return False
    

############################## 
#  3. 동치 관계일 경우 동치류 출력
# ############################

# ----------------------------------------------
# 3-1. 집합의 원소에 대해 동치류를 판별하는 함수를 구현
# ----------------------------------------------
def get_equivalence_classes(matrix, A):
    print("\n[동치류 결과]")
    n = len(A)
    visited = set()

    for i in range(n):
        # 3-2. 집합의 각 원소에 대한 동치류를 각각 출력
        if A[i] not in visited:
            eq_class = []
            for j in range(n):
                # 양방향 검사
                if matrix[i][j] == 1 and matrix[j][i] == 1:
                    eq_class.append(A[j])
            visited.update(eq_class)
            print(f"{A[i]}의 동치류 = {eq_class}")



############################## 
#  4. 폐포 구현 기능 + 와샬 알고리즘
# ############################

# ----------------------------------------------------------------------------
# 4-1. 입력받은 관계가 반사，대칭，추이 관계가 아닐 경우 각각의 폐포로 만드는 함수를 구현
# ----------------------------------------------------------------------------
def reflexive_closure(matrix):
    """반사폐포: 모든 (a,a)를 추가"""
    n = len(matrix)
    for i in range(n):
        matrix[i][i] = 1
    return matrix


def symmetric_closure(matrix):
    """대칭폐포: (a,b)가 있으면 (b,a)도 추가"""
    n = len(matrix)
    for i in range(n):
        for j in range(n):
            if matrix[i][j] == 1:
                matrix[j][i] = 1
    return matrix

def transitive_closure(matrix):
    """기본 추이폐포: (a,b), (b,c) 있으면 (a,c)를 1로 만듦"""
    n = len(matrix)
    result = [row[:] for row in matrix]

    for i in range(n):
        for j in range(n):
            if result[i][j] == 1:
                for k in range(n):
                    if result[j][k] == 1:
                        result[i][k] = 1

    return result

# ----------------------------------------------
# (추가기능2) 추이폐초를 와샬 알고리즘으로
# ----------------------------------------------
def warshall_algorithm(matrix):
    """와샬 알고리즘을 이용한 추이폐포 (Transitive Closure)"""
    n = len(matrix)
    result = [row[:] for row in matrix]
    print("\n[와샬 알고리즘 단계별 진행]")
    for k in range(n):
        print(f"\n중간 정점 {k+1} 고려 후:")
        for i in range(n):
            for j in range(n):
                result[i][j] = result[i][j] or (result[i][k] and result[k][j])
        for row in result:
            print(row)
    return result


# ==============================================

def main():
    A = [1, 2, 3, 4, 5]

    print("==============================================")
    print("1. 순서쌍으로 관계 입력 (예: 1 2)")
    print("2. 5x5 행렬로 직접 입력")
    choice = input("선택 (1 또는 2): ").strip()

    if choice == "1":
        M = relation_matrix_from_pairs() # 순서쌍으로 입력 받고 관계행렬로
    else:
        M = input_relation_matrix() # 관계행렬을 입력 받음

    # 입력된 관계 행렬 출력
    print("\n입력된 관계 행렬:")
    for row in M:
        print(row)

    if is_equivalence(M): # 관계 성질 판별
        get_equivalence_classes(M, A) # 동치류 출력

    else:
        print("\n[폐포 변환 시작]")
        base = deepcopy(M)

        # 4-2. 각각의 관계에 대한 폐포 변환 전， 변환 후를 출력
        # 4-3. 각각의 폐포로 변환한 후 동치  관계를 다시 판별하고 동치류 출력하기
        print("----------------------------------------------")
        print("\n(1) 반사 폐포:")
        print("\n[반사 폐포 변환 전]:")
        for r in base: print(r)

        print("\n[반사 폐포 변환 후]:")
        R1 = reflexive_closure(deepcopy(base))
        for r in R1: print(r)
        
        print("\n[반사 폐포 적용 후 관계 판별]")
        if is_equivalence(R1): get_equivalence_classes(R1, A)
        else:
            print("동치 관계가 아니므로 동치류는 존재하지 않습니다.")

        print("----------------------------------------------")
        print("\n(2) 대칭 폐포:")
        print("\n[대칭 폐포 변환 전]:")
        for r in base: print(r)

        print("\n[대칭 폐포 변환 후]:")
        R2 = symmetric_closure(deepcopy(base))
        for r in R2: print(r)

        print("\n[대칭 폐포 적용 후 관계 판별]")
        if is_equivalence(R2): get_equivalence_classes(R2, A)
        else:
            print("동치 관계가 아니므로 동치류는 존재하지 않습니다.")

        print("----------------------------------------------")
        print("\n(3) 추이 폐포 :")
        print("\n[추이 폐포 변환 전]:")
        for r in base: print(r)

        print("\n[추이 폐포 변환 후]:")
        R3 = transitive_closure(deepcopy(base))
        for r in R3: print(r)

        print("\n[추이 폐포 적용 후 관계 판별]")
        if is_equivalence(R3): get_equivalence_classes(R3, A)
        else:
            print("동치 관계가 아니므로 동치류는 존재하지 않습니다.")

        print("----------------------------------------------")
        print("\n추가기능: 와샬 알고리즘으로 단계 시각화 (y/n)")
        i = input().strip().lower()

        if i == "y": warshall_algorithm(deepcopy(base))

if __name__ == "__main__":
    main()