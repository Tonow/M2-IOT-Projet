import paho.mqtt.publish as publish
import setting
import textwrap
import entre_station as to_station
import setting

print("#"*20)
print(f"Debug = {setting.debug}")
print("#"*20)


def debit_test_valeur():
    debit = -1
    while (0 > debit) or (setting.debit_max < debit):
        debit = input(f"Quelle debit entre 0 et {setting.debit_max} ")
        try:
            debit = int(debit)
            debit_str = str(debit)
            debit_str_longueur = len(debit_str)
            while debit_str_longueur != 4:
                debit_str = "0" + debit_str
                debit_str_longueur = len(debit_str)
        except ValueError:
            print('Entrer un entier')
            debit = -1
    return debit_str

def arriver_user():
    list_sortie_eau = setting.list_sortie_eau

    print("\nVoici la liste des sortie d'eau:")
    for sortie in list_sortie_eau:
        mot = sortie[0].split("_")
        text = " ".join(mot)
        print(f"{text} : {sortie[1]}")

    num_sortie = int(input("\nQue voulez vous ouvrir? : "))

    debit = debit_test_valeur()

    for sortie in list_sortie_eau:
        if num_sortie == sortie[1]:
            mot = sortie[0].split("_")
            text = " ".join(mot)
            num_output = str(sortie[1])
            num_output_longueur = len(num_output)
            while num_output_longueur != 4:
                num_output = "0" + num_output
                num_output_longueur = len(num_output)
            robinet_ouvert(num_output, text, debit)

def robinet_ouvert(num_output, text, debit):
    modif = "ouvert"
    to_station.bague_to_station(str(num_output) + debit)

    while modif != "f":
        modif = input("modifier le debit = m ou fermer = f  m/f : ")
        if modif.lower() == 'm':
            debit = debit_test_valeur()
            print("\nDebit modifier")
            to_station.bague_to_station(str(num_output) + debit)

        if modif.lower() == 'f':
            print("\nRobinet fermer")
            to_station.bague_to_station(str(num_output) + "0000")

arriver_user()
