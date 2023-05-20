DROP TABLE IF EXISTS Etudiant;
DROP TABLE IF EXISTS Livre;
DROP TABLE IF EXISTS Lecteur;
DROP TABLE IF EXISTS Emprunt;

CREATE TABLE Etudiant (
    Num_Etu INTEGER,
    Nom VARCHAR,
    Prenom VARCHAR
);

CREATE TABLE Livre (
    Id_Livre INTEGER,
    Titre VARCHAR,
    Auteur VARCHAR
);

CREATE TABLE Lecteur (
    Num_Lecteur INTEGER,
    Nom VARCHAR,
    Prenom VARCHAR,
    Emprunt INTEGER
);

CREATE TABLE Emprunt (
    Num_Lecteur INTEGER,
    Id_Livre INTEGER
);

INSERT INTO Etudiant (Num_Etu, Nom, Prenom) VALUES
(1, 'Abbott', 'William'),
(2, 'Costello', 'Lou'),
(3, 'Laurel', 'Stanley'),
(4, 'Hardy', 'Oliver'),
(5, 'Lloyd','Harold'),
(6, 'Marx', 'Groucho');

INSERT INTO Livre (Id_Livre, Titre, Auteur) VALUES
/* (1, 'The Great Dictator', 'Charles Chaplin'), */
(2, 'Steamboat Bill, Jr.', 'Charles Reisner'),
(3, 'The Gold Rush', 'Charles Chaplin'),
(4, 'The General', 'Buster Keaton'),
(5, 'A Night at the Opera', 'Sam Wood'),
(6, 'Duck Soup', 'Leo McCarey');

INSERT INTO Lecteur (Num_Lecteur, Nom, Prenom, Emprunt) VALUES
(1, 'Abbott', 'Bilal', 2),
(2, 'Costello', 'Lou', 1),
(3, 'Laurel', 'Stanley', 1),
(4, 'Hardy', 'Oliver', 1),
(5, 'Lloyd','Harold', 2),
(6, 'Marx', 'Groucho', 1);

INSERT INTO Emprunt (Num_Lecteur, Id_Livre) VALUES
(1, NULL),
(1, 2),
(2, 3),
(3, 4),
(4, 5),
(5, 6),
(6, 1);