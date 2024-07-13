from  import TYI

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
