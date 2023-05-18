from constraints import *
from standard_chase import *
#import psycopg2

def main():
    person_relation = Relation("Person",
        ("name", "surname", "phone", "email"),
        ("LEJEUNE", "Alban", "0663296514", "Alban.LEJEUNE@gmail.com"),
        ("SEDDIKI", "Bilal", "0663296512", "Bilal.SEDDIKI@gmail.com"),
        ("HAMIMI", "Dany", "0663296511", "Dany.HAMIMI@gmail.com"))

    employee_relation = Relation("Employe",
        ("name", "surname", "phone", "email", "id"),
        ("KAABECHE", "Rayane", "0663296510", "a@b", 5151555))

    # Création de la base de données
    database = Database({
        "Person": person_relation
    })

    # Contrainte : Deux personnes ne peuvent pas avoir le même numéro de téléphone
    phone_tgd = TGD("Person", ["phone"], ["name"])

    # Contrainte : L'adresse email doit contenir le symbole "@" 
    email_egd = EGD("Person", ["email"], [lambda t: f"{t['surname']}.{t['name']}@gmail.com"])


    # Définition des contraintes
    constraints = [phone_tgd, email_egd]

    database.constraints = constraints

    # Vérification des contraintes avec Standard Chase
    if database.is_conformant():
        print("La base de données satisfait toutes les contraintes.")
    else:
        print("La base de données ne satisfait pas toutes les contraintes.")

    # Vérification individuelle des contraintes
    #for constraint in constraints:
    #    if isinstance(constraint, TGD):
    #        print(f"La contrainte TGD {constraint.lhs} -> {constraint.rhs} est satisfaite: {constraint.is_satisfied_by(database)}")
    #    elif isinstance(constraint, EGD):
     #       print(f"La contrainte EGD {constraint.lhs} = {constraint.rhs} est satisfaite: {constraint.is_satisfied_by(database)}")


if __name__ == '__main__':
    main()
