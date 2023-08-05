#导入相关模块
import pandas as pd
from sqlalchemy import create_engine
import pymysql as pl

class pymysqlpro():
    def __init__(self,username,psw,localhost_info,port_info,database_name):
        self.get_name = username
        self.psw = psw
        self.localhost_info = localhost_info
        self.port_info = port_info
        self.database_name = database_name
           
    #数据查询并返回dataframe
    
    def chaxun(self,sql_info):
        engine=create_engine("mysql+pymysql://"+self.get_name+":"+self.psw+"@"+self.localhost_info+":"+self.port_info+"/"+self.database_name)
        sql=sql_info
        df=pd.read_sql(sql,engine)
        print("查询成功")
        return df
    
    #增删改和建表
    def gai(self,sql_info):
        db=pl.connect(
            user=self.get_name,
            password=self.psw,
            host=self.localhost_info,
            database=self.database_name,
            
        )
        sql=sql_info
        cursor=db.cursor()
        try:
            cursor.execute(sql)
            db.commit()
            print("更改成功！")
        except:
            db.rollback()
            print("更改失败")
        db.close()                  