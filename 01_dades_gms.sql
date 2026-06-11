CREATE DATABASE escacs

/*Creem la taula dels GMS*/
CREATE TABLE rendiment_gms(
    nom varchar(50),
    obertura varchar(50),
    rendiment float,
    partides int,
    PRIMARY KEY (nom, obertura)
);

/*Inserim les dades calculades a partir de chessgames.com*/
INSERT INTO rendiment_gms (nom, obertura, rendiment, partides) VALUES  
("Mikhail Tal", "C60", 0.6767, 266), 
("Mikhail Tal", "D30", 0.6377, 167), 
("Mikhail Tal", "A10", 0.6821, 162), 
("Anatoly Karpov", "C60", 0.7447, 143), 
("Anatoly Karpov", "D30", 0.6828, 506), 
("Anatoly Karpov", "A10", 0.7225, 173), 
("Garry Kasparov", "C60", 0.7308, 104), 
("Garry Kasparov", "D30", 0.7768, 280), 
("Garry Kasparov", "A10", 0.7459, 122)

/*Creem una taula per les nostres dades*/
CREATE TABLE rendiment_propi(
obertura varchar(50) PRIMARY KEY,
rendiment float,
partides int
);