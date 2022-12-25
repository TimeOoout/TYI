from PyTranslator import Search_words
import re
import sqlite3
from pathlib import Path
import time
import logging
import tqdm

__handlerF = logging.FileHandler('dict.log')
__handlerF.setLevel(logging.DEBUG)
__handlerC = logging.StreamHandler()
__handlerC.setLevel(logging.INFO)
__formatter = logging.Formatter('%(asctime)s <%(levelname)s>: %(message)s')
__handlerF.setFormatter(__formatter)
__handlerC.setFormatter(__formatter)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(__handlerF)
logger.addHandler(__handlerC)


def open_table(path: Path) -> sqlite3.Connection:
    if not path.exists():
        conn = sqlite3.connect(path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE WORD(
            EN           TEXT   PRIMARY KEY,
            CN           TEXT   ,
            PRONOUNCE    TEXT   ,
            COMBO        TEXT   );
        ''')
    else:
        conn = sqlite3.connect(path)   
    return conn

def query(searcher: Search_words, word: str) -> tuple[str]:
    res = searcher.Simple_search(word)

    en = res['Word']
    pron = f"{res['pronounce'][0]} 英 & {res['pronounce'][1]} 美" if res['pronounce'] != [] else ''
    cn = re.sub('[ |\']', '', str(list(_ for _ in res['Simple-meaning']))[1 : -1].replace(',', '\n')) 
    combo = re.sub('[ |\']', '', str(list(_[0] + re.sub('[\n| ]', '', _[1]) for _ in res['Phrase']))[1 : -1].replace(',', '\n'))

    return en, cn, pron, combo

def addone(cursor: sqlite3.Cursor, en: str, cn: str, pronounce: str, combo: str) -> None:
    try:
        cursor.execute(f'''
            INSERT INTO WORD (EN, CN, PRONOUNCE, COMBO)
            VALUES ("{en}", "{cn}", "{pronounce}", "{combo}");
        ''')
    except Exception as e:
        logger.error(f'{type(e)}|{str(e)}')


def addmany(conn: sqlite3.Connection, wordlist: list[str], delay: int = 1) -> None:
    searcher=Search_words()
    cursor = conn.cursor()
    for i in tqdm.tqdm(range(len(wordlist))):
        word = wordlist[i]
        en, cn, pron, combo = query(searcher, word)
        addone(cursor, en, cn, pron, combo)
        conn.commit()
        time.sleep(delay)

def run(dbname: str, wordfile: str) -> None:
    with open(wordfile, 'r', encoding = 'utf-8') as f:
        wordlist = f.read().strip().split('\n')

    DATABASE_PATH = Path(__file__).parent / dbname
    conn = open_table(DATABASE_PATH)

    addmany(conn, wordlist)

    conn.close()

if __name__ == '__main__':
    '''
    DB_NAME: 基于sqlite3的数据库名,若不存在自动创建
    wordfile: 单词文件名称, 文件与该脚本同目录

    单词文件格式:每行一个英文单词,回车为分隔符
    '''
    DB_NAME = 'dict.db'
    wordfile = 'word.txt'
    run(DB_NAME, wordfile)
    

    # def verify():
    #     conn = open_table(Path(__file__).parent / 'dict.db')
    #     cur = conn.cursor()
    #     sql = 'select * from WORD'
    #     cur.execute(sql)
    #     x = cur.fetchall()
    #     for each in x:
    #         print(each)
    #         print()
    # verify()
