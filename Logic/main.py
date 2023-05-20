from standard_chase import *

def main():
    person_relation = Relation("Person",
        ("name", "surname", "phone", "email"),
        (True, True, False, False),
        ("LEJEUNE", "Alban", "0663296514", "Alban.LEJEUNE@gmail.com"),
        ("SEDDIKI", "Bilal", "0663296512", "Bilal.SEDDIKI@gmail.com"),
        ("HAMIMI", "Dany", "0663296511", "Dany.HAMIMI@gmail.com"))
    
    employee_relation = Relation("Employe",
        ("surname", "name", "phone", "email", "id"),
        (True, True, False, False, False),
        ("Alban", "LEJEUNE", "0663296514", "Alban.LEJEUNE@travail.com"))
    
    cadre_relation = Relation("Cadre",
        ("surname", "name", "phone", "email", "id"),
        (True, True, False, False),
        ("Bilal", "SEDDIKI", "0663296514", 130)) 

    # Création de la base de données
    database = Database({
        "Person": person_relation,
        "Employe": employee_relation,
        "Cadre": cadre_relation
    })

    # Contrainte : Une personne doit avoir un travail
    work_tgd = TGD(database,
                   source="Person", 
                   where=("Employe", "Cadre"),
                   default="Employe")

    # Contrainte : L'adresse email doit contenir le symbole "@" 
    email_egd = EGD(database, "Person", ["email"], [lambda t: f"{t['surname']}.{t['name']}@gmail.com"])


    # Définition des contraintes
    constraints = [work_tgd, email_egd]

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
