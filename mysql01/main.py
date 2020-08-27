import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
from crawling import GETgu, GETcity, GETlist
from table import Connect, CREATE, TRUNCATE, SEARCH_ADDR, INSERT_ADDR, INSERT_TANK
import re


def PrintResult(search_type, name):
    cursor = Connect()

    if search_type == 'tank_search' :
        sql = f"""
                        SELECT CONCAT(a.CITY, '-', a.GU) 지역, t.NAME, t.PRICE, t.SELF, t.REG_DATE
                        FROM ADDRESS a
                        RIGHT JOIN TANK t
                        ON a.GU = t.GU
                        WHERE t.NAME LIKE '%{name}%'
                        ;
                     """
                     
    elif search_type == 'gu_search' :
        sql = f"""
                        SELECT CONCAT(a.CITY, '-', a.GU) 지역, t.NAME, t.PRICE, t.SELF, t.REG_DATE
                        FROM ADDRESS a
                        RIGHT JOIN TANK t
                        ON a.GU = t.GU
                        WHERE t.GU = '{name}'
                        ORDER BY t.PRICE
                        LIMIT 10 
                        ;
                     """
    else:
        print('print_result에서 문제 발생')
        raise Exception      

    cursor.execute(sql)
    rows = cursor.fetchall()
    data = pd.DataFrame(rows)
    data.rename(columns={0: '지역', 1: '주유소명',2:'휘발유가격', 3: '셀프주유여부',4:'등록일'}, inplace=True)
    
    print(data)


def FindVar(results,string):
    dirty_list = re.findall(string,results)
    clean_list = []
    for item in dirty_list :
        item = item.split('=')[1]
        item = item.replace('"','').replace(' ','').replace(';','')
        clean_list.append(item)

    return clean_list




while True:
    
    order = input('[메인메뉴] (1) 주유소등록, (2) 주유소검색, (3) 주유소정보 크롤링, (0) 종료 : ')

    # 주유소 등록.  지역명이 DB에 없을 경우만 등록

    if order == '1':

        name = input('주유소 이름 : ')
        gu = input('위치한 구 이름 : ')
        if SEARCH_ADDR(gu) == 0 :
            city = input('구가 속한 시의 이름 : ')
            INSERT_ADDR(city, gu)            
        price = input('가격 : ')
        while True:
            try :
                _self = input('셀프주유가 가능한가요? [Y/N]').upper()
                if _self in ('Y','N') :
                    break
            except:
                print('Y나 N을 입력해주세요')
            
  
        INSERT_TANK(name, gu, price, _self)

    #주유소검색
    elif order == '2':
        while True:
            search = input('[주유소검색] (1)주유소명검색, (2)저렴한주유소(TOP10), (0)이전메뉴로 : ')
            
            if search == '1':
                tank_name = input('주유소명을 입력해주세요 : ')
                
                PrintResult('tank_search',tank_name)

                break
                
            elif search == '2':
                gu_name = input('구 이름을 입력하세요 : ')

                      
                PrintResult('gu_search',gu_name)

                break
                
            elif search == '0':
                break
            else:
                print('0,1,2 중 입력해주세요')


    # 기존 db 삭제후 크롤링         
    elif order == '3':

        TRUNCATE()

        cities = GETcity()
        for city in cities :
            gu_json = GETgu(city)

            gu_list = [ gu['SIGUNGU_NM'] for gu in gu_json ]
            for gu in gu_list :
                INSERT_ADDR(city, gu)
                results = GETlist(city,gu)

                names = FindVar(results,'var OS_NM .*;')
                prices = FindVar(results,'var B027_P .*;')
                selfs = FindVar(results,'var SELF_DIV_CD .*;')
                
                for name,price,_self in zip(names,prices,selfs[:41]) :
                     INSERT_TANK(name, gu, price, _self)      
             
        

    elif order == '0':
        print('종료되었습니다')
        break

    else :
        print('1,2,3,0 중 하나를 입력해주세요')

