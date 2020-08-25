import requests
from selenium import webdriver
from bs4 import BeautifulSoup as bs
import time


def STRtoDICT(string):
    toDICT= dict()
    items = string.replace(' ','').split('\n')
    for item in items :
        if item =='':
            continue
        key, var = item.split(':',1)
        if var == '':
            toDICT[key] = None
        else:
            toDICT[key] = var
    return toDICT

def GETcity():

    cities = []
    
    headers_str = """
                    Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
                    Accept-Encoding: gzip, deflate
                    Accept-Language: ko,en;q=0.9,en-US;q=0.8
                    Connection: keep-alive
                    Cookie: WMONID=Me1s7WN-h4V; JSESSIONID=CSK70RG65E2gaNq8cLaVQ6mccOpiAgDbiOkidMi0L1liAMyaVt7baaGaQtl1xOHb.opwas_2_servlet_engine1; NetFunnel_ID=5002%3A200%3Akey%3D18E98F6E77EEC2591AFA80305056E81F1C97C3BFDCE1AF2724411ED520E4BB549AE4D91CFEBD8C513C28A072C1C59C75F97F4E1F8D2816B448685DFF3C519964EDA216B5A4016D80B04E5478C89AA3A7C05C4FB4A117B63488D854A91AD6BDF119EAB572EDAEC9EDB46EC5D0DE4A6F78%26nwait%3D0%26nnext%3D0%26tps%3D0%26ttl%3D0%26ip%3Dnfl.opinet.co.kr%26port%3D443
                    Host: www.opinet.co.kr
                    Referer: http://www.opinet.co.kr/user/main/mainView.do
                    Upgrade-Insecure-Requests: 1
                    User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36 Edg/84.0.522.63
                """
    headers = STRtoDICT(headers_str)
    session = requests.session()
    session.get("http://www.opinet.co.kr/")

    req = session.post("http://www.opinet.co.kr/searRgSelect.do", headers=headers)
    soup = bs(req.text,"html.parser")
    options = soup.select('select[id=SIDO_NM0] > option')
    for option in options :
        value = option.attrs['value']
        if value == '':
            continue
        cities.append(value)
        
    return cities

    


    
def GETgu(city):  
    data_str = f'SIDO_NM: {city}'    
    headers_str = '''Accept: */*
                User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36 Edg/84.0.522.63
                X-Requested-With: XMLHttpRequest
'''
    data = STRtoDICT(data_str)
    headers = STRtoDICT(headers_str)
    session = requests.session()
    session.get("http://www.opinet.co.kr/")

    req = session.post("http://www.opinet.co.kr/common/sigunguGisSelect.do", data=data, headers=headers)
    return req.json()['result']
    

def GETlist(city,gu):
    
    data_str = f'''
                BTN_DIV: os_btn
                BTN_DIV_STR: 
                POLL_ALL: all
                SIDO_NM: {city}
                SIGUNGU_NM: {gu}
                SIDO_CD: 02
                SIGUN_CD: 0209
                MAP_CENTER_X: 
                MAP_CENTER_Y: 
                MAP_ZOOM: 
                MAP_FIRST_X: 
                MAP_FIRST_Y: 
                LPG_YN: 
                SESSION_USER_ID: 
                SIDO_NM0: {city}
                SIGUNGU_NM0: {gu}
                DONG_NM: 
                GIS_X_COOR: 
                GIS_Y_COOR: 
                GIS_X_COOR_S: 
                GIS_X_COOR_E: 
                GIS_Y_COOR_S: 
                GIS_Y_COOR_E: 
                SEARCH_MOD: addr
                OS_NM: 
                OS_ADDR: 
                NORM_YN: on
                SELF_DIV_CD: on
                VLT_YN: on
                KPETRO_YN: on
                KPETRO_DP_YN: on
                POLL_DIV_CD: SKE
                POLL_DIV_CD: GSC
                POLL_DIV_CD: HDO
                POLL_DIV_CD: SOL
                POLL_DIV_CD: RTO
                POLL_DIV_CD: ETC
                '''

    headers_str = '''
            Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
            User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36 Edg/84.0.522.63
            '''
    
    data = STRtoDICT(data_str)
    headers = STRtoDICT(headers_str) 

    session = requests.session()
    session.get("http://www.opinet.co.kr/")

    req = session.post("http://www.opinet.co.kr/searRgSelect.do", data=data, headers=headers)
    test = bs(req.text,"html.parser")
    results = test.select("td.rlist a")
    for item in results:
        script = item.attrs['href'].split('(',1)[1].split(',')
        #INSERT_TANK(name, gu, price, self)
        name = script[24]
        # self : var SELF_DIV_CD 	= "Y";
   		# price		var B027_P
   		# name : var OS_NM 			= "브레인시티주유소";


															
    return None

