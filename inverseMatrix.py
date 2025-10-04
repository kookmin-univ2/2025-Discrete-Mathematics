# Inverse Matrix

# 행렬식 계산
def determinant(matrix):
    # 행렬의 크기가 1인 경우 행렬식은 첫 번째 원소
    if len(matrix) == 1:
        return matrix[0][0]
    
    # 행렬의 크기가 2인 경우 행렬식 (ad - bc) (예시 행렬: [[a, b], [c, d]])
    if len(matrix) == 2:
        return matrix[0][0]*matrix[1][1] - matrix[0][1]*matrix[1][0]
    
    # 행렬의 크기가 3 이상인 경우
    det = 0
    for c in range(len(matrix)): # cofactor

        # minor: c열 제거한 부분행렬
        minor = [row[:c] + row[c+1:] for row in matrix[1:]]
        """ 반복문으로 작성
        minor = []
        for row in matrix[1:]:         # 첫 행 제외
            new_row = []
            for i in range(len(row)):  # 현재 행의 각 열 순회
                if i != c:             # c번째 열 제외
                    new_row.append(row[i])
            minor.append(new_row)
        """

        # (-1)^(i+j) 부호 반영
        det += ((-1)**c) * matrix[0][c] * determinant(minor)

    return det

# 행렬식 이용 역행렬 계산
def inverse_by_determinant(matrix):
    n = len(matrix) # 행렬의 크기
    det = determinant(matrix) # 행렬식 계산

    if det == 0: # 행렬식이 0인 경우 역행렬 존재 불가, 예외 처리
        raise ValueError("det=0, 역행렬이 존재하지 않음")

    # 여인수 행렬
    cofactors = [] 
    for r in range(n):
        row = []
        for c in range(n):
            # (r,c) 원소에 대한 소행렬
            minor = [m[:c] + m[c+1:] for m in (matrix[:r] + matrix[r+1:])]
            """
            minor = []
            temp_matrix = matrix[:r] + matrix[r+1:]  # r행 제외
            for m in temp_matrix:
                new_row = []
                for i in range(len(m)):
                    if i != c:
                        new_row.append(m[i])
                minor.append(new_row)
            """

            # 여인수 계산
            row.append(((-1)**(r+c)) * determinant(minor)) 
        cofactors.append(row)

    # 수반행렬 = cofactors의 전치행렬
    adjugate = [list(row) for row in zip(*cofactors)]
    """
    adjugate = []
    for i in range(n):
        new_row = []
        for j in range(n):
            new_row.append(cofactors[j][i])
        adjugate.append(new_row)
    """

    # 역행렬 계산 adj(A) / det(A)
    inverse_matrix = [[adjugate[i][j] / det for j in range(n)] for i in range(n)]
    """
    inverse_matrix = []
    for i in range(n):
        new_row = []
        for j in range(n):
            new_row.append(adjugate[i][j] / det)
        inverse_matrix.append(new_row)
    """

    return inverse_matrix

# 가우스 조단 역행렬 계산
def inverse_by_gauss_jordan(matrix):
    n = len(matrix) # 행렬의 크기

    # 확장 행렬로 변환 [A | I] # 원본 행렬 오른쪽에 단위행렬을 붙임
    m = [row + [float(i == j) for j in range(n)] for i, row in enumerate(matrix)]
    """
    m = []
    for i, row in enumerate(matrix):
        new_row = row[:]  # 원본 복사
        for j in range(n):
            if i == j:
                new_row.append(1.0)
            else:
                new_row.append(0.0)
        m.append(new_row)
    """

    row_ops = 0  # 기본행연산 횟수 카운터

    # 피봇을 1로, 다른 행은 0으로 변환(기약행사다리꼴)
    for i in range(n):
        pivot = m[i][i]

        # pivot이 0이면 아래 행 탐색 (부분 피봇팅)
        if pivot == 0:
            swapped = False
            for k in range(i + 1, n):
                if m[k][i] != 0:  # 교환 가능한 행
                    m[i], m[k] = m[k], m[i]
                    row_ops += 1  # 행 교환 연산 1회
                    print(f"pivot이 0이므로 행{i}과 행{k} 교환")
                    swapped = True
                    pivot = m[i][i]  # 새로운 pivot 갱신
                    break
            if not swapped:
                # 아래 행 모두 0이면 → det=0 → 역행렬 존재 X
                raise ValueError(f"모든 pivot 후보가 0 → det=0, 역행렬이 존재하지 않음 (열 {i})")

        
        # 피봇을 1로 변환
        for j in range(2*n):
            m[i][j] /= pivot
        row_ops += 1  # 한 행의 스칼라배 연산 -> 기본행연산 1회

        # 피봇과 같은 열의 다른 원소를 0으로 변환
        for k in range(n):
            if k != i: # 자신의 행 제외
                factor = m[k][i]

                if factor != 0:  # 불필요한 연산 제외
                    for j in range(2*n):
                        m[k][j] -= factor * m[i][j]
                    row_ops += 1  # 한 행에 다른 행의 배수를 더함

    # 역행렬 계산(오른쪽 행렬)
    inverse_matrix = [row[n:] for row in m]
    """
    inverse_matrix = []
    for row in mat:
        new_row = []
        for j in range(n, 2*n):
            new_row.append(row[j])
        inverse_matrix.append(new_row)
    """

    print(f"총 기본행연산 횟수: {row_ops}회")
    return inverse_matrix

# 두 행렬이 동일한지 결과 비교
def compare_matrices(A, B, tol=1e-6):
    # tol: 부동소수점 오차 허용 범위
    n = len(A)
    for i in range(n):
        for j in range(n):
            if abs(A[i][j] - B[i][j]) > tol:
                return False
    return True

###### 프로그램

test_count = 0  # 현재 테스트 횟수
matrix_list = []  # 테스트한 행렬 저장 리스트

while True:
    print("\n==============================")
    print(f"[테스트 #{test_count + 1}] 새로운 행렬 입력")
    print("==============================")

    n = int(input("정방행렬의 크기 n을 입력하세요 (0 입력 시 종료): "))
    if n == 0:
        print("\n프로그램을 종료합니다.")
        print(f"총 {test_count}개의 테스트를 진행했습니다.")
        break

    # 행렬 원소 입력
    m = []
    for _ in range(n):
        print("행렬의 각 행을 입력하세요:")
        m.append(list(map(float, input().split())))
    # m = [list(map(float, input().split())) for _ in range(n)]

    # 입력한 행렬 저장
    matrix_list.append(m)
    test_count += 1

    # 행렬식 출력
    print("\n[1] 행렬식 (Determinant):")
    print(determinant(m))


    # 행렬식 기반 역행렬 계산
    print("\n[2] 행렬식 이용 역행렬:")
    A = None
    try: # 예외를 잡기 위해 try 구문 사용

        A = inverse_by_determinant(m)
        for row in A:  print(row)

    except ValueError as e:
        print(e)


    # 가우스-조던 소거법 기반 역행렬 계산
    print("\n[3] 가우스-조던 소거법 이용 역행렬:")
    B = None
    try:

        B = inverse_by_gauss_jordan(m)
        for row in B:  print(row)

    except ValueError as e:
        print(e)

    # A, B의 결과 비교
    print("\n[4] 결과 비교:")
    if A is not None and B is not None:
        if (compare_matrices(A,B)):
            print("\n역행렬 계산 결과가 같습니다.")
        else:
            print("\n역행렬 계산 결과가 다릅니다.")
    else:
        print("\n비교할 역행렬이 존재하지 않습니다.")

    
    # 다음 테스트 진행 여부
    next_test = input("\n다른 행렬을 테스트하시겠습니까? (y/n): ").lower()
    if next_test != 'y':
        print("\n프로그램을 종료합니다.")
        print(f"총 {test_count}개의 테스트를 진행했습니다.")
        break