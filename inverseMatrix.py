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


def inverse_by_determinant(matrix):

    n = len(matrix) # 행렬의 크기
    det = determinant(matrix) # 행렬식 계산

    # 행렬식이 0인 경우 역행렬 존재 불가, 예외 처리
    if det == 0:
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



def inverse_by_gauss_jordan(matrix):
    n = len(matrix) # 행렬의 크기

    # 확장 행렬로 변환 [A | I]
    # 원본 행렬 오른쪽에 단위행렬을 붙임
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

    # 피봇을 1로, 다른 행은 0으로 변환(기약행사다리꼴)
    for i in range(n):

        pivot = m[i][i]

        if pivot == 0:
            raise ValueError("pivot=0, 역행렬이 존재하지 않음")
        
        # 피봇을 1로 변환
        for j in range(2*n):
            m[i][j] /= pivot

        # 피봇과 같은 열의 다른 원소를 0으로 변환
        for k in range(n):

            if k != i: # 자신의 행 제외
                factor = m[k][i]
                for j in range(2*n):
                    m[k][j] -= factor * m[i][j]

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

    return inverse_matrix


###### 행렬 입력 

# 정방행렬의 크기 입력
n = int(input("정방행렬의 크기 n을 입력하세요: "))


# 행렬 원소 입력
m = []
for _ in range(n):
    print("행렬의 각 행을 입력하세요:")
    m.append(list(map(float, input().split())))
# m = [list(map(float, input().split())) for _ in range(n)]


# 행렬식 출력
print("\n[1] 행렬식 (Determinant):")
print(determinant(m))


# 행렬식 기반 역행렬 계산
print("\n[2] 행렬식 이용 역행렬:")
try: # 예외를 잡기 위해 try 구문 사용

    matrix = inverse_by_determinant(m)
    for row in matrix:  print(row)

except ValueError as e:
    print(e)


# 가우스-조던 소거법 기반 역행렬 계산
print("\n[3] 가우스-조던 소거법 이용 역행렬:")
try:

    matrix = inverse_by_gauss_jordan(m)
    for row in matrix:  print(row)

except ValueError as e:
    print(e)