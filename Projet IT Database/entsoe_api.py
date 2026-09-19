from entsoe import EntsoePandasClient
import pandas as pd
from datetime import datetime, timedelta
from dotenv import load_dotenv #on chope le dichier .env
import os

def charger_prix_entsoe():
    load_dotenv() #lie le fichier
    token = os.getenv("ENTSOE_KEY") #chope la clef 
    if not token:
        raise Exception("Token ENTSO-E non trouvé dans .env")

    client = EntsoePandasClient(api_key=token)
    country_code = "BE"

    today = datetime.utcnow().date()
    start = pd.Timestamp(today.strftime("%Y%m%d"), tz="Europe/Brussels") #le bot qui va faire la requete sur le site entsoe 
    end = pd.Timestamp((today + timedelta(days=1)).strftime("%Y%m%d"), tz="Europe/Brussels")

    data = client.query_day_ahead_prices(country_code, start=start, end=end) #retourne une serie panda avec le price  
    return data
