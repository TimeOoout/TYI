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
        self._obj = None
        # 例句前缀                                    str
        self.lj_pre = "lj%3A"
        # 百科前缀                                    str
        self.bk_pre = "bk%3A"

        # 刷新状态信息
        self.__RefreshStatus__()

    def __GetPronunciation__(self):
        # 一般英语会有两个音标，中文只有一个拼音
        self.pronun = self._html.xpath('//*/span[@data-v-39fab836=""][@class="phonetic"]/text()')
        self.pinyin = self._html.xpath('//*/span[@data-v-15cf3186=""][@class="phonetic"]/text()')
        if self.pinyin == []:
            if self.pronun ==[]:
                self.pronun=None
            # 1是英式2是美式，中文只有拼音没有发音，下载到了也只有空文件
            self.pronunc = ["https://dict.youdao.com/dictvoice?audio=" + self._obj + "&type=1",
                            "https://dict.youdao.com/dictvoice?audio=" + self._obj + "&type=2"]
            self.pinyin = None
            response = requests.head(self.pronunc[0])
            filesize = int(response.headers['Content-Length'])
            if filesize<=1920:
                self.pronunc=None
        else:
            self.pronun = None
            self.pinyin = self.pinyin[0]

    def __GetTranslation__(self):
        temp=self._html.xpath('//*/p[@class="trans-content"]/text()')
        if temp != []:
            self.trans=temp[0]
        else:
            self.trans=None

    def __GetBriefMeaning__(self):
        list = self._html.xpath('//*/span[@data-v-8042e1b4=""][@class="pos"]/text()')
        if list != []:
            list_c=self._html.xpath('//*/span[@data-v-8042e1b4=""][@class="trans"]/text()')
            self.brief_meaning = []
            for i in range(len(list_c)):
                self.brief_meaning.append((list[i],list_c[i]))
        else:
            list = self._html.xpath('//*/span[@data-v-8042e1b4=""][@class="col1 index grey"]/text()')
            if list != []:
                list_c = self._html.xpath('//*/a[@data-v-8042e1b4=""][@class="point"]/text()')
                list_c2 = self._html.xpath('//*/div[@data-v-8042e1b4=""][@class="word-exp_tran grey"]/text()')
                self.brief_meaning = []
                for i in range(len(list_c)):
                    self.brief_meaning.append((list[i],{ list_c[i]:list_c2[i]}))

        """        list=self._html.xpath('//*/span[@data-v-8042e1b4=""]/text()')
                    if list!=[]:
                        order = True
                        self.brief_meaning=[]
                        temp=["",""]
                        for i in list:
                            if order:
                                temp[0]=i
                                order=False
                            else:
                                temp[1]=i
                                order=True
                                self.brief_meaning.append((temp[0],temp[1]))
        """

    def __RefreshStatus__(self):
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
        # 发音 (一般0为英，1为美，支持拼音)               list
        self.pronun = None
        # 链接 (同上)                                 list
        self.pronunc = None
        # 拼音                                        str
        self.pinyin = None

        # 释义                                        list
        # 简明
        self.brief_meaning = None
        # 柯林斯
        self.collins_meaning = None
        # 新汉英
        self.nce = None
        # 现代汉语
        self.ccl = None

        # 标签                                        list
        self.label=None

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
        # 同/近义词                                     list
        self.synonym = None
        # 同根词                                       list
        self.cognates = None

        # 猜你想搜                                      list
        self.guess = None

        # 提示                                        str
        self.tip = None

    def setObj(self, obj: str):
        self._obj = self._encode(obj)

    def queryAll(self, obj: str = None):
        # 刷新状态
        if obj is not None:
            self.setObj(obj)
        # 刷新状态
        self.__RefreshStatus__()
        # 获取所有数据
        self.__GetContent__()
        # 解析发音信息
        self.__GetPronunciation__()
        # 解析翻译
        self.__GetTranslation__()
        # 解析简明释义
        self.__GetBriefMeaning__()

    def __GetContent__(self):
        # 获取第一页数据
        try:
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
                                               self.lj_pre +
                                               self._obj +
                                               self.o_url[1],
                                               headers=self.Head)
                # 获取例句数据
                self._lj_con = self.__response.text
                self._lj_html = etree.HTML(self._lj_con)

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

    @staticmethod
    def _encode(s: str):
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
        st = st.replace(":", "%3A")
        return st


if __name__ == '__main__':
    a = TYI({
        "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 "
            "Safari/537.36 Edg/95.0.1020.44 "
    })
    a.setObj("When do I have a midnight snack")
    a.queryAll()
    print(a.pinyin)
    print(a.pronun)
    print(a.pronunc)
    print(a.trans)
    print(a.brief_meaning)
