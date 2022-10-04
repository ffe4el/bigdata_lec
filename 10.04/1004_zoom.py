import re

s = "12345abbbbbbc123abc456"

#match는 처음부터 있는 문자열을 찾음
#search는 가운데에 있는 문자열도 찾아줌, 근데 한개만 찾아줌(맨 첫번째에 있는거...)
#findall 여러개의 문자열을 찾아줌, 그래서 findall로 찾으면 리스트 형태로 나옴. 패턴과 일치하는 여러문자열을 찾고 싶을때...
m= re.findall('abc', s) #

if m:
    print("match", m)
else :
    print("no match")



