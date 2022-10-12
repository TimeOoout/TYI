import sys

import requests
import re
from lxml import etree

class Search_words():

    #def __init__(self):

    def Simple_search(self,word:str):
        head={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36 Edg/95.0.1020.44"
        }
        url="http://dict.youdao.com/w/"+word
        respone=requests.get(url)
        text=respone.text
        html=text
        #print(text)
        text=etree.HTML(text)

        send={}

        send.setdefault("Word",word)

        #print(word)
        #音标
        pronu=text.xpath('//*[@id="phrsListTab"]/h2/div/span/span')
        pronounce=[]
        for i in pronu:
            pronounce.append(i.text)
        #print(pronounce)
        send.setdefault("pronounce",pronounce)

        #释义
        Simple_mean=text.xpath('//*[@id="phrsListTab"]/div/ul/li')
        Simple_meaning=[]
        for i in Simple_mean:
            Simple_meaning.append(i.text.replace('\n','').replace(' ',''))
        #print(Simple_meaning)
        send.setdefault("Simple-meaning",Simple_meaning)

        #释义（中文->En
        En_mean=text.xpath('//*[@id="phrsListTab"]/div/ul/p/span/a')
        En_meaning=[]
        for i in En_mean:
            En_meaning.append(i.text)
        send.setdefault("Chinese-meaning",En_meaning)

        #拼音
        ping=text.xpath('//*[@id="phrsListTab"]/h2/span[2]')
        pin_yin=[]
        for i in ping:
            pin_yin.append(i.text)
        send.setdefault("Pin-Yin",pin_yin)

        #中文拼音意思
        Ch_mean=text.xpath('//*[@id="phrsListTab"]/div/ul/li')
        Ch_meaning=[]
        for i in Ch_mean:
            Ch_meaning.append(i.text)
        send.setdefault('Ch-meaning',Ch_meaning)

        #网络释义
        i_m_t=re.compile('''<a href="#" title="详细释义" rel="#rw1" class="sp do-detail">&nbsp;</a>
        <span>
                (.+?)</span>
    </div>
    <p class="collapse-content">
    (.+?)</p>
            <p class="collapse-content via">(.+?)<span class="sl">-</span><a href=".+?">相关网页</a></p>
    </div>
                <div class="wt-container wt-collapse">''')
        Internet_mean_type=i_m_t.findall(html)
        #print(Internet_mean_type)
        send.setdefault("Internet-meaning",Internet_mean_type)

        #短语
        short=text.xpath('//*[@id="webPhrase"]/p/span/a')
        ph=text.xpath('//*[@id="webPhrase"]/p/text()[1]')
        a=re.compile('''<p class="wordGroup">
  
      <span class="contentTitle"><a class="search-js" href=".+?">(.+?)</a></span>
                          (.+?)
              </p>''',re.DOTALL)
        phrase=a.findall(html)
        phr=[]
        for i in phrase:

            c=i[1].replace('\t','').replace('\n','')
            b=re.compile('<(.+?)>').findall(c)
            d=re.compile('<(.+?)>').findall(i[0])
            e=i[0].replace('\t','')
            for h in b:

                c=c.replace('<'+h+'>','')
            for h in d:
                e=e.replace('<'+h+'>','')
            phr.append((e.replace('\n','').replace('\t','').replace('<a>','').replace('</a>','').replace('<p>','').replace('</p>',''),c.replace('<spanclass=gray>','').replace('</span>','').replace('\n','')))
        '''for i in range(len(short)):
            phrase.append((short[i].text,ph[i].replace(' ','').replace('\n','').replace('\t','')))'''
        #print(phr)
        send.setdefault("Phrase",phr)

        #专业释义
        '''further=text.xpath('//*[@id="tPETrans-type-list"]/a')
        further_mean=text.xpath('//*[@id="tPETrans-all-trans"]/li/div/span[1]')
        further_list=[]
        for i in range(len(further)):
            #print(further_mean[i].text)
            further_list.append((further[i].text,further_mean[i].text.replace('\n','') ))
        #print(further_list)
        send.setdefault('Profession',further_list)'''

        #句子
        # print(html)
        # sen=re.compile('<span id=.+? onmouseover=.+? onmouseout="unhlgt.+?>(.+?)</span><span>')
        # sen=sen.findall(html)
        # sentence=[]
        # for i in sen:
        #     sentence.append(i)
        # print(sentence)

        sen=text.xpath('/html/body/div[1]/div[2]/div[1]/div[2]/div[2]/div/div/div[1]/ul/li/p/span')
        sentence1=[]
        for i in sen:
            sentence1.append(i.text)
        #print(sentence1)
        sen=text.xpath('/html/body/div[1]/div[2]/div[1]/div[2]/div[2]/div/div/div/ul/li/p/span/b')
        sentence=[]
        for i in sen:
            sentence.append(i.text)
        #print(sentence)
        for h in range(len(sentence)):
            for i in range(len(sentence1)):
                if sentence1[i]==None:
                    sentence1[i]='<font color=dodgerblue face="微软雅黑" size=4><b>'+sentence[h]+'</b></font>'
                    break
        print(sentence1)
        group=[]
        senten=''
        print(sentence)
        for i in sentence1:
            if  ('.' not in i) and ('。' not in i):
                #print(i)
                senten+=i
            else:
                group.append((senten+i))
                senten=''
        print(group)
        send.setdefault("Sentence",group)

        try:
            other=text.xpath('/html/body/div[1]/div[2]/div[1]/div[2]/div[2]/div[1]/div[2]/p')
            for i in other:
                i=i.text
            ret=''
            num=0
            for h in range(len(i)):
                if i[h]!='[' and i[h]!=' ' and i[h]!=']':
                    ret+=i[h]
            ret=ret.replace('\n',':')
            rest=''
            now=0
            for i in ret:
                if i ==':':
                    num+=1

                if num%2!=0 and num!=1 and i==':':
                    rest+=' ; '
                elif now!=0:
                        rest+=i
                now+=1
            if len(rest)>6:
                send.setdefault('Others','['+rest+']')
            else:
                send.setdefault('Others','')
        except:
            print('others error')
        try:
            guess_e=text.xpath('/html/body/div[1]/div[2]/div[1]/div[2]/div[2]/div[1]/div/p/span/a')
            e_=[]
            for i in guess_e:
                e_.append(i.text.replace('\n',''))
            guess_c=text.xpath('/html/body/div[1]/div[2]/div[1]/div[2]/div[2]/div[1]/div/p/text()')
            c_=[]
            for i in guess_c:
                i=i.replace('\n','').replace(' ','')
                if i!='':
                    c_.append(i)
            guess=[]
            print(e_,c_)
            for i in range(len(e_)):
                guess.append((e_[i],c_[i]))
            send.setdefault('Guess',guess)
        except:
            send.setdefault('Guess',[])



        return send

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
