from .Crawler import Crawler
import time

all_citys = {
  "/beijing": "北京",
  "/shanghai": "上海",
  "/tianjin": "天津",
  "/chongqing": "重庆",
  "/fujian": "福建",
  "/shenzhen": "深圳",
  "/gansu": "甘肃",
  "/guangdong": "广东",
  "/guangxi": "广西",
  "/guizhou": "贵州",
  "/hainan": "海南",
  "/hebei": "河北",
  "/henan": "河南",
  "/hubei": "湖北",
  "/hunan": "湖南",
  "/jilin": "吉林",
  "/jiangsu": "江苏",
  "/jiangxi": "江西",
  "/liaoning": "辽宁",
  "/zhejiang": "浙江",
  "/neimenggu": "内蒙古",
  "/anhui": "安徽",
  "/ningxia": "宁夏",
  "/qinghai": "青海",
  "/shandong": "山东",
  "/shanxi-3": "陕西",
  "/shanxi": "山西",
  "/sichuan": "四川",
  "/xizang": "西藏",
  "/heilongjiang": "黑龙江",
  "/xinjiang": "新疆",
  "/yunnan": "云南"
}
time_stamp = time.time()
oil_rt = None

def get_oil_price():
    global oil_rt
    if time.time() - time_stamp > 3600:
        oil_rt = None
    if oil_rt == None:
        oil_rt = []
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
        data = c.search(all_citys.keys(),cMap,fun=None,sleepTime=0.5)
        index = 0
        for k,v in all_citys.items():
            oil_rt.append({
                "city_name":v,
                "92#":data["92#"][index],
                "95#":data["95#"][index],
                "98#":data["98#"][index],
                "0#":data["0#"][index],
            })
            index += 1
    return oil_rt
def get_all_city():
    if len(all_citys) == 0:
        cMap={
            'div,Area':'aa'
        }
        url = 'http://www.qiyoujiage.com/zhejiang.shtml'
        c = Crawler(url)
        request = c.search([0],cMap,fun=None,sleepTime=0.5)[1]
        # 解拼音
        rt = request["aa"]
        rt = rt.split(".shtml")[:-3]
        rt = [x[x.rfind('/'):] for x in rt]
        # 解中文
        cn = request["aa"].split("</a>")[:-3]
        cn = [x[x.rfind('>')+1:] for x in cn]
        for i in range(len(rt)):
            all_citys[rt[i]] = cn[i]
    return all_citys