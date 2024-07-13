import re
from lxml import etree

import requests

'''
所有信息：
1.发音信息                      /
2.简明释义                      /
3.翻译                         /
4.时态                         /
5.网络释义                      /
6.专业释义                      /
7.英英释义                      /
8.短语                         /
9.双语例句                      /
10.原声例句                     /
11.权威例句                     /
12.词典短语                     × 
13.同近义词                     /
14.同根词                      maybe
15.词源                        maybe
16.词语辨析                     /
17.百科                        old_edition
18.标签                        /
19.提示                        /
20.猜你想搜（输入了可能错误的单词） /
21.柯林斯词典
22.新英汉词典
23.现代汉语                     maybe
24.可能要搜（预输入猜测）
25.可能的图片
'''


class TYI:
    def __init__(self, head=None):
        if head is None:
            head = {"User-Agent": "Mediapartners-Google"}
        # 本类前缀
        self.__prefix = " | From class TYI : "

        # 翻译对象，自动将 space & / & % 替换成URL编码   str
        self._obj = None
        # 获取单词发音音频链接
        self.get_word_pronunciation = True
        # 获取双语例句音频链接
        self.get_bilingual_ex_pronunciation = True
        # 获取原声例句音频链接
        self.get_original_ex_pronunciation = True
        # 获取权威例句音频链接
        self.get_authoritative_ex_pronunciation = True
        # http标头                                   dict
        self.Head = head
        # Original_Url                              tuple*2
        self._o_url = ("https://dict.youdao.com/result?word=", "&lang=en")
        # 旧版词典                                   str
        self._old_url = "http://dict.youdao.com/w/"
        # 双语例句url                                 tuple*2
        self._lj_db_url = ("https://dict.youdao.com/example/blng/eng/", "/#keyfrom=dict.main.moreblng")
        # 原声例句url                                 tuple*2
        self._lj_or_url = ("https://dict.youdao.com/example/mdia/", "/#keyfrom=dict.main.moremedia")
        # 权威例句url                                 tuple*2
        self._lj_au_url = ("https://dict.youdao.com/example/auth/", "/#keyfrom=dict.main.moreauth")
        # 百科前缀                                    str
        self._bk_pre = "bk%3A"

        # 刷新状态信息
        self.__RefreshStatus__()

    # 获取旧页数据
    def __GetOldPage__(self):
        # 获取旧版词典信息
        try:
            self.__response = requests.get(self._old_url + self._obj,
                                           headers=self.Head)
            # 获取例句数据
            self._lj_con = self.__response.text
            self._lj_html = etree.HTML(self._lj_con)

        except requests.exceptions.RequestException as er:
            print(self.__prefix,
                  "RequestError: Failed to request for data.")
            print(type(er), " | ", er)
            self.lj_status = re.search(r"(?<=port=)\d+", str(er)).group(0)

    # 获取双语例句
    def __GetDbEx__(self):
        # 双语例句
        try:
            self.__response = requests.get(self._lj_db_url[0] + self._obj + self._lj_db_url[1],
                                           headers=self.Head)
            # 获取例句数据
            self._lj_db_con = self.__response.text
            self._lj_db_html = etree.HTML(self._lj_db_con)

        except requests.exceptions.RequestException as er:
            print(self.__prefix,
                  "RequestError: Failed to request for data.")
            print(type(er), " | ", er)
            self.lj_status = re.search(r"(?<=port=)\d+", str(er)).group(0)

    # 获取原声例句
    def __GetOrEx__(self):
        # 原声例句
        try:
            self.__response = requests.get(self._lj_or_url[0] + self._obj + self._lj_or_url[1],
                                           headers=self.Head)
            # 获取例句数据
            self._lj_or_con = self.__response.text
            self._lj_or_html = etree.HTML(self._lj_or_con)

        except requests.exceptions.RequestException as er:
            print(self.__prefix,
                  "RequestError: Failed to request for data.")
            print(type(er), " | ", er)
            self.lj_status = re.search(r"(?<=port=)\d+", str(er)).group(0)

    # 获取权威例句
    def __GetAuEx__(self):
        # 权威例句
        try:
            self.__response = requests.get(self._lj_au_url[0] + self._obj + self._lj_au_url[1],
                                           headers=self.Head)
            # 获取例句数据
            self._lj_au_con = self.__response.text
            self._lj_au_html = etree.HTML(self._lj_au_con)

        except requests.exceptions.RequestException as er:
            print(self.__prefix,
                  "RequestError: Failed to request for data.")
            print(type(er), " | ", er)
            self.lj_status = re.search(r"(?<=port=)\d+", str(er)).group(0)

    # 获取百科数据
    def __GetBk__(self):
        # 获取百科
        try:
            self.__response = requests.get(self._o_url[0] +
                                           self._bk_pre +
                                           self._obj +
                                           self._o_url[1],
                                           headers=self.Head)
            # 获取例句数据
            self._bk_con = self.__response.text
            self._bk_html = etree.HTML(self._bk_con)

        except requests.exceptions.RequestException as er:
            print(self.__prefix,
                  "RequestError: No encyclopedia information was available or failed to request for data.")
            print(type(er), " | ", er)
            self.bk_status = re.search(r"(?<=port=)\d+", str(er)).group(0)

    # 获取新页数据
    def __GetNewPage__(self):
        try:
            # 发送请求
            self.__response = requests.get(self._o_url[0] +
                                           self._obj +
                                           self._o_url[1],
                                           headers=self.Head)
            # 获取响应码 & 更新状态
            self.status = self.__response.status_code
            self.if_suc = True
            # 获取网页数据
            self._content = self.__response.text
            self._html = etree.HTML(self._content)

        except requests.exceptions.RequestException as er:
            print(self.__prefix, "RequestError: Failed to request for data.")
            print(type(er), " | ", er)
            self.status = re.search(r"(?<=port=)\d+", str(er)).group(0)

    def __GetPronunciation__(self):
        # 一般英语会有两个音标，中文只有一个拼音
        self.pronun = self._html.xpath('//*/span[@data-v-39fab836=""][@class="phonetic"]/text()')
        self.pinyin = self._html.xpath('//*/span[@data-v-15cf3186=""][@class="phonetic"]/text()')
        if self.pinyin == []:
            if self.pronun == []:
                self.pronun = None
            if self.get_word_pronunciation:
                # 1是英式2是美式，中文只有拼音没有发音，下载到了也只有空文件
                self.pronunc = ["https://dict.youdao.com/dictvoice?audio=" + self._obj + "&type=1",
                                "https://dict.youdao.com/dictvoice?audio=" + self._obj + "&type=2"]
                self.pinyin = None
                response = requests.head(self.pronunc[0], headers=self.Head)
                filesize = int(response.headers['Content-Length'])
                if filesize <= 1920:
                    self.pronunc = None
        else:
            self.pronun = None
            self.pinyin = self.pinyin[0]

    def __GetTranslation__(self):
        temp = self._html.xpath('//*/p[@class="trans-content"]/text()')
        if temp != []:
            self.trans = temp[0]
        else:
            self.trans = None

    def __GetBriefMeaning__(self):
        lis = self._html.xpath('//*/span[@data-v-8042e1b4=""][@class="pos"]/text()')
        if lis != []:
            list_c = self._html.xpath('//*/span[@data-v-8042e1b4=""][@class="trans"]/text()')
            self.brief_meaning = []
            for i in range(len(list_c)):
                self.brief_meaning.append((lis[i], list_c[i]))
        else:
            lis = self._html.xpath('//*/span[@data-v-8042e1b4=""][@class="col1 index grey"]/text()')
            if lis != []:
                list_c = self._html.xpath('//*/a[@data-v-8042e1b4=""][@class="point"]/text()')
                list_c2 = self._html.xpath('//*/div[@data-v-8042e1b4=""][@class="word-exp_tran grey"]/text()')
                self.brief_meaning = []
                if list_c2!=[]:
                    for i in range(len(list_c)):
                        self.brief_meaning.append((lis[i], {list_c[i]: list_c2[i]}))
                else:
                    for i in range(len(list_c)):
                        self.brief_meaning.append((lis[i], {list_c[i]: ''}))

    def __GetLabel__(self):
        self.label = self._html.xpath('//*/span[@data-v-8042e1b4=""][@class="exam_type-value"]/text()')
        if self.label == []:
            self.label = None

    def __GetTense__(self):
        # 形式
        tempA = self._html.xpath('//*/span[@data-v-8042e1b4=""][@class="transformation"]/text()')
        # 时态
        tempB = self._html.xpath('//*/span[@data-v-8042e1b4=""][@class="wfs-name"]/text()')
        self.tense = {}
        for i in range(len(tempB)):
            self.tense.setdefault(tempB[i], tempA[i])
        if self.tense == {}:
            self.tense = None

    def __GetWebMeaning__(self):
        # 释义
        tempA = self._html.xpath('//*/div[@class="col2"]/p/text()')
        tempA2 = []
        for i in tempA:
            if "\xa0" in i:
                tempA2.append(i.replace("\xa0", ""))
        tempB = self._html.xpath('//*/p[@class="secondaryFont"]')
        tempB2 = []
        self.web = {}
        for i in range(len(tempB)):
            if tempB[i].xpath('string(.)') != "":
                tempB2.append(tempB[i].xpath('string(.)').replace("\n", "").replace("\t", "; ").replace("    ", ""))
        for i in range(len(tempB2)):
            self.web.setdefault(tempA2[i], tempB2[i])
        if self.web == {}:
            self.web = None

    def __GetProMeaning__(self):
        # 第一个领域
        temp1 = self._lj_html.xpath('//*/a[@hidefocus="true"][@class="p-type selected_link"]/text()')
        # 剩下的
        temp2 = self._lj_html.xpath('//*/a[@hidefocus="true"][@class="p-type"]/text()')
        tempA = temp1 + temp2

        # 每个领域释义
        self.pro = {}
        for i in range(len(tempA)):
            self.pro.setdefault(tempA[i],
                                self._lj_html.xpath('//*/li[@class="ptype_' + str(i) + ' types"]/div/span/text()'))
        if self.pro == {}:
            self.pro = None

        # 数据来源信息
        if self._lj_html.xpath('//*/div[@id="tPETrans"]/p[@class="additional"]/text()') != []:
            self.pro_detail = self._lj_html.xpath('//*/div[@id="tPETrans"]/p[@class="additional"]/text()')[0].replace(
                "\n", "").replace("  ", "")

    def __GetEngMeaning__(self):
        # 英英释义数据来源
        self.en_detail = self._lj_html.xpath('//*/p[@class="via ar"]/a[@target="_blank"][@rel="nofollow"]/text()')
        if self.en_detail != []:
            self.en_detail = self.en_detail[0]
        else:
            self.en_detail = None

        group = self._lj_html.xpath('//*/ul/li/span[@class="pos"]/text()')
        if group != []:
            # 所有词性的释义
            exps = self._lj_html.xpath('//*/ul[@class="ol"]')
            self.en = {}
            # 总词性
            for i in range(len(group)):
                # 每个词性总共释义
                exp = []
                # 单个释义
                single_all = exps[i].xpath('./li')
                for h in range(len(single_all)):
                    exp.append({1: single_all[h].xpath('./span[@class="def"]/text()'),
                                2: single_all[h].xpath('./p[@class="gray"]/a/text()'),
                                3: single_all[h].xpath('./p/em/text()')})

                self.en.setdefault(group[i], exp)

            head = self._lj_html.xpath('//*/h4/span[@class="phonetic"]/text()')
            self.en.setdefault(self._obj, head)

    def __GetPhrases__(self):
        # 英语词组
        wordgroup = self._lj_html.xpath(
            '//*/div[@id="wordGroup"]/p[@class="wordGroup"] | //*/div[@id="wordGroup"]/p[@class="wordGroup collapse"]')
        if wordgroup != []:
            self.phrase = {}
            for i in wordgroup:
                self.phrase.setdefault(i.xpath("./span/a/text()")[0],
                                       i.xpath("./text()")[1].replace("\n", '').replace("  ", ""))
        else:
            wordgroup = self._lj_html.xpath('//*/div[@id="webPhrase"]/div[@class="title"]/following-sibling::*')
            if wordgroup != []:
                self.phrase = {}
                wordgroup.pop()
                for i in wordgroup:
                    self.phrase.setdefault(i.xpath("./span/a/text()")[0],
                                           i.xpath("./text()")[1].replace("\n", '').replace("  ", ""))

    def __GetBilingualExample__(self):
        groups = self._lj_db_html.xpath('//*/ul[@class="ol"]/li')
        order = None
        if groups != []:
            self.lj_db = []
            for i in groups:
                group = i.xpath("./p")
                single = []
                for h in group:
                    ori = h.xpath('./span')
                    detail = h.xpath('./a/text()')
                    sen = ""
                    for g in ori:
                        sen += g.xpath("string(.)")
                    if sen != "":
                        single.append(sen)
                    else:
                        single.append(detail[0])
                if self.get_bilingual_ex_pronunciation:
                    if order == None:
                        response = requests.head("https://dict.youdao.com/dictvoice?audio=" + single[0] + "&type=1",
                                                 headers=self.Head)
                        filesize = int(response.headers['Content-Length'])
                        if filesize <= 1920:
                            response = requests.head("https://dict.youdao.com/dictvoice?audio=" + single[1] + "&type=1",
                                                     headers=self.Head)
                            filesize = int(response.headers['Content-Length'])
                            if filesize > 1920:
                                order = 1
                        else:
                            order = 0
                    single.append("https://dict.youdao.com/dictvoice?audio=" + single[order] + "&type=1")
                    single.append("https://dict.youdao.com/dictvoice?audio=" + single[order] + "&type=2")
                self.lj_db.append(single)

    def __GetOriginalExample__(self):
        groups = self._lj_or_html.xpath('//*/ul[@class="ol"]/li')
        if groups != []:
            self.lj_or = []
            for i in groups:
                group = i.xpath("./p")
                single = []
                for h in group:
                    ori = h.xpath('string(.)')
                    if ori != "":
                        single.append(ori.replace("\n", "").replace("\t", "").replace("  ", ""))

                if self.get_original_ex_pronunciation:
                    single.append("https://dict.youdao.com/dictvoice?audio=" + single[0] + "&type=1")
                    single.append("https://dict.youdao.com/dictvoice?audio=" + single[0] + "&type=2")
                self.lj_or.append(single)

    def __GetAuthoritativeExample__(self):
        groups = self._lj_au_html.xpath('//*/ul[@class="ol"]/li')
        if groups != []:
            self.lj_au = []
            for i in groups:
                group = i.xpath("./p")
                single = []
                for h in group:
                    ori = h.xpath('string(.)')
                    if ori != "":
                        single.append(ori.replace("\n", "").replace("\t", "").replace("  ", ""))

                if self.get_authoritative_ex_pronunciation:
                    single.append("https://dict.youdao.com/dictvoice?audio=" + single[0] + "&type=1")
                    single.append("https://dict.youdao.com/dictvoice?audio=" + single[0] + "&type=2")
                self.lj_au.append(single)

    def __GetMaybe__(self):
        group = self._html.xpath('//*/div[@data-v-10fccf05=""][@class="maybe_word"]')
        if group != []:
            self.guess = []
            for i in group:
                self.guess.append([i.xpath("./a/text()")[0], i.xpath('./p/text()')])

    def __GetTip__(self):
        group = self._html.xpath('//*/span[@data-v-3ace3ba2=""][@class="no-word"]/text()')
        if group != []:
            self.tip = group[0]

    def __GetSynonyms__(self):
        groups = self._lj_html.xpath('//*/div[@id="synonyms"]/ul')
        if groups != []:
            self.synonym = []
            ex = self._lj_html.xpath('//*/div[@id="synonyms"]/ul/li/text()')
            word = self._lj_html.xpath('//*/div[@id="synonyms"]/ul/p')
            for i in range(len(ex)):
                wordgroup = word[i].xpath('./span/a/text()')
                self.synonym.append([[ex[i]], wordgroup])

    '''def __GetCognates__(self):
        groups = self._lj_html.xpath('//*/div[@id="relWordTab"]/text()')
        temp = []
        for i in range(len(groups)):
            groups[i] = groups[i].replace("\n", "").replace(" ", "")
            if groups[i] != "":
                temp.append(groups[i])
        trans=self._lj_html.xpath('//*/div[@id="relWordTab"]/p[@class="wordGroup"]/text()')'''

    def __GetCritic__(self):
        groups = self._lj_html.xpath(
            '//*/div[@id="discriminate"]/div[@class="wt-container"]/div[@class="title"]/span/text()')
        if groups != []:
            self.critic = {}
            group = self._lj_html.xpath(
                '//*/div[@id="discriminate"]/div[@class="wt-container"]/div[@class="collapse-content"]/p/text()')
            group.pop()
            group.pop()
            exp = self._lj_html.xpath(
                '//*/div[@id="discriminate"]/div[@class="wt-container"]/div[@class="collapse-content"]/div[@class="wordGroup"]/p/text()')
            a = []
            for i in exp:
                i = i.replace(" ", "").replace("\n", "")
                if i != '':
                    a.append(i)
            b = []
            for i in range(len(groups)):
                b = groups[i].split(',')
                self.critic.setdefault(groups[i], group[i])
                for h in range(len(b)):
                    self.critic.setdefault(b[h], a[h])

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
        # 新版网页动态加载，通过获取旧版网页获取信息
        # 例句源数据就是旧版网页数据
        # 三个特殊释义 | 短语 | 三种例句 | 词典短语 | 同/近义词 | 同根词 | 词语辨析 都是通过旧版数据解析
        # 例句源数据                                 str
        self._lj_con = None
        # 例句解析数据                                etree
        self._lj_html = None
        # 三种例句分别获取

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

        # 时态信息                                      list
        self.tense = None

        # 标签                                        list
        self.label = None

        # 翻译                                        str
        self.trans = None

        # 特殊释义                                     dict
        # 网络释义
        self.web = None
        # 英英释义
        self.en = None
        # 英英释义数据来源                              str
        self.en_detail = None
        # 专业释义
        self.pro = None
        # 专业释义数据来源                              str
        self.pro_detail = None

        # 双语例句源码
        self._lj_db_con = None
        # 原声例句源码
        self._lj_or_con = None
        # 权威例句源码
        self._lj_au_con = None

        # 双语例句解析
        self._lj_db_html = None
        # 原声例句解析
        self._lj_or_html = None
        # 权威例句解析
        self._lj_au_html = None

        # 短语                                        dict
        self.phrase = None

        # 词典短语                                      list
        self.dict_ph = None
        # 词源                                         list
        self.ph_ori = None
        # 同/近义词                                     list
        self.synonym = None
        # 同根词                                       list
        self.cognates = None
        # 词语辨析                                      list
        self.critic = None

        # 猜你想搜                                      list
        self.guess = None

        # 提示                                          str
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
        self.__GetAllContent__()
        # 解析发音信息
        self.__GetPronunciation__()
        # 解析翻译
        self.__GetTranslation__()
        # 解析简明释义
        self.__GetBriefMeaning__()
        # 获取标签
        self.__GetLabel__()
        # 获取时态
        self.__GetTense__()
        # 获取网络释义
        self.__GetWebMeaning__()
        # 获取专业释义
        self.__GetProMeaning__()
        # 获取英英释义
        self.__GetEngMeaning__()
        # 获取短语
        self.__GetPhrases__()
        # 获取双语例句
        self.__GetBilingualExample__()
        # 获取原声例句
        self.__GetOriginalExample__()
        # 获取权威例句
        self.__GetAuthoritativeExample__()
        # 猜你想搜
        self.__GetMaybe__()
        # 获取提示信息
        self.__GetTip__()
        # 获取同/近义词
        self.__GetSynonyms__()
        # 获取词语辨析
        self.__GetCritic__()

    def __GetAllContent__(self):
        # 获取第一页数据
        self.__GetNewPage__()
        # 获取旧版数据
        self.__GetOldPage__()
        # 获取双语例句
        self.__GetDbEx__()
        # 获取原声例句
        self.__GetOrEx__()
        # 获取权威例句
        self.__GetAuEx__()
        # 获取百科数据
        self.__GetBk__()

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
    a.setObj("甲鱼喜欢岳岳")
    a.queryAll()
    print("拼音       ：", a.pinyin)
    print("音标       ：", a.pronun)
    print("发音链接    ：", a.pronunc)
    print("翻译       ：", a.trans)
    print("简明释义    ：", a.brief_meaning)
    print("考试标签    ：", a.label)
    print("时态       ：", a.tense)
    print("网络释义    ：", a.web)
    print("专业释义    ：", a.pro)
    print("专业释义数据来源：", a.pro_detail)
    print("英英释义    ：", a.en)
    print("英英释义数据来源：", a.en_detail)
    print("短语       ：", a.phrase)
    print("双语例句    ：", a.lj_db)
    print("原声例句    ：", a.lj_or)
    print("权威例句    ：", a.lj_au)
    print("猜你想搜    ：", a.guess)
    print("提示信息    ：", a.tip)
    print("同/近义词   ：", a.synonym)
    print("词语辨析    ：", a.critic)
