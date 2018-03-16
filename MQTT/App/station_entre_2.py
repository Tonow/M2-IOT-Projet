import setting
import station_publish_data_3 as station_publish_data

list_sortie_eau = setting.list_sortie_eau()


def bague_to_station(flux_bague):
    (id_bague, debit) = convertie_entre_bag_to_topic(flux_bague)
    if setting.debug:
        vu_convertion(id_bague, debit)
    station_publish_data.publish_data(id_bague, debit)


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
