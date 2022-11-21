import csv
import random
import os

dictonnaire_francais = {}

grammaire_francais = {
    "P": ({"nom": "SN", "place": 1, "obligatoire": True},{"nom": "SV", "place": 2, "obligatoire": True},{"nom": "SPrep", "place": 3, "obligatoire": False}),
    "SN": ({"nom": "ART:ind", "place": 1, "obligatoire": True},{"nom": "NOM", "place": 2, "obligatoire": True}, {"nom": "ADJ", "place": 3, "obligatoire": False}),
    "SV": ({"nom": "VER", "place": 1, "obligatoire": True}, {"nom": "SN", "place": 2, "obligatoire": False}),
    "SPrep": ({"nom": "PRE", "place": 1, "obligatoire": True},{"nom": "SN", "place": 2, "obligatoire": True})
}


def mot_selon_classe(classe, nombre, genre):
    if classe != "":
        i = 0
        while True:
            rand_mot = random.choice(dictonnaire_francais[classe])
            print(rand_mot)
            if(rand_mot["nombre"] == nombre and rand_mot["genre"] == "") or (rand_mot["nombre"] == "" and rand_mot["genre"] == genre) or (rand_mot["nombre"] == nombre and rand_mot["genre"] == genre):
                return rand_mot
            elif(rand_mot["nombre"] == "" and rand_mot["genre"] == "" and classe == "VER"):
                return rand_mot
            if(i == 100):
                print("Error")
                return rand_mot
            i += 1

def VER(nombre, personne):
    while True:
        rand_mot = random.choice(dictonnaire_francais["VER"])
        print(rand_mot)
        if rand_mot["info_verbe"]["nombreVerbe"] == nombre and rand_mot["info_verbe"]["personne"] == personne:
            return rand_mot

def print_syntagme(syntagme, nombre, genre):
    phrase = ""
    for Synt in grammaire_francais[syntagme]:
        if Synt["nom"] in grammaire_francais.keys():
            phrase += print_syntagme(Synt["nom"], nombre, genre)
        else:
            if Synt["nom"] == "VER":
                mot = globals()[Synt["nom"]](nombre, "3")
                phrase += mot["mot"]
                phrase += " "
            elif Synt != "":
                mot = mot_selon_classe(Synt["nom"], nombre, genre)
                phrase += mot["mot"]
                phrase += " "
    return phrase



if __name__ == "__main__":
    with open(r"database\Lexique383.tsv", encoding='utf-8') as file:
        tsv_file = csv.reader(file, delimiter="\t")
        for i, array in enumerate(tsv_file):
            (mot, classeGrammaticale, nombre, genre, info_verbe) = (array[0],array[3], array[5], array[4], array[10])
            if classeGrammaticale in dictonnaire_francais:
                if info_verbe:
                    try: 
                        (mode, temps, personne, nombreVerbe) = (array[10][0:3], array[10][4:7], array[10][8], array[10][9])
                    except:
                        (mode, temps, personne, nombreVerbe) = (array[10][0:3], array[10][4:7], None, None)
                    dictonnaire_francais[classeGrammaticale].append({"mot": mot, "nombre": nombre, "genre": genre, "info_verbe": {"mode": mode, "temps": temps, "personne": personne, "nombreVerbe": nombreVerbe}})
                else:
                    dictonnaire_francais[classeGrammaticale].append({"mot": mot, "nombre": nombre, "genre": genre, "info_verbe": info_verbe})
            else:
                dictonnaire_francais[classeGrammaticale] = [{"mot": mot, "nombre": nombre, "genre": genre, "info_verbe": info_verbe}]

    
    nombre = random.choice(["s","p"])
    genre = random.choice(["f", "m"])
    print(print_syntagme("P", nombre, genre))
