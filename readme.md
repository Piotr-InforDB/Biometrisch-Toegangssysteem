# Toegangssysteem met Microservices en MQTT

## Installatie & Gebruik

### Clone de repository
   `git clone https://github.com/Piotr-InforDB/Biometrisch-Toegangssysteem && cd toegangssysteem`

### MQTT Configuratie
- Maak een gebruikersbestand:  
  `mosquitto_passwd -c ./mqtt-broker/config/passwd <username>`
- Voeg ACL toe in `mqtt-broker/config/acl`:  
  `user <username>`  
  `topic readwrite #`

### Start services met Docker Compose  
   `docker-compose up -d --build`

### Check logs  
   `docker logs <container_name>`

### Stoppen en verwijderen  
   `docker-compose down`

[//]: # (### Beveiliging )
[//]: # (   `chmod 0700 ./mqtt-broker/config/passwd ./mqtt-broker/config/acl`  )
[//]: # (   `chown mosquitto ./mqtt-broker/config/passwd ./mqtt-broker/config/acl`)
