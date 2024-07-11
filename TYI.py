import re
from lxml import etree

import requests


class TYI:
    def __init__(self, head=None):
        if head is None:
            head = {"User-Agent": "Mediapartners-Google"}
        # 本类前缀
        self.__prefix = " | From class TYI : "

        # http标头                                   dict
        self.Head = head
        # Original_Url                              tuple
        self.o_url = ("https://dict.youdao.com/result?word=", "&lang=en")
        # 翻译对象，自动将 space & / & % 替换成URL编码   str
        self._obj = "None"
        # 例句前缀                                    str
        self.lj_pre = "lj%3A"
        # 百科前缀                                    str
        self.bk_pre="bk%3A"

        # 网页response                               request
        self.__response = None
        # 记录最后一次请求的请求状态                     int
        self.status = None
        # 记录上一次请求是否成功                        bool
        self.if_suc = False
        # 网页源数据                                  str
        self._content = None
        # lxml解析数据                               etree
        self._html = None

        # 例句部分
        # 例句源数据                                 str
        self._lj_con = None
        # 例句解析数据                                etree
        self._lj_html = None
        # 例句数据                                   list
        # 双语例句
        self.lj_db = None
        # 原声例句
        self.lj_or=None
        # 权威例句
        self.lj_au=None
        # 例句状态                                   int
        self.lj_status = None

        # 百科部分
        # 百科源数据                                 str
        self._bk_con = None
        # 百科解析数据                                etree
        self._bk_html = None
        # 百科数据                                   list
        self.bk = None
        # 百科状态                                   int
        self.bk_status = None

        # 主页部分
        # 发音 (一般A为英，B为美，支持拼音)               str
        self.pronunA=None
        self.pronunB=None
        # 链接                                        str
        self.pronunAc=None
        self.pronunBc=None

        # 释义                                        list
        # 简明
        self.brief_meaning=None
        # 柯林斯
        self.collins_meaning=None
        # 新汉英
        self.nce=None
        # 现代汉语
        self.ccl=None

        # 翻译                                        str
        self.trans=None

        # 特殊释义                                     list
        # 网络释义
        self.web=None
        # 英英释义
        self.en=None
        # 专业释义
        self.pro=None

        # 短语                                        list
        self.phrase=None

        # 词典短语                                      list
        self.dict_ph=None
        #词源                                         list
        self.ph_ori=None

        # 猜你想搜                                      list
        self.guess=None

        # 提示                                        str
        self.tip=None


    def getExample(self):
        lj=[]

    def __ReloadStatus__(self):
        # 清空当前状态
        # 网页response                               request
        self.__response = None
        # 记录最后一次请求的请求状态                     int
        self.status = None
        # 记录上一次请求是否成功                        bool
        self.if_suc = False
        # 网页源数据                                  str
        self._content = None
        # lxml解析数据                               etree
        self._html = None

        # 例句部分
        # 例句源数据                                 str
        self._lj_con = None
        # 例句解析数据                                etree
        self._lj_html = None
        # 例句数据                                   list
        # 双语例句
        self.lj_db = None
        # 原声例句
        self.lj_or = None
        # 权威例句
        self.lj_au = None
        # 例句状态                                   int
        self.lj_status = None

        # 百科部分
        # 百科源数据                                 str
        self._bk_con = None
        # 百科解析数据                                etree
        self._bk_html = None
        # 百科数据                                   list
        self.bk = None
        # 百科状态                                   int
        self.bk_status = None

        # 主页部分
        # 发音 (一般A为英，B为美，支持拼音)               str
        self.pronunA = None
        self.pronunB = None
        # 链接                                        str
        self.pronunAc = None
        self.pronunBc = None

        # 释义                                        list
        # 简明
        self.brief_meaning = None
        # 柯林斯
        self.collins_meaning = None
        # 新汉英
        self.nce = None
        # 现代汉语
        self.ccl = None

        # 翻译                                        str
        self.trans = None

        # 特殊释义                                     list
        # 网络释义
        self.web = None
        # 英英释义
        self.en = None
        # 专业释义
        self.pro = None

        # 短语                                        list
        self.phrase = None

        # 词典短语                                      list
        self.dict_ph = None
        # 词源                                         list
        self.ph_ori = None

        # 猜你想搜                                      list
        self.guess = None

        # 提示                                        str
        self.tip = None

    def _encode(self, s: str):
        st = s.replace("/", "/%2F").replace("%", "%25").replace(" ", "%20")
        st = st.replace("!", "%21")
        st = st.replace('"', "%22")
        st = st.replace("#", '%23')
        st = st.replace("$", "%24")
        st = st.replace("&", "26")
        st = st.replace("'", '%27')
        st = st.replace("(", "%28")
        st = st.replace(")", "%29")
        st = st.replace("*", "%2A")
        st = st.replace("+", "%2B")
        st = st.replace(",", "%2C")
        st = st.replace("-", "%2D")
        st = st.replace(".", "%2E")
        st=st.replace(":","%3A")
        return st

    def setObj(self, obj: str):
        self._obj = self._encode(obj)

    def __GetContent__(self):
        # 获取第一页数据
        try:
            # 刷新状态
            self.__ReloadStatus__()
            # 发送请求
            self.__response = requests.get(self.o_url[0] +
                                           self._obj +
                                           self.o_url[1],
                                           headers=self.Head)
            # 获取响应码 & 更新状态
            self.status = self.__response.status_code
            self.if_suc = True
            # 获取网页数据
            self._content = self.__response.text
            self._html = etree.HTML(self._content)

            # 获取例句
            try:
                self.__response = requests.get(self.o_url[0] +
                                               self.lj_pre+
                                               self._obj +
                                               self.o_url[1],
                                               headers=self.Head)
                # 获取例句数据
                self._lj_con= self.__response.text
                self._lj_html=etree.HTML(self._lj_con)

            except requests.exceptions.RequestException as er:
                print(self.__prefix,
                      "RequestError: No example information was available or failed to request for data.")
                print(type(er), " | ", er)
                self.lj_status = re.search(r"(?<=port=)\d+", str(er)).group(0)

            # 获取百科
            try:
                self.__response = requests.get(self.o_url[0] +
                                               self.bk_pre +
                                               self._obj +
                                               self.o_url[1],
                                               headers=self.Head)
                # 获取例句数据
                self._bk_con = self.__response.text
                self._bk_html = etree.HTML(self._bk_con)

            except requests.exceptions.RequestException as er:
                print(self.__prefix,
                      "RequestError: No encyclopedia information was available or failed to request for data.")
                print(type(er), " | ", er)
                self.bk_status = re.search(r"(?<=port=)\d+", str(er)).group(0)

        except requests.exceptions.RequestException as er:
            print(self.__prefix, "RequestError: Failed to request for data.")
            print(type(er), " | ", er)
            self.status = re.search(r"(?<=port=)\d+", str(er)).group(0)


if __name__ == '__main__':
    a = TYI()
    a.__GetContent__()
    print(a.status)
