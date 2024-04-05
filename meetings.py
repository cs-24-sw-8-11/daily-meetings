import sys
import os
from subprocess import check_output
import datetime

import sqlite3

path = "db.db3" if not "--path" in sys.argv else sys.argv[sys.argv.index("--path")+1]

connection = sqlite3.Connection(path)

def init():
    cursor = sqlite3.Cursor(connection)
    cursor.execute("create table if not exists mornings (id integer primary key, date varchar not null, thomas varchar not null, nicolai varchar not null, patrick varchar not null)")
    cursor.execute("create table if not exists afternoons (id integer primary key, date varchar not null, thomas varchar not null, nicolai varchar not null, patrick varchar not null)")
    connection.commit()
    cursor.close()

def insert(table:str, values:list[str]):
    cursor = sqlite3.Cursor(connection)

    date = datetime.datetime.today()

    cursor.execute(f"insert into {table} (date, time, thomas, nicolai, patrick) values ('{date.day}/{date.month}/{date.year}', '{date.hour}:{date.minute}', ?, ?, ?)", values)
    connection.commit()
    cursor.close()


# main

init()

meeting_type = input("Specify meeting type: (mornings, afternoons): ")

if meeting_type == "show":
    print("Morning and afternoon meetings: ")
    print(check_output([
        "sqlite3",
        path,
        "select date,time,nicolai,patrick,thomas from mornings; select date,time,nicolai,patrick,thomas from afternoons",
        "-box"
    ]).decode())

if not meeting_type in ["mornings", "afternoons"]:
    exit()

date = datetime.date.today()
data = {}

group = ["thomas", "nicolai", "patrick"]

shared = input(f"What shared work {'has' if meeting_type == 'afternoons' else 'is'} the group doing today?: ")

for person in group:
    description = input(f"What {'has' if meeting_type == 'afternoons' else 'is'} {person[0].upper() + person[1:]} {'worked' if meeting_type == 'afternoons' else 'working'} on today?: ")
    data[person] = shared + "\n" + description
    
insert(meeting_type, [data[person] for person in group])

print(check_output([
    "sqlite3",
    path,
    "select date,time,nicolai,patrick,thomas from mornings; select date,time,nicolai,patrick,thomas from afternoons;",
    "-box"
]).decode())
