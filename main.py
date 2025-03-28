# encoding=utf8

import json
import os
import webbrowser

from wox import Wox, WoxAPI

from util import Logger


class Main(Wox):        
    def load_config(self):
        """加载配置文件"""
        config_path = os.path.join(os.path.dirname(__file__), "config.json")
        default_config = {
            "wechat": "https://weixin.sogou.com/weixin?type=2&query={}"
        }
        
        try:
            with open(config_path, "r") as f:
                return json.load(f)
        except:
            return default_config
    
    # 必须有一个query方法，用户执行查询的时候会自动调用query方法
    def query(self, query):
        logger = Logger()        
        logger.info("query is: "+query)
        
        results = []
        results.append({
            "Title": query,
            "SubTitle": "Query {} with multiple SearchEngines.".format(query),
            "IcoPath": "Images/app.ico",
            "JsonRPCAction": {
                "method":"queryWithMultipleSearchEngines",
                "parameters":[query],
                "dontHideAfterAction":False
            }
        })      
        
        logger.info("Query: {}".format(results))
        return results

    def queryWithMultipleSearchEngines(self, query):  
        logger = Logger()   
        logger.info("load urls from config.json")
        queryUrls = self.load_config().values()
        logger.info(queryUrls)
        for searchUrlWithQueryPlaceHolder in queryUrls:
            logger.info("进入逐个打开URL:{}".format(searchUrlWithQueryPlaceHolder))
            url = searchUrlWithQueryPlaceHolder.format(query)
            logger.info(url)
            webbrowser.open_new_tab(url)
        WoxAPI.change_query(query)

if __name__ == "__main__":
    Main()


