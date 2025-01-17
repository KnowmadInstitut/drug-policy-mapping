# -*- coding: utf-8 -*-
"DrugPolicyMap.py"

import feedparser
import re
import json
import time
import os
from geopy.geocoders import Nominatim

# Configuración
RSS_FEEDS = [
    "https://www.google.com/alerts/feeds/01872346950212075020/15507985768876955442",
    "https://www.google.com/alerts/feeds/01872346950212075020/13592738456099705424",
    "https://www.google.com/alerts/feeds/01872346950212075020/5341380160234851186",
    "https://www.google.com/alerts/feeds/01872346950212075020/9877437808332650381",
    "https://www.google.com/alerts/feeds/01872346950212075020/2050950185955790412",
    "https://www.google.com/alerts/feeds/01872346950212075020/5283678870718380226",
    "https://www.google.com/alerts/feeds/01872346950212075020/16122414043021568554",
    "https://www.google.com/alerts/feeds/01872346950212075020/17366392114772033505",
    "https://www.google.com/alerts/feeds/01872346950212075020/7314051412600896034",
    "https://www.google.com/alerts/feeds/01872346950212075020/13711816824261701821",
    "https://www.google.com/alerts/feeds/01872346950212075020/1024626091151407918",
    "https://www.google.com/alerts/feeds/01872346950212075020/18261878657397615121",
    "https://www.google.com/alerts/feeds/01872346950212075020/16488092157424877300",
    "https://www.google.com/alerts/feeds/01872346950212075020/14265366006190744082",
    "https://www.google.com/alerts/feeds/01872346950212075020/4776535314032621330",
    "https://www.google.com/alerts/feeds/01872346950212075020/15046669131817246698",
    "https://www.google.com/alerts/feeds/01872346950212075020/4530593821469801172",
    "https://www.google.com/alerts/feeds/01872346950212075020/868610497455970878",
    "https://www.google.com/alerts/feeds/01872346950212075020/5821522806395791158",
    "https://www.google.com/alerts/feeds/01872346950212075020/17544772323386217275",
    "https://www.google.com/alerts/feeds/01872346950212075020/4202275151651138343",
    "https://www.google.com/alerts/feeds/01872346950212075020/3828731372178537259",
    "https://www.google.com/alerts/feeds/01872346950212075020/3295480546902346010",
    "https://www.google.com/alerts/feeds/01872346950212075020/6304086962222164521",
    "https://www.google.com/alerts/feeds/01872346950212075020/9969718479880621521",
    "https://www.google.com/alerts/feeds/01872346950212075020/9298621603294203506",
    "https://www.google.com/alerts/feeds/01872346950212075020/8891477933609463614",
    "https://www.google.com/alerts/feeds/01872346950212075020/9457341481161703674",
    "https://www.google.com/alerts/feeds/01872346950212075020/7761231775371803234",
    "https://www.google.com/alerts/feeds/01872346950212075020/16052023127015581049",
    "https://www.google.com/alerts/feeds/01872346950212075020/14618528762864077957",
    "https://www.google.com/alerts/feeds/01872346950212075020/15345833958491747428",
    "https://www.google.com/alerts/feeds/01872346950212075020/10673654886685196800",
    "https://www.google.com/alerts/feeds/01872346950212075020/6664075344137428864",
    "https://www.google.com/alerts/feeds/01872346950212075020/11593791563401631149",
    "https://www.google.com/alerts/feeds/01872346950212075020/17172464200989770713",
    "https://www.google.com/alerts/feeds/01872346950212075020/14265366006190745052",
    "https://www.google.com/alerts/feeds/01872346950212075020/10646315268078852434",
    "https://www.google.com/alerts/feeds/01872346950212075020/9039570584131434634",
    "https://www.google.com/alerts/feeds/01872346950212075020/10646315268078850504",
    "https://www.google.com/alerts/feeds/01872346950212075020/7890067899220446383",
    "https://www.google.com/alerts/feeds/01872346950212075020/2851908895033983104",
    "https://www.google.com/alerts/feeds/01872346950212075020/7683677893196573610",
    "https://www.google.com/alerts/feeds/01872346950212075020/5283678870718380305",
    "https://www.google.com/alerts/feeds/01872346950212075020/4471378157588964973",
    "https://www.google.com/alerts/feeds/01872346950212075020/9559413413532899278",
    "https://www.google.com/alerts/feeds/01872346950212075020/12523096761590479458",
    "https://www.google.com/alerts/feeds/01872346950212075020/342282697543143800",
    "https://www.google.com/alerts/feeds/01872346950212075020/2930808370765872927",
    "https://www.google.com/alerts/feeds/01872346950212075020/14629814561705691542",
    "https://www.google.com/alerts/feeds/01872346950212075020/3146148600593057464",
    "https://www.google.com/alerts/feeds/01872346950212075020/3970775287726633246",
    "https://www.google.com/alerts/feeds/01872346950212075020/1356494377665862087",
    "https://www.google.com/alerts/feeds/01872346950212075020/17635816014965415661",
    "https://www.google.com/alerts/feeds/01872346950212075020/17635816014965412092",
    "https://www.google.com/alerts/feeds/01872346950212075020/4993857720154434310",
    "https://www.google.com/alerts/feeds/01872346950212075020/6316262236871822648",
    "https://www.google.com/alerts/feeds/01872346950212075020/8871527006585091276",
    "https://www.google.com/alerts/feeds/01872346950212075020/4130973173780022122",
    "https://www.google.com/alerts/feeds/01872346950212075020/9786975626766836052",
    "https://www.google.com/alerts/feeds/01872346950212075020/5144274488126041658",
    "https://www.google.com/alerts/feeds/01872346950212075020/3474434860951309264",
    "https://www.google.com/alerts/feeds/01872346950212075020/14710293060482877527",
    "https://www.google.com/alerts/feeds/01872346950212075020/10646315268078852395",
    "https://www.google.com/alerts/feeds/01872346950212075020/4530593821469802274",
    "https://www.google.com/alerts/feeds/01872346950212075020/4558200358794358582",
    "https://www.google.com/alerts/feeds/01872346950212075020/5144274488126040422",
    "https://www.google.com/alerts/feeds/01872346950212075020/17588066172892872061",
    "https://www.google.com/alerts/feeds/01872346950212075020/2747047499171357488",
    "https://www.google.com/alerts/feeds/01872346950212075020/1447816832278231203",
    "https://www.google.com/alerts/feeds/01872346950212075020/9877437808332649348",
    "https://www.google.com/alerts/feeds/01872346950212075020/9301003631655820249",
    "https://www.google.com/alerts/feeds/01872346950212075020/3355835436393953033",
    "https://www.google.com/alerts/feeds/01872346950212075020/3355835436393951674",
    "https://www.google.com/alerts/feeds/01872346950212075020/17943388756403922193",
    "https://www.google.com/alerts/feeds/01872346950212075020/3172691028773162273",
    "https://www.google.com/alerts/feeds/01872346950212075020/6727361044322319894",
    "https://www.google.com/alerts/feeds/01872346950212075020/2176816698376521583",
    "https://www.google.com/alerts/feeds/01872346950212075020/16719833965094972603",
    "https://www.google.com/alerts/feeds/01872346950212075020/17588409156472668558",
    "https://www.google.com/alerts/feeds/01872346950212075020/15574369732216859283"
]

MASTER_JSON = "master_data.json"
OUTPUT_GEOJSON = "drug_policy_alerts.geojson"

# Configuración para geocodificación
USE_GEOCODING = True
geolocator = Nominatim(user_agent="drug_policy_geolocator")

# Funciones auxiliares
def load_master_data():
    if os.path.isfile(MASTER_JSON):
        with open(MASTER_JSON, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_master_data(data):
    with open(MASTER_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def is_duplicate(entry, master_data):
    link_new = entry.get("link", "")
    for item in master_data:
        if item.get("link", "") == link_new:
            return True
    return False

def extract_possible_location(text):
    pattern = r"\b(?:in|at)\s([A-Z][a-zA-Z]+(?:\s[A-Z][a-zA-Z]+)*)"
    matches = re.findall(pattern, text)
    return matches[0] if matches else None

def geocode_location(location_str):
    try:
        time.sleep(1)
        loc = geolocator.geocode(location_str)
        if loc:
            return (loc.latitude, loc.longitude)
    except Exception as e:
        print(f"[ERROR] geocoding {location_str}: {e}")
    return None

def extract_location_from_metadata(entry):
    """
    Intenta extraer ubicación de los metadatos del feed.
    """
    if hasattr(entry, 'geo_lat') and hasattr(entry, 'geo_long'):
        return (float(entry.geo_lat), float(entry.geo_long))
    elif hasattr(entry, 'location'):
        return geocode_location(entry.location)
    return None

def extract_location_from_additional_fields(entry):
    """
    Busca ubicaciones en otros campos como 'author' o 'category'.
    """
    fields_to_check = ['author', 'category', 'source']
    for field in fields_to_check:
        if hasattr(entry, field):
            location = extract_possible_location(getattr(entry, field, ''))
            if location:
                return geocode_location(location)
    return None

def geocode_entry(entry):
    """
    Geolocaliza una entrada basada en metadatos, contenido textual y campos adicionales.
    """
    # 1. Priorizar metadatos geográficos
    coords = extract_location_from_metadata(entry)
    if coords:
        return coords

    # 2. Buscar en campos adicionales como 'author', 'category'
    coords = extract_location_from_additional_fields(entry)
    if coords:
        return coords

    # 3. Extraer desde el texto del título y resumen
    full_text = f"{entry.get('title', '')} {entry.get('summary', '')}"
    possible_location = extract_possible_location(full_text)
    if possible_location:
        coords = geocode_location(possible_location)
        if coords:
            return coords

    # 4. Registrar como no geolocalizado
    print(f"[WARNING] No se pudo geolocalizar: {entry.get('title', 'Sin título')}")
    return None

def generate_description(title, summary, link):
    """
    Genera una descripción coherente incluso si el resumen o título están incompletos.
    """
    if not summary:
        summary = "Descripción no disponible."
    description_text = f"**{title}**\n\n{summary}\n\n[[{link}|Ver la fuente]]"
    return description_text

def generate_apa_citation(title, link, published):
    """
    Genera una referencia APA7 válida incluso si faltan datos.
    """
    if not title:
        title = "Sin título"
    if not published:
        published = "Fecha desconocida"
    if not link:
        link = "Enlace no disponible"
    return f"{title}. ({published}). [Blog post]. Recuperado de {link}"

def determine_type(title, description):
    """
    Determina el tipo de contenido basado en palabras clave en el título o descripción.
    """
    keywords = {
        "prohibicionista": ["prohibición", "guerra contra las drogas", "represión"],
        "antiprohibicionista": ["regulación", "legalización", "reducción de daños"],
        "educativo": ["capacitación", "curso", "información"],
        "noticia": ["reportaje", "informe", "última hora"],
        "opinión": ["editorial", "columna", "análisis"],
    }
    for tipo, palabras in keywords.items():
        if any(palabra in title.lower() or palabra in description.lower() for palabra in palabras):
            return tipo.capitalize()
    return "Otro"

def parse_feed(feed_url):
    feed = feedparser.parse(feed_url)
    entries = []

    for e in feed.entries:
        title = getattr(e, 'title', 'No Title')
        summary = getattr(e, 'summary', '')
        link = getattr(e, 'link', '')
        published = getattr(e, 'published', '')
        source = getattr(e, 'source', 'Fuente desconocida')

        coords = geocode_entry(e)

        new_entry = {
            "title": title,
            "summary": summary,
            "link": link,
            "published": published,
            "lat": coords[0] if coords else None,
            "lon": coords[1] if coords else None,
            "description": generate_description(title, summary, link),
            "apa_citation": generate_apa_citation(title, link, published),
        }
        entries.append(new_entry)

    return entries

def generate_geojson(data):
    geojson_data = {
        "type": "FeatureCollection",
        "features": []
    }

    for item in data:
        lat = item.get("lat")
        lon = item.get("lon")
        if lat is not None and lon is not None:
            feature = {
                "type": "Feature",
                "properties": {
                    "title": item.get("title", "No Title"),
                    "description": item.get("description", "Descripción no disponible."),
                    "published": item.get("published", ""),
                    "apa_citation": item.get("apa_citation"),
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [lon, lat]
                }
            }
            geojson_data["features"].append(feature)

    return geojson_data

# Proceso principal
def main():
    master_data = load_master_data()
    all_entries = []

    for feed_url in RSS_FEEDS:
        entries = parse_feed(feed_url)
        for entry in entries:
            if not is_duplicate(entry, master_data):
                master_data.append(entry)
                all_entries.append(entry)

    save_master_data(master_data)
    geojson_data = generate_geojson(all_entries)

    with open(OUTPUT_GEOJSON, "w", encoding="utf-8") as f:
        json.dump(geojson_data, f, ensure_ascii=False, indent=2)
    print("[INFO] Archivo GEOJSON generado.")

if __name__ == "__main__":
    main()
