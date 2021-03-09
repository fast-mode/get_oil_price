from .Crawler import Crawler



def get_oil_price():
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
    url = 'http://www.qiyoujiage.com/zhejiang.shtml'
    c = Crawler(url)
    return c.search([0],cMap,fun=None,sleepTime=0.5)[1]
