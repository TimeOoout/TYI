# TO's Youdao Interfacce
## 基于Python爬虫的有道翻译接口
> 目前只支持英译中/中译英 \
> 作者很懒，几乎不更新/维护 (  ) \
> 目前已经根据有道词典新版进行完全重构
> > 从主要使用正则表达式获取数据改为使用xpath获取数据，数据更加简洁干净 
>
> 
> 仅限个人开发学习使用，<b> 请勿高强度爬虫干扰网站正常运行 </b>

### 新版接口-TYI

> 使用方法：将release文件拷贝到需要使用的项目目录里即可 \
> 后续视情况更新到Pypi

* 接口信息
> <b>以下所有数据类型为 [ 某一类型 / None ] 的均为 [ 未初始化（查询）时 / 未查询到时 ] 为None </b>

| Ord  | 对象名称 | 数据类型 | 数据结构 | 备注     |
| ----- |------ | -------- | ------- |--------|
| ____      |  _____________________________________     |___________________________       |_________________________________________________________________              | ___________________________________________________________________________      |
| 1.    |Head      | dict     | {"User-Agent" : . . . ( str ) }| 填写有效Header，默认为"Mediapartners-Google"|  
| 2.    |_obj |str | 无     | 通过设置函数修改，不建议自行调用修改 |
| 3.    |get_word_pronunciation | bool | 无 |值为True时会在单词发音list中添加声音文件链接，默认为True|
| 4.    |get_bilingual_ex_pronunciation|bool | 无 |值为True时会在双语例句list中添加声音文件链接，默认为True|
| 5.    |get_original_ex_pronunciation |bool |无 | 值为True时会在原声例句list中添加声音文件链接，默认为True|
| 6.    |get_authoritative_ex_pronunciation |bool |无 | 值为True时会在权威例句list中添加声音文件链接，默认为True|
| 7.    |status |int / None |无 |</b>上一次查询的 <b> 新版数据 </b> http返回值 |
| 8.    |if_suc |bool/None |无 |判断上一次查询是否成功（似乎并没有什么用）|
| 9.    |_content|str/None |html|<b> 新版网页源数据 </b> |
| 10.   | _html | lxml.etree._Element/None | —— | _content经过lxml 中etree解析后的数据；|
| 11.   |_lj_con | str/None | html | </b>上一次查询的 <b> 旧版数据 </b> |
| 12.   | _lj_html | lxml.etree._Element/None | —— |_lj_con经过lxml 中etree解析后的数据；|
| 13.   |lj_db|list/None    | [ [ '1' , '2' , '3' , '4' , '5'  ] , [ . . . ] , . . . ] | 1为例句，2为译句，3为来源，4为英式发音，5为美式发音，若get_bilingual_ex_pronunciation=False则没有4、5|
| 14.   | lj_or | list/None | [ [ '1' , '2' , '3' , '4' （, '5'）  ] , [ . . . ] , . . . ] | 1为例句，若有译句则2为译句，3为来源（向后推），否则2为来源，3为英式发音，4为美式，若get_original_ex_pronunciation=False则没有3、4、（ 5 ） |
| 15  |lj_au | list/None|  [ [ '1' , '2' , '3' , '4'  ] , [ . . . ] , . . . ] |1为例句，2为来源，3为英式发音，4为美式发音，若get_authoritative_ex_pronunciation=False则没有3、4|
| 16.   |lj_status|int/None|无 |值表示例句获取情况（http码）（好像也没什么用）|
| 17.   |pronun|list/None |[ 'Eng' , 'Ame' ] |一般有两个值，前一个为英式发音音标，后一个为美式|
| 18.   |pronunc|list/None|['linkEn','linkAme']|一般有两个值，前一个为英式发音链接，后一个为美式|
| 19.   |pinyin |str/None |  'pinyin'  | 一般有一个值，为拼音 |
| 20.   |brief_meaning |list/None|[ ('1', { '2' : 'a' } ) , . .  . ] |1为词性或序号，2为译文，a为释义 |
| 21. | 还没写完 。。。|


~~~
from TYI import TYI

if __name__ == '__main__':
    a = TYI({
        "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 "
            "Safari/537.36 Edg/95.0.1020.44 "
    })
    a.setObj("do")
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


* 输出有点多这里不放了

~~~


## ---下面是旧版(PyTranslator)案例-- -

### 用法
~~~
a=Search_words()              #初始化对象
b=a.Simple_search(“Hello”)    #进行搜索，支持中译英/英译中，返回一个字典
~~~
#### 字典内数据
> 返回的数据可能含有换行符或<b>、</b>标记以及空格，请自行过滤
* b['Word']
> 查询的单词
* b['pronounce']
> 音标
> b["pronounce"][0]为英式 \
> b["pronounce"][1]为美式（部分有）
* b['Simple-meaning']
> 释义（英译中）
* d['Internet-meaning']
> 网络释义
* b['Phrase']
> 相关短语
* b['Sentence']
> 相关句子
* b['Chinese-meaning']
> 释义（中译英）
* b['Guess']
> 猜你想搜（大部分情况为空，反之有可能输入了错误的单词）
* b['Pin-Yin']
> 拼音 

### 示例
~~~
if __name__ == '__main__':
    a=Search_words()
    print("| PyTranslator")
    print("| Version: 0.1.6 beta")
    print("| 按回车键开始检索，输入 'exit()' 以退出")
    while True:
        c=str(input("\n请输入要查询的单词\n查询>>>"))
        if c=='exit()':
            sys.exit()
        d=a.Simple_search(c)
        print("\n您查询的单词是：\n"+d['Word']+"\n")
        if d['pronounce']!=[]:
            print("它的音标是：\n"+d['pronounce'][0]+" | 英 & "+d['pronounce'][1]+' 美')
            print("\n它的意思是：")
            for i in d['Simple-meaning']:
                print(i)

        print("\n它的网络释义有：\n")
        for i in d['Internet-meaning']:
            for h in range(len(i)):
                if h==0:
                    print(i[h])
                else:
                    print("     |"+i[h].replace('<b>','-').replace('</b>','-'))

        print("\n与它相关的词组有：\n")
        for h in d['Phrase']:
            print(h[0]+' ： '+h[1].replace(' ','').replace('\n',''))
            
~~~
