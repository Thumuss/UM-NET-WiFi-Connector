from time import sleep, time
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.ssl_ import create_urllib3_context
from dotenv import load_dotenv
import os
import subprocess


class TLSAdapter(HTTPAdapter):
    """Force TLS 1.2+ for better compatibility"""
    def init_poolmanager(self, *args, **kwargs):
        ctx = create_urllib3_context()
        ctx.set_ciphers("DEFAULT@SECLEVEL=1")
        ctx.check_hostname = False
        kwargs["ssl_context"] = ctx
        return super().init_poolmanager(*args, **kwargs)


url = "https://portail-um-net.umontpellier.fr/undefined"
login_url = "https://portail-um-net.umontpellier.fr/login.html?redirect=http://detectportal.firefox.com/canonical.html"

def is_connected_to_fac_wifi():
    try:
        result = subprocess.run(
            ["iw", "dev", "wlan0", "link"],
            capture_output=True,
            text=True,
            check=True
        )
        output = result.stdout
        # Check for connection and SSID (assuming "UMNET" as the fac WiFi)
        return "Connected to" in output and "UM-net" in output
    except subprocess.CalledProcessError:
        return False

headers = {
    "Host": "portail-um-net.umontpellier.fr",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:145.0) Gecko/20100101 Firefox/145.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Referer": "https://portail-um-net.umontpellier.fr/login.html?redirect=http://detectportal.firefox.com/canonical.html",
    "Content-Type": "application/x-www-form-urlencoded",
    "Origin": "https://portail-um-net.umontpellier.fr",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "DNT": "1",
    "Sec-GPC": "1",
    "Priority": "u=0, i",
}




def request_with_session(username, password):
    data = {
        "username": username,
        "password": password,
        "buttonClicked": "4",
        "redirect_url": "http://detectportal.firefox.com/canonical.html",
        "err_flag": "0",
    }
    with requests.Session() as s:
        try:
            s.mount("https://", TLSAdapter())
            # GET login page to initialize session/cookies
            s.get(login_url, headers=headers, verify=True)
            # Adapter le Referer pour inclure le paramètre redirect
            headers_post = headers.copy()
            headers_post["Referer"] = login_url
            r = s.post(url, headers=headers_post, data=data, verify=True)
            if "Authentication Cache Expired Page" in r.text:
                return False
            return True
        except Exception as e:
            print(f"[SCRIPT_WIFI:{int(time())}] Erreur lors de la requête : {e}")
            return False


if __name__ == "__main__":
    load_dotenv()
    username = os.getenv("USERNAME")
    password = os.getenv("PASSWORD")
    if not username or not password:
        raise ValueError("USERNAME and PASSWORD must be set in the .env file.")
    
    while True:
        if is_connected_to_fac_wifi():
            print(f"[SCRIPT_WIFI:{int(time())}] Connecté au WiFi de la fac, tentative d'authentification...")
            if request_with_session(username, password):
                print(f"[SCRIPT_WIFI:{int(time())}] Authentification réussie.")
            else:
                print(f"[SCRIPT_WIFI:{int(time())}] Échec de l'authentification.")
        else:
            print(f"[SCRIPT_WIFI:{int(time())}] Non connecté au WiFi de la fac. Connexion impossible.")
        sleep(300)  # Attendre 5 minutes avant de vérifier à nouveau


