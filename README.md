# TO's Youdao Interfacce
## 一个基于Python爬虫的有道翻译接口
> 目前只支持英译中/中译英 \
> 作者很懒，几乎不更新/维护 \
> 目前“猜你想搜”接口似乎无法正常工作 \
> 仅限个人开发学习使用，请勿高强度爬虫干扰网站正常运行

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
