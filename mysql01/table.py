import pymysql


def Connect():
    db = pymysql.connect(host='localhost',port=3303, user='study',passwd='studymysql',
                            db='oil',charset='utf8',autocommit=True)
    return db.cursor()



def CREATE():
    cursor = Connect()
    sql1= """
        CREATE TABLE IF NOT EXISTS oil.ADDRESS (
                    CITY VARCHAR(10),
                    GU VARCHAR(10)
        );
        """
    sql2="""
        CREATE TABLE IF NOT EXISTS oil.TANK (
                    NAME VARCHAR(10),
                    GU VARCHAR(10),
                    PRICE FLOAT,
                    SELF CHAR(1),
                    REG_DATE DATETIME DEFAULT NOW()
        );
        """
    cursor.execute(sql1)
    cursor.execute(sql2)

def TRUNCATE():
    cursor = Connect()
    sql1 = 'TRUNCATE TABLE oil.ADDRESS;'
    sql2 = 'TRUNCATE TABLE oil.TANK;'
    cursor.execute(sql1)
    cursor.execute(sql2)


def INSERT_TANK(name, gu, price, self):
    cursor = Connect()
        
    sql = f"""
        INSERT INTO oil.TANK
        VALUES(0,'{name}','{gu}',{price},'{self}',current_timestamp());"""
    cursor.execute(sql)
    
    

def INSERT_ADDR(city, gu):   #확인
    cursor = Connect()
    if SEARCH_ADDR(gu) != 0 :
        return 
        
    sql = f"""
        INSERT INTO oil.ADDRESS
        VALUES('{city}','{gu}');"""
    
    cursor.execute(sql)


def SEARCH_ADDR(gu) :
    cursor = Connect()
    sql = f"""
            SELECT COUNT(*) FROM oil.ADDRESS
            WHERE GU = '{gu}';"""
    cursor.execute(sql)
    rows = cursor.fetchone()
    return rows[0]



