import os
import sys
import urllib.request
import datetime
import time
import json
import pandas as pd

def getRequestUrl(url):
    req = urllib.request.Request(url)  #매개변수로 받은 url에 대한 요청을 보낼 객체를 생성
    try:
        response = urllib.request.urlopen(req)  #요청 객체를 보내서 받은 응답 데이터를 response 객체에 저장

        #response 객체에 저장된 코드를 확인. 코드가 200이면 요청을 정상 처리한 것이므로 성공.
        # 메시지와 현재 시간을 파이썬 셸 창에 출력하고 응답을 utf-8 형식으로 디코딩하여 반환.
        if response.getcode() == 200:
            print("[%s] Url Request Success" % datetime.datetime.now())
            return response.read().decode('utf-8')
    except Exception as e:
        print(e)
        print("[%s] Error for URL : %s" % (datetime.datetime.now(), url))
        return None

# [code2] 입국관광통계서비스의 오픈 API를 사용하여 데이터 요청 url을 만들고 [CODE 1]의 getRequestUrl(url)을 호출해서 받은 응답 데이터를 반환
ServiceKey = "TEo5fURVg6O3ChvfXOmzkr0IXbTl0d4VkfIj3JVTz0ctJ%2BNS0IjPHxLXlijxDlubeXvzd3ZlGksTn%2FHhACp8gA%3D%3D"

def getTourismStatsItem(ServiceKey, area, category):
    service_url = "http://openapi.tour.go.kr/openapi/service/EdrcntTourismStatsService/getEdrcntTourismStatsList"

    parameters = "?_type=json&serviceKey=" + ServiceKey #인증키
    parameters += "&Area=" + area
    parameters += "&Category=" + category

    url = service_url + parameters
    print(url)   #액세스 거부 여부 확인용 출력
    retData = getRequestUrl(url) #[CODE 1]

    if (retData == None):
        return None
    else:
        return json.loads(retData)

def getTourismStatsService(area, category):
    jsonResult = []
    result = []
    jsonData = getTourismStatsItem(ServiceKey, area, category) #[CODE 2]
    if (jsonData['response']['header']['resultMsg'] == 'OK'):
        area = jsonData['response']['body']['items']['item']['AREA'] #지역코드
        sno = jsonData['response']['body']['items']['item']['SNO'] #SNO는 숙박업체 고유번호
        category = jsonData['response']['body']['items']['item']['CATEGORY'] #숙박업체종류
        address1 = jsonData['response']['body']['items']['item']['ADDRESS1'] #숙박업체 주소
        address2 = jsonData['response']['body']['items']['item']['ADDRESS2'] #숙박업체 상세주소
        tel = jsonData['response']['body']['items']['item']['TEL'] #숙박업체 전화번호
        name = jsonData['response']['body']['items']['item']['NAME'] #숙박업체 이름
        jsonResult.append({'name' : name,'area': area, 'address1': address1,'address2': address2, 'category': category, 'sno': sno, 'tel': tel})
        result.append([sno,area,category, name, address1, address2,tel])
    return (jsonResult, result, name)

def main():
    jsonResult = []
    result = []

    print("<< 전라북도 관광지 숙박 위치 정보 >>")
    area = input(
        '지역코드(01-고창군 02-군산시 03-김제시 04-남원시 05-무주군 06-부안군 07-순창군 08-완주군 09-익산시 10-임실군 11-장수군 12-전주시 13-진안군 14-진안군) : ')
    category = int(input('숙박시설분류(01-호텔 02-굿스테이 03-리조트/콘도 04-모텔 05-팬션/민박 06-유스호스텔/수련원 07-한옥) : '))

    jsonResult, result, name = getTourismStatsService(area, category)  # [CODE 3]

    if (name == ''):  # URL 요청은 성공하였지만, 데이터 제공이 안된 경우
        print('데이터가 전달되지 않았습니다. 공공데이터포털의 서비스 상태를 확인하기 바랍니다.')
    else:
        # 파일저장 : csv 파일
        columns = ["고유번호", "지역코드", '숙박종류', "이름", "주소", "상세주소", '전화번호']
        result_df = pd.DataFrame(result, columns=columns)
        result_df.to_csv(f'./{area}_{category}.csv', index=False, encoding='cp949')

if __name__ == "__main__":
    main()