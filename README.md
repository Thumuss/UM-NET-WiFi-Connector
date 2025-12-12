# UM-NET WiFi Connector

Ce script Python automatise la connexion au portail WiFi de l'Université de Montpellier (UM-net).

## Fonctionnalités
- Vérifie si vous êtes connecté au WiFi de la fac (SSID "UMNET").
- Effectue une authentification automatique via le portail.
- Utilise un fichier `.env` pour stocker les identifiants en sécurité.

## Prérequis
- Python 3.x
- Bibliothèque `requests` et `python-dotenv`

## Installation
1. Installez les dépendances :
   ```bash
   pip install requests python-dotenv
   ```

2. Créez un fichier `.env` dans le même dossier :
   ```
   USERNAME=votre_username
   PASSWORD=votre_mot_de_passe
   ```

## Utilisation
Lancez le script :
```bash
python connect.py
```

Le script vérifiera d'abord la connexion WiFi, puis tentera l'authentification si connecté.

## Notes
- Assurez-vous que l'interface WiFi est `wlan0` (modifiez si nécessaire). 
- Si le SSID n'est pas "UM-NET", ajustez la fonction `is_connected_to_fac_wifi`. Cette fonction est basée sur ma configuration sous Arch.
