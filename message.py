import random
from datetime import datetime
import psycopg2
import psycopg2.extras

con = psycopg2.connect(
        host = "localhost",
        database = "zuil",
        user = "postgres",
        password = "pundenaai")

con.autocommit = True

datum = datetime.now().date().strftime("%d/%m/%Y")
tijd = datetime.now().time().strftime("%H:%M:%S")

name = input("Wat is uw naam/anoniem?")
if name == "anoniem":
    print("Uw naam is anoniem")
else:
    print('Hallo', name)

infile = open(
    'stations.txt').read().splitlines()
rstation = random.choice(infile)
print(rstation)
lijnen = open('tekst.csv', 'r')

def reiziger_insert():
    cursor = con.cursor()

    query = """
            INSERT INTO reiziger (naam, station)
            VALUES (%s, %s) RETURNING reiziger_id;
            """
    cursor.execute(query, (name, rstation, ))
    reiziger_id = cursor.fetchone()[0]
    cursor.close()

    return reiziger_id

reiziger_id = reiziger_insert()

while True:
    bericht = input('Voer hier uw bericht in (max 140 karakters): ')
    if len(bericht) <= 140:
        print('Uw bericht wordt doorgestuurd naar de moderator, Fijne dag nog!')
        break
    else: print('Opnieuw graag! Uw bericht heeft teveel karakters')

file = open('tekst.csv', 'a')
file.write(f"{reiziger_id}, {name}, {datum}, {tijd}, {rstation}, {bericht}\n")


con.commit()
con.close()
