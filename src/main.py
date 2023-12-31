import psycopg2
from contraintes import TGD, EGD
from algorithm import standard_chase, oblivious_chase

DB_NAME = "projet"
USER = "postgres"
PASSWORD = "test"
HOST = "localhost"
PORT = "5432"

if __name__ == "__main__":
    connection = psycopg2.connect(
        database=DB_NAME,
        user=USER,
        password=PASSWORD,
        host=HOST,
        port=PORT
    )

    cursor = connection.cursor()

    cursor.execute("SELECT * FROM Lecteur;")
    print(cursor.fetchall())
    cursor.execute("SELECT * FROM Etudiant;")
    print(cursor.fetchall())

    contrainte1 = TGD(
        ("Emprunt", ("Id_Livre",)),
        ("Livre", ("Id_Livre",)),
        cursor)
    
    contrainte2 = EGD(
        (("Etudiant", ("Nom",)), ("Lecteur", ("Nom",))),
        ((("Etudiant"), ("Prenom",)), (("Lecteur"), ("Prenom",))),
        cursor)

    tables = ["Emprunt", "Livre", "Etudiant", "Lecteur"]

    if standard_chase([contrainte1, contrainte2], tables):
        print("Standard chase succeeded")
    else:
        print("Standard chase failed")
        
    if oblivious_chase([contrainte1], tables):
        print("Oblivious chase succeeded")
    else:
        print("Oblivious chase failed")

    connection.commit()

    cursor.close()
    connection.close()