#!/usr/bin/env python

import json
import sqlite3

def main():

  conn = sqlite3.connect('rosterdb.sqlite')
  c = conn.cursor()

  #drop databse if exists and create new databses
  c.executescript(''' 
    DROP TABLE IF EXISTS User;
    DROP TABLE IF EXISTS Course;
    DROP TABLE IF EXISTS Member;

    CREATE TABLE User(name TEXT UNIQUE, id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE);
    CREATE TABLE Course(title TEXT UNIQUE, id INTEGER PRIMARY KEY AUTOINCREMENT
    UNIQUE);
    CREATE TABLE Member(user_id INTEGER, course_id INTEGER, role INTEGER,
    PRIMARY KEY ( user_id, course_id));
    ''')

  #open JSON file
  js = raw_input("Enter JASON file name:")
  if len(js)<1: js = "roster_data.json"

  #read JSON data from file
  jsn = open(js).read()
  jdata = json.loads(jsn)

  #read all lists in JSONs
  for item in jdata:
    user_name = item[0]
    title_course = item[1]
    role = int(item[2])
    #put data to SQL
    c.execute("INSERT OR IGNORE INTO User (name) VALUES (?)",(user_name,))
    c.execute("SELECT id FROM User WHERE name = ?",(user_name,))
    user_id = c.fetchone()[0]
    print user_id

    c.execute("INSERT OR IGNORE INTO Course (title) VALUES (?)",(title_course,))
    c.execute("SELECT id FROM Course WHERE title = ?",(title_course,))
    course_id = c.fetchone()[0]
    print course_id

    c.execute('''INSERT OR REPLACE INTO Member (user_id, course_id, role) VALUES ( ?, ?, ? )''', ( user_id, course_id, role ) ) 

  conn.commit()
  conn.close()


if __name__ == '__main__':
    main()
