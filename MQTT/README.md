# MQTT paho

### Intallation initial

#### Redis

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

* ```sudo -H pip3 install --upgrade pip```

* ajouté au ```bashrc``` ou au ```zshrc``` cette ligne ```alias python="python3.6"```

```alias pip="pip3.6"```


### Mise a jour de version

```sudo pip install -r requirement.txt```

### Lancer les scripts

* ```mosquitto```

* ```/home/[user]/redis-4.0.8/src/redis-server &```

* Ce mettre dans ce dossier ```/MQTT/App```

* ```python server_client_sub_4.py```

* ```python bague_1.py```


##### Voir les ce qu'il y a dans la bdd redis message par messages

* ```python server_lire_redis_6.py```
