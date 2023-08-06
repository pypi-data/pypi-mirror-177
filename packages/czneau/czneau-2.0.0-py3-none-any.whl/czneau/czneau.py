'''
CCN
XCD
'''

from .refer import *
from .crawlF import F1

ccn = {
    '_urlComment': 'http://czneau.com/api/comments',
    '_urlNew': 'http://czneau.com/api/posts',
    '_urlHot': 'http://czneau.com/api/hot',
    '_referer': 'http://czneau.com/',
}
CCN = F1.crawl(ccn)


class CCNAnalyse(AnalyseContent):
    def AnalyseContentIter(self, data: Union[str, CCN]):
        if type(data) == str:
            file, data = data, CCN()
            data.loadData(file)
        return (data[x]['content'] for x in data)


xcd = {
    '_urlComment': 'http://xcard.czneau.com/api/comments',
    '_urlNew': 'http://xcard.czneau.com/api/posts',
    '_urlHot': 'http://xcard.czneau.com/api/hot',
    '_referer': 'http://xcard.czneau.com/',
}

XCD = F1.crawl(xcd)


class XCDAnalyse(AnalyseContent):
    def AnalyseContentIter(self, data: Union[str, CCN]):
        if type(data) == str:
            file, data = data, CCN()
            data.loadData(file)
        return (data[x]['content'] for x in data)
