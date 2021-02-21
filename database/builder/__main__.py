import os
import sqlite3

from database.builder.etymologies import get_etymologies
from database.builder.languages import get_language_name
from database.builder.progress import ProgressBar

dir_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
data_sources = os.path.join(dir_path, "data")
database = os.path.join(data_sources, 'etymologies.db')

WORDS = dict()
LANGS = set()
RELS = dict()


def add_word(cursor, word, lang):
    t = (word, lang)
    rowid = cursor.execute('''
    insert into word(string, lang) VALUES (?, ?);
    ''', t).lastrowid
    WORDS[t] = rowid
    return rowid


def add_language(cursor, lang, name):
    t = (lang, name)
    cursor.execute('''
    insert into language VALUES (?, ?);
    ''', t)
    LANGS.add(lang)


def add_rel(c, relationship: str):
    r_text = relationship.replace("_", " ")
    t = (r_text, )
    row_id = c.execute('''
    insert into relationship(name) VALUES (?);
    ''', t).lastrowid
    RELS[relationship] = row_id
    return row_id


def build_database():
    conn = create_database()
    count = 0
    bar = ProgressBar("populat", 'database', 6031431, 30)
    c = conn.cursor()
    bar.start()
    for etymology in get_etymologies():
        if not etymology['s_lang'] in LANGS:
            add_language(c, etymology['s_lang'], get_language_name(etymology['s_lang']))
        if not etymology['t_lang'] in LANGS:
            add_language(c, etymology['t_lang'], get_language_name(etymology['t_lang']))
        s_word_id = WORDS.get((etymology['s_word'], etymology['s_lang']))
        if s_word_id is None:
            s_word_id = add_word(c, etymology['s_word'], etymology['s_lang'])
        t_word_id = WORDS.get((etymology['t_word'], etymology['t_lang']))
        relationship = RELS.get(etymology['relationship'])
        if relationship is None:
            relationship = add_rel(c, etymology['relationship'])
        if t_word_id is None:
            t_word_id = add_word(c, etymology['t_word'], etymology['t_lang'])
        t = (s_word_id, t_word_id, relationship)
        c.execute('''
        INSERT INTO etymology VALUES (?,?,?);
        ''', t)
        count += 1
        if count == 10000:
            bar.update(count)
            count = 0
            conn.commit()

    bar.update(count)
    conn.commit()


def create_database():
    # Delete the old  database
    if os.path.exists(database):
        print('Found old database, deleting')
        os.remove(database)
    print('Creating new database schema...')
    conn = sqlite3.connect(database)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE language
        (iso_code text primary key, name text NOT NULL);
    ''')
    c.execute('''
        CREATE TABLE word
        (id integer primary key autoincrement, string text NOT NULL, lang text NOT NULL,
        foreign key(lang) references language(iso_code));
    ''')
    c.execute('''
        CREATE TABLE relationship
        (id integer primary key autoincrement, name text NOT NULL) 
    ''')
    c.execute('''
        CREATE TABLE etymology
        (source integer, target integer, relationship integer,
        primary key(source, target, relationship),
        foreign key(source) references word(id),
        foreign key(target) references word(id),
        foreign key(relationship) references relationship(id))
    ''')

    c.close()
    conn.commit()
    return conn


if __name__ == '__main__':
    build_database()
