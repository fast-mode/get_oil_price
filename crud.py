from .Crawler import Crawler
import time

all_citys = {
  "北京": "/beijing",
  "上海": "/shanghai",
  "天津": "/tianjin",
  "重庆": "/chongqing",
  "福建": "/fujian",
  "深圳": "/shenzhen",
  "甘肃": "/gansu",
  "广东": "/guangdong",
  "广西": "/guangxi",
  "贵州": "/guizhou",
  "海南": "/hainan",
  "河北": "/hebei",
  "河南": "/henan",
  "湖北": "/hubei",
  "湖南": "/hunan",
  "吉林": "/jilin",
  "江苏": "/jiangsu",
  "江西": "/jiangxi",
  "辽宁": "/liaoning",
  "浙江": "/zhejiang",
  "内蒙古": "/neimenggu",
  "安徽": "/anhui",
  "宁夏": "/ningxia",
  "青海": "/qinghai",
  "山东": "/shandong",
  "陕西": "/shanxi-3",
  "山西": "/shanxi",
  "四川": "/sichuan",
  "西藏": "/xizang",
  "黑龙江": "/heilongjiang",
  "新疆": "/xinjiang",
  "云南": "/yunnan"
}

cache = {}

def _catch_data(city_name:str):
    cMap={
        'div,youjiaCont':{
            'dd':{
                'value 0':'92#',
                'value 1':'95#',
                'value 2':'98#',
                'value 3':'0#'
            }
        }
    }
    #
    url = 'http://www.qiyoujiage.com{}.shtml'
    c = Crawler(url)
    data = c.search([all_citys[city_name]],cMap,fun=None,sleepTime=0.5)
    data["update_date"] = time.strftime("%Y/%m/%d", time.localtime())
    return data

def get_oil_price(city_name:str):
    if city_name not in cache:
        data = _catch_data(city_name)
        cache[city_name] = data
        print("updated")
        return data
    else:
        now = time.strftime("%Y/%m/%d", time.localtime())
        if now != cache[city_name]["update_date"]:
            data = _catch_data(city_name)
            cache[city_name] = data
            print("updated")
            return data
        else:
            return cache[city_name]
