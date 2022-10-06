import pandas as pd

df = pd.read_csv("bank(1).csv")

#데이터의 행, 열 크기 확인
print(df.shape)

# 전체 구조출력
print(df.info())

#요약 통계 확인
print(df.describe())


print(df.head())

print(df['job'].unique()) #종류들을 나열해줌

print(df.job)
print(df[['job', 'age']]) #열값을 주르륵 보여줌

print(df.loc[:,['job']]) #job 열에 있는 모든 행[:}을 보여주는 코드
print(df.iloc[:,1]) #위, 아래 둘다 동일하다

print(df[0:3]) #행이 0부터 2까지 선택된다.
print(df.iloc[0:3,:]) #위랑 동일한 값이 출력된다.
print(df.iloc[2]) #2번째 있는 사람의 정보를 딕셔너리(?)식으로 나타내기

