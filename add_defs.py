import argparse
import re
import sqlite3
import os

def get_defs_dict(defs_file):
    res = {}
    if not os.path.isfile(defs_file):
        print("definitions file does not exist: {}".format(defs_file))
        exit(-1)
    with open(defs_file) as my_file:
        for line in my_file:
            match = re.search("^.(\w+).\t\s*([^\t]*)", line)
            if match.group(1) is None or match.group(2) is None:
                print("match not found for {}".format(line))
                exit(-1)
            res[match.group(1)] = match.group(2)
    return res

def add_defs(defs_dict, db_file):
    if not os.path.isfile(db_file):
        print("database does not exist: {}".format(db_file))
        exit(-1)
    db = sqlite3.connect(db_file)
    for row in db.execute('SELECT word FROM words'):
        word = row[0]
        if word in defs_dict:
            db.execute("UPDATE words SET definition = ? WHERE word = ?", (defs_dict[word], word))
        else:
            print("not found in definitions dictionary: {}".format(word))
            pass
    db.commit()
    db.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", type=str, help="filename of the sqlite database file")
    parser.add_argument("--defs", type=str, help="filename of the zyzzyva exported definitions")
    args = parser.parse_args()
    if not args.db or not args.defs:
        print("required: db and defs")
        exit(-1)
    
    defs_dict = get_defs_dict(args.defs)
    add_defs(defs_dict, args.db)