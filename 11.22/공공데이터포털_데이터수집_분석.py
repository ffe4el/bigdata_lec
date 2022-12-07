import os
import sys
import urllib.request
import datetime
import time
import json
import pandas as pd
import xmltodict

# [code1] url 접속을 요청하고 응답을 받아서 반환
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

def getTourismStatsItem(yyyymm, national_code, ed_cd):
    service_url = "http://openapi.tour.go.kr/openapi/service/EdrcntTourismStatsService/getEdrcntTourismStatsList"

    parameters = "?_type=json&serviceKey=" + ServiceKey #인증키
    parameters += "&YM=" + yyyymm
    parameters += "&NAT_CD=" + national_code
    parameters += "&ED_CD=" + ed_cd

    url = service_url + parameters
    print(url)   #액세스 거부 여부 확인용 출력
    retData = getRequestUrl(url) #[CODE 1]


    if (retData == None):
        return None
    else:
        return json.loads(retData)

# [code3] 수집 기간 동안 월 단위로 [CODE 2]의 getTourismStatsItem()을 호출해 받은 데이터를 리스트로 묶어 반환

def getTourismStatsService(nat_cd, ed_cd, nStartYear, nEndYear):
    jsonResult = []
    result = []
    for year in range(nStartYear, nEndYear+1):
        for month in range(1, 13):
            yyyymm = "{0}{1:0>2}".format(str(year), str(month))
            jsonData = getTourismStatsItem(yyyymm, nat_cd, ed_cd) #[CODE 2]
            if (jsonData['response']['header']['resultMsg'] == 'OK'):
            #데이터가 없는 마지막 항목인 경우 ----------------------------
                if jsonData['response']['body']['items'] == '':
                    dataEND = "{0}{1:0>2}".format(str(year), str(month-1))
                    print("데이터 없음.... \n제공되는 통계 데이터는 %s년 %s월까지입니다." %(str(year), str(month-1)))
                    break
                    #jsonData를 출력하여 확인...........................................
            print(json.dumps(jsonData, indent = 4, sort_keys = True, ensure_ascii = False))

            natName = jsonData['response']['body']['items']['item']['natKorNm']
            natName = natName.replace(' ', '') #중국
            num = jsonData['response']['body']['items']['item']['num'] #인구
            ed = jsonData['response']['body']['items']['item']['ed'] #방한외래관광객
            print('[ %s_%s : %s ]' %(natName, yyyymm, num))
            print('------------------------------------------------------')
            jsonResult.append({'nat_name': natName, 'nat_cd': nat_cd,
                                 'yyyymm': yyyymm, 'visit_cnt': num})
            result.append([natName, nat_cd, yyyymm, num])
    return (jsonResult, result, natName, ed, dataEND)

def main():
    jsonResult = []
    result = []

    print("<< 국내 입국한 외국인의 통계 데이터를 수집합니다. >>")
    nat_cd = input('국가 코드를 입력하세요(중국: 112 / 일본: 130 / 미국: 275) : ')
    nStartYear = int(input('데이터를 몇 년부터 수집할까요? : '))
    nEndYear = int(input('데이터를 몇 년까지 수집할까요? : '))
    ed_cd = "E"  # E : 방한외래관광객, D : 해외 출국

    jsonResult, result, natName, ed, dataEND = getTourismStatsService(nat_cd, ed_cd, nStartYear, nEndYear)  # [CODE 3]

    if (natName == ''):  # URL 요청은 성공하였지만, 데이터 제공이 안된 경우
        print('데이터가 전달되지 않았습니다. 공공데이터포털의 서비스 상태를 확인하기 바랍니다.')
    else:
        # 파일저장 1 : json 파일
        with open('./%s_%s_%d_%s.json' % (natName, ed, nStartYear, dataEND), 'w',
                  encoding='utf8') as outfile:
            jsonFile = json.dumps(jsonResult, indent=4, sort_keys=True, ensure_ascii=False)
            outfile.write(jsonFile)
        # 파일저장 2 : csv 파일
        columns = ["입국자국가", "국가코드", "입국연월", "입국자 수"]
        result_df = pd.DataFrame(result, columns=columns)
        result_df.to_csv('./%s_%s_%d_%s.csv' % (natName, ed, nStartYear, dataEND), index=False, encoding='cp949')
        # result_df.head()

if __name__ == "__main__":
    main()