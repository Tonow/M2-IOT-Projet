# MQTT paho

### Intallation initial

#### Redis

```sudo apt-get install redis-server```

ou

* ```wget http://download.redis.io/releases/redis-4.0.8.tar.gz```

* ```tar xzf redis-4.0.8.tar.gz```

* ```cd redis-4.0.8```

* ```make```

#### Mosquitto

```sudo apt-get install mosquitto```

#### Python 3

[doc python ubuntu](https://doc.ubuntu-fr.org/python)

* ```sudo add-apt-repository ppa:jonathonf/python-3.6```

* ```sudo apt update```

* ```sudo apt install python3.6```

* ```sudo apt install python3-pip```

* ajouté au ```bashrc``` ou au ```zshrc``` cette ligne ```alias python=python3```


### Mise a jour de version

```pip install -r requirement.txt```

### Lancer les scripts

* ```mosquitto```

* ```/home/redis-4.0.8src/redis-server```

* Ce mettre dans ce dossier ```/MQTT```

* ```python client_sub.py```

* ```python publish_single.py```


##### Voir les ce qu'il y a dans la bdd redis message par messages

* ```python to_client.py```
