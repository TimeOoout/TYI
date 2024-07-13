import time

from TYI import TYI
import pytest

a = TYI({
    "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 "
        "Safari/537.36 Edg/95.0.1020.44 "
})

def test_Ado():
    time.sleep(1)
    a.setObj("do")
    a.queryAll()
    assert 1

def test_Bpronun():
    assert a.pronun!=None

def test_Cpronunc():
    assert a.pronunc!=None

def test_Dtrans():
    assert a.trans==None

def test_Ebrief():
    assert a.brief_meaning!=None

def test_Flabel():
    assert a.label!=None

def test_Gtense():
    assert a.tense!=None

def test_Hweb():
    assert a.web!=None

def test_Ipro():
    assert a.pro!=None

def test_Jro_det():
    assert a.pro_detail!=None

def test_Ken():
    assert a.en!=None

def test_Len_det():
    assert a.en_detail!=None

def test_Mphr():
    assert a.phrase!=None

def test_Ndb():
    assert a.lj_db!=None

def test_Oori():
    assert a.lj_or!=None

def test_Pau():
    assert a.lj_au!=None


def test_Qsyn():
    assert a.synonym!=None

def test_Rcritic():
    assert a.critic!=None

def test_Snihao():

    a.setObj("你好")
    a.queryAll()
    assert 1

def test_Tpinyin():
    assert a.pinyin!=None

def test_Uweb():
    assert a.web!=None

def test_Vphr():
    assert a.phrase!=None

def test_Wdb():
    assert a.lj_db!=None

def test_Xori():
    assert a.lj_or!=None

def test_Ylike():
    time.sleep(1)
    a.setObj("甲鱼喜欢岳岳")
    a.queryAll()
    assert 1

def test_Ztrans():
    assert a.trans is not None

def test_awrapa():
    time.sleep(1)
    a.setObj("do")
    a.queryAll()
    assert 1

def test_bguess():
    assert a.guess==None

def test_ctip():
    assert a.tip==None
