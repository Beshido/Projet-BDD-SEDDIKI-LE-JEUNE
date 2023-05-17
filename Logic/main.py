from constraints import *
from standard_chase import *
#import psycopg2

def main():
    # Création de la base de données
    database = Database({
        "Person": Relation("Person",
                            ("LEJEUNE", "Alban", "0663296514", "lejeunealban94@gmail.com"),
                            ("SEDDIKI", "Bilal", "0663296514", "seddikibilal@gmail.com"),
                            ("HAMIMI", "Dany", "0663296514", "danyestsupermochegmail.com"))
    })

    # Définition des attributs
    name_attr = Attribute("name", "Person")
    phone_attr = Attribute("phone", "Person")
    email_attr = Attribute("email", "Person")

    # Contrainte : Deux personnes ne peuvent pas avoir le même numéro de téléphone
    phone_tgd = TGD([phone_attr], [name_attr])

    # Contrainte : L'adresse email doit contenir le symbole "@"
    email_egd = EGD([email_attr], [lambda t: "@" in t[0]])

    # Définition des contraintes
    constraints = [phone_tgd, email_egd]

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
