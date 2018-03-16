import time
import serveur_lire_redis_6
import serveur_graph_8
import serveur_dbscan_91

serveur_lire_redis_6.sortie_rapport()

time.sleep(2)

serveur_graph_8.plot_shema()

time.sleep(2)

serveur_dbscan_91.dbscan()
