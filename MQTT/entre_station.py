from datetime import datetime
import setting

list_sortie_eau = setting.list_sortie_eau

def bague_to_station(flux_bague):
    (id_bague, debit) = convertie_entre_bag_to_topic(flux_bague)
    if setting.debug:
        vu_convertion(id_bague, debit)
    cree_data(id_bague, debit)

def convertie_entre_bag_to_topic(flux_bague):
    id_bague = flux_bague[0:4]
    debit = flux_bague[-4:]
    id_bague = prend_dernier_chiffre_flux(id_bague)
    debit = prend_dernier_chiffre_flux(debit)
    return (id_bague, debit)

def prend_dernier_chiffre_flux(flux):
    while flux.startswith('0'):
        flux = flux[1:]
    if flux == '':
        flux = 0
    return flux

def vu_convertion(id_bague, debit):
    print(f"bague : {id_bague}")
    print(f"debit : {debit}")

def cree_data(id_bague, debit):
    '''Avec le topic et message et le temps'''
    time = datetime.now()
    text = ''
    for sortie in list_sortie_eau:
        if int(id_bague) == sortie[1]:
            mot = sortie[0].split("_")
            text = "/".join(mot)
    topic = "home/" + text
    data = {'topic': topic, 'debit': debit, 'date': time}
    if setting.debug:
        print("\n")
        for cle, valeur in data.items():
            print(f"{cle} : {valeur}")
