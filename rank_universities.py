import json
import random

def rank_universities(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        universities = json.load(f)

    # Heuristics for scoring
    # We want to favor big, popular Erasmus cities
    top_cities = ["Madrid", "Lisbon", "Paris", "Vienna", "Porto", "Barcelona", "Valencia", "Lyon", "Hamburg", "Budapest", "Prague", "Stockholm", "Helsinki"]
    medium_cities = ["Granada", "Seville", "Bordeaux", "Toulouse", "Ghent", "Antwerp", "Coimbra", "Bologna", "Turin", "Milan"]
    
    import math

    def haversine(lat1, lon1, lat2, lon2):
        R = 6371  # Earth radius in km
        phi1, phi2 = math.radians(lat1), math.radians(lat2)
        dphi = math.radians(lat2 - lat1)
        dlambda = math.radians(lon2 - lon1)
        a = math.sin(dphi / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return int(R * c)

    # TUL Coordinates (Lodz University of Technology)
    TUL_COORDS = [51.7474, 19.4550]

    # Geocoordinates for Map
    city_coords = {
        "Lisbon": [38.7223, -9.1393],
        "Porto": [41.1579, -8.6291],
        "Madrid": [40.4168, -3.7038],
        "Barcelona": [41.3851, 2.1734],
        "Valencia": [39.4699, -0.3763],
        "Seville": [37.3891, -5.9845],
        "Granada": [37.1773, -3.5986],
        "Paris": [48.8566, 2.3522],
        "Lyon": [45.7640, 4.8357],
        "Bordeaux": [44.8378, -0.5792],
        "Toulouse": [43.6047, 1.4442],
        "Vienna": [48.2082, 16.3738],
        "Innsbruck": [47.2692, 11.4041],
        "Graz": [47.0707, 15.4395],
        "Hamburg": [53.5511, 9.9937],
        "Berlin": [52.5200, 13.4050],
        "Munich": [48.1351, 11.5820],
        "Budapest": [47.4979, 19.0402],
        "Prague": [50.0755, 14.4378],
        "Warsaw": [52.2297, 21.0122],
        "Krakow": [50.0647, 19.9450],
        "Stockholm": [59.3293, 18.0686],
        "Helsinki": [60.1695, 24.9354],
        "Ghent": [51.0543, 3.7174],
        "Antwerp": [51.2194, 4.4025],
        "Brussels": [50.8503, 4.3517],
        "Coimbra": [40.2033, -8.4103],
        "Bologna": [44.4949, 11.3426],
        "Turin": [45.0703, 7.6869],
        "Milan": [45.4642, 9.1900],
        "Rome": [41.9028, 12.4964],
        "Naples": [40.8518, 14.2681],
        "Padua": [45.4064, 11.8768],
        "Pisa": [43.7228, 10.4017],
        "Aveiro": [40.6405, -8.6538],
        "Braga": [41.5454, -8.4265],
        "Covilha": [40.2827, -7.5033],
        "Faro": [37.0179, -7.9308],
        "Guimaraes": [41.4425, -8.2930],
        "Leiria": [39.7438, -8.8078],
        "Vila Real": [41.3010, -7.7448],
        "Viseu": [40.6566, -7.9124],
        "Setubal": [38.5244, -8.8882],
        "Funchal": [32.6505, -16.9085],
        "Ponta Delgada": [37.7412, -25.6756],
        "Tomar": [39.6036, -8.4146],
        "Castelo Branco": [39.8197, -7.4965],
        "Guarda": [40.5384, -7.2661],
        "Beja": [38.0151, -7.8632],
        "Braganca": [41.8058, -6.7572],
        "Santarem": [39.2333, -8.6833],
        "Portalegre": [39.2938, -7.4312],
        "Almada": [38.6790, -9.1569],
        "Adana": [37.0000, 35.3213],
        "Aigaleo": [37.9838, 23.6685],
        "Alcalá de Henares": [40.4818, -3.3643],
        "Amberg": [49.4456, 11.8593],
        "Ankara": [39.9334, 32.8597],
        "Arcavacata di Rende": [39.3621, 16.2256],
        "Astana": [51.1605, 71.4704],
        "Aydın": [37.8444, 27.8458],
        "Balıkesir": [39.6484, 27.8826],
        "Barcelos": [41.5388, -8.6151],
        "Belfort": [47.6397, 6.8638],
        "Bergamo": [45.6983, 9.6773],
        "Bingen am Rhein": [49.9667, 7.8943],
        "Bitola": [41.0297, 21.3292],
        "Blois": [47.5861, 1.3359],
        "Borås": [57.7210, 12.9401],
        "Brandenburg": [52.4125, 12.5539],
        "Braşov": [45.6427, 25.5546],
        "Brest": [48.3904, -4.4861],
        "Bucharest": [44.4268, 26.1025],
        "Cagliari": [39.2238, 9.1217],
        "Caserta": [41.0706, 14.3168],
        "Catania": [37.5079, 15.0830],
        "Compiègne": [49.4179, 2.8260],
        "Cádiz": [36.5271, -6.2886],
        "Deggendorf": [48.8354, 12.9644],
        "Dewathang": [26.8640, 91.4646],  # BHUTAN!
        "Dornbirn": [47.4125, 9.7423],
        "Dundalk": [54.0088, -6.4028],
        "Düzce": [40.8438, 31.1565],
        "Eindhoven": [51.4416, 5.4697],
        "Enschede": [52.2215, 6.8937],
        "Erfurt": [50.9848, 11.0299],
        "Erzurum": [39.9043, 41.2679],
        "Eskişehir": [39.7667, 30.5256],
        "Gif-sur-Yvette": [48.7001, 2.1348],
        "Girona": [41.9794, 2.8214],
        "Grenoble": [45.1885, 5.7245],
        "Groningen": [53.2194, 6.5665],
        "Győr": [47.6875, 17.6504],
        "Ioánnina": [39.6650, 20.8537],
        "Isparta": [37.7648, 30.5566],
        "Istanbul": [41.0082, 28.9784],
        "Kahramanmaraş": [37.5858, 36.9371],
        "Karlsruhe": [49.0069, 8.4037],
        "Kaunas": [54.8985, 23.9036],
        "Kiel": [54.3233, 10.1227],
        "Kocaeli": [40.8533, 29.8815],
        "Kongsberg": [59.6647, 9.6502],
        "Konya": [37.8667, 32.4833],
        "Košice": [48.7164, 21.2611],
        "Lappeenranta": [61.0549, 28.1897],
        "Leioa": [43.3276, -2.9829],
        "León": [42.6000, -5.5703],
        "Liberec": [50.7663, 15.0543],
        "Liepāja": [56.5047, 21.0108],
        "Lille": [50.6292, 3.0573],
        "Linköping": [58.4108, 15.6214],
        "Mannheim": [49.4875, 8.4660],
        "Merseburg": [51.3551, 11.9961],
        "Mittweida": [50.9856, 12.9803],
        "Mytilíni": [39.1044, 26.5560],
        "Nancy": [48.6921, 6.1844],
        "Nantes": [47.2184, -1.5536],
        "Nice": [43.7102, 7.2620],
        "Nicosia": [35.1856, 33.3823],
        "Niš": [43.3209, 21.8958],
        "Noisy-le-Grand": [48.8477, 2.5528],
        "Nottingham": [52.9548, -1.1581],
        "Novi Sad": [45.2671, 19.8335],
        "Oldenburg": [53.1435, 8.2146],
        "Orléans": [47.9030, 1.9093],
        "Osijek": [45.5550, 18.6955],
        "Oslo": [59.9139, 10.7522],
        "Osnabrück": [52.2799, 8.0472],
        "Ostrava": [49.8209, 18.2625],
        "Pamplona": [42.8125, -1.6458],
        "Pejë": [42.6610, 20.2925],
        "Pilsen": [49.7384, 13.3736],
        "Podgorica": [42.4304, 19.2594],
        "Rennes": [48.1173, -1.6778],
        "Reykjavík": [64.1466, -21.9426],
        "Riga": [56.9496, 24.1052],
        "Rouen": [49.4432, 1.0999],
        "Saarbrücken": [49.2326, 6.9969],
        "Saint-Barthélemy-d’Anjou": [47.4682, -0.4952],
        "Sankt Pölten": [48.2043, 15.6229],
        "Santarém": [39.2333, -8.6833],
        "Schiltigheim": [48.6083, 7.7479],
        "Sofia": [42.6977, 23.3219],
        "Strasbourg": [48.5734, 7.7521],
        "Tallinn": [59.4370, 24.7536],
        "The Hague": [52.0705, 4.3007],
        "Tilburg": [51.5555, 5.0913],
        "Tours": [47.3941, 0.6848],
        "Trento": [46.0697, 11.1211],
        "Trollhättan": [58.2837, 12.2886],
        "Tromsø": [69.6492, 18.9553],
        "Trondheim": [63.4305, 10.3951],
        "Turku": [60.4518, 22.2666],
        "Ulm": [48.3984, 9.9916],
        "Valladolid": [41.6523, -4.7245],
        "Varna": [43.2141, 27.9147],
        "Vigo Pontevedra": [42.2406, -8.7207], 
        "Villeneuve dAscq": [50.6232, 3.1434],
        "Weimar": [50.9795, 11.3297],
        "Wildau": [52.3168, 13.6338],
        "Évora": [38.5714, -7.9135],
        "Évry": [48.6298, 2.4418],
        "Ústí nad Labem": [50.6611, 14.0520],
        "İzmir": [38.4237, 27.1428],
        "Şanlıurfa": [37.1674, 38.7955],
        "Unknown": [51.7525, 19.4532] # Default to Lodz
    }

    # Average June Weather (Daytime Highs in Celsius)
    city_weather_june = {
        "Lisbon": 26, "Porto": 23, "Faro": 28, "Coimbra": 25, "Braga": 24, "Aveiro": 22,
        "Madrid": 29, "Barcelona": 25, "Valencia": 27, "Seville": 33, "Granada": 30, "Malaga": 28,
        "Paris": 23, "Lyon": 25, "Bordeaux": 25, "Toulouse": 26, "Nice": 24, "Lille": 21,
        "Berlin": 22, "Munich": 21, "Hamburg": 20, "Cologne": 22, "Frankfurt": 23,
        "Rome": 28, "Milan": 26, "Naples": 28, "Turin": 25, "Bologna": 27, "Florence": 29,
        "Vienna": 24, "Graz": 23, "Innsbruck": 22,
        "Prague": 22, "Brno": 22, "Ostrava": 21,
        "Budapest": 25, "Debrecen": 24,
        "Warsaw": 22, "Krakow": 23, "Lodz": 22, "Wroclaw": 22, "Gdansk": 19,
        "Amsterdam": 19, "Rotterdam": 19, "Utrecht": 20, "Groningen": 18, "Eindhoven": 20,
        "Brussels": 20, "Antwerp": 20, "Ghent": 20, "Leuven": 20,
        "Stockholm": 19, "Gothenburg": 18, "Malmo": 18, "Uppsala": 18,
        "Oslo": 19, "Bergen": 16, "Trondheim": 15,
        "Helsinki": 18, "Turku": 17, "Tampere": 18,
        "Copenhagen": 19, "Aarhus": 18,
        "Dublin": 17, "Cork": 16, "Galway": 16,
        "London": 20, "Edinburgh": 17, "Manchester": 18,
        "Athens": 30, "Thessaloniki": 28, "Heraklion": 27,
        "Istanbul": 27, "Ankara": 26, "Izmir": 30,
        "Zurich": 22, "Geneva": 23, "Basel": 23,
        "Reykjavik": 12,
        "Valletta": 27,
        "Dewathang": 24, # Bhutan
        "Unknown": 22
    }
    
    # Tech keywords for academic score
    tech_keywords = ["Technology", "Politechnica", "Polytechnique", "Technical", "Technological", "Sciences"]

    ranked_list = []

    for uni in universities:
        city = uni.get("city", "Unknown")
        name = uni.get("name", "Unknown")
        image = uni.get("image", None)
        
        if not image:
            fallback_images = ["uni_classic_1770075331731.png", "uni_modern_1770075345966.png", "uni_campus_1770075359522.png", "uni_library_1770075372721.png"]
            image = random.choice(fallback_images)
            
        country = uni.get("country", "Unknown")
        url = uni.get("url", "#")
        # places = uni.get("places", "Unknown") # Places is now per field, removed from top level
        fields = uni.get("fields", [])

        # Base scores (0-10)
        
        # Location Score
        if city in top_cities:
            loc_score = random.uniform(9.0, 10.0)
        elif city in medium_cities:
            loc_score = random.uniform(7.5, 9.0)
        else:
            loc_score = random.uniform(5.0, 7.5) 
            
        # Grant Calculation (Erasmus+ 2024/25 for Poland - Long Term Study)
        # Group 1 (Higher living costs): ~550 EUR
        group_1_countries = [
            "Denmark", "Finland", "Ireland", "Iceland", "Liechtenstein", "Luxembourg", 
            "Norway", "Sweden", "Austria", "Belgium", "Cyprus", "France", "Greece", 
            "Spain", "Netherlands", "Malta", "Germany", "Portugal", "Italy"
        ]
        
        # Group 2 (Lower living costs): ~450 EUR
        if country in group_1_countries:
            grant_amount = 550
        else:
            grant_amount = 450 # Default to Group 2 for others
            
            # Special check for Bhutan/Distant countries (Partner Countries usually have different rates, often 700eur + travel)
            # But stick to requester's simplifed model unless asked.
            
        # Coordinates & Distance
        coords = city_coords.get(city, city_coords["Unknown"])
        
        # Calculate distance from TUL
        dist_from_tul = haversine(TUL_COORDS[0], TUL_COORDS[1], coords[0], coords[1])

        # Academic Reputation
        field_names = [f["name"] for f in fields]
        if any(keyword in name for keyword in tech_keywords) or any(any(k in fname for k in tech_keywords) for fname in field_names):
            acad_score = random.uniform(8.0, 9.5) 
        else:
            acad_score = random.uniform(6.0, 9.0)
            
        # Global Ranking Heuristic (Approximate)
        # Top known universities get better ranks
        top_unis_keywords = ["Politecnico Do Porto", "Sorbonne", "Munich", "Berlin", "Vienna", "Lisbon", "Barcelona", "KTH", "Delft", "Zurich", "Milano", "Sapienza", "Bologna", "Leuven", "Ghent", "Aalto"]
        
        if any(k in name for k in top_unis_keywords):
             global_rank = random.randint(50, 250)
        else:
             # Estimate based on academic score (higher score = better rank)
             # Map 6.0-9.5 to 1000-300 range approx
             base_rank = 1200 - int((acad_score - 6.0) * 250)
             global_rank = max(300, base_rank + random.randint(-50, 50))

        # Student Life / Vibe
        if country in ["Spain", "Portugal", "Italy", "Greece"]:
            vibe_score = random.uniform(8.5, 10.0) # South has better parties/weather
        elif country in ["France", "Germany", "Netherlands", "Belgium"]:
            vibe_score = random.uniform(7.0, 9.0)
        else:
            vibe_score = random.uniform(6.0, 8.5)

        # Cost (Affordability) - Higher score = Cheaper/Better value
        if country in ["Poland", "Hungary", "Czechia", "Romania", "Bulgaria", "Turkey", "Portugal", "Bhutan"]:
             cost_score = random.uniform(8.0, 10.0)
        elif country in ["Spain", "Italy", "Greece"]:
             cost_score = random.uniform(6.0, 8.0)
        elif country in ["Germany", "France", "Austria", "Belgium"]:
             cost_score = random.uniform(4.0, 6.0)
        elif country in ["Norway", "Sweden", "Finland", "Denmark", "Ireland", "Netherlands", "Switzerland"]:
             cost_score = random.uniform(2.0, 4.0)
        else:
             cost_score = random.uniform(5.0, 7.0)

        # Weighted Total (out of 10)
        # Weights: Vibe 40%, Academic 30%, Cost 20%, Location 10% (as per plan)
        total_score = (vibe_score * 0.4) + (acad_score * 0.3) + (cost_score * 0.2) + (loc_score * 0.1)
        
        uni_data = {
            "name": name,
            "city": city,
            "country": country,
            "url": url,
            "image": image,
            # "places": places, # Removed top level
            "fields": fields,
            "grant": grant_amount,
            "coords": coords,
            "distance_tul": dist_from_tul,
            "global_rank": global_rank,
            "weather_june": city_weather_june.get(city, city_weather_june.get("Unknown", 22)),
            "scores": {
                "total": round(total_score, 1),
                "academic": round(acad_score, 1),
                "vibe": round(vibe_score, 1),
                "cost": round(cost_score, 1),
                "location": round(loc_score, 1)
            },
            "tags": []
        }
        
        # Add tags
        if acad_score > 9.0: uni_data["tags"].append("Top Tier Education")
        if vibe_score > 9.0: uni_data["tags"].append("Party Central")
        if cost_score > 9.0: uni_data["tags"].append("Wallet Friendly")
        if loc_score > 9.0: uni_data["tags"].append("Iconic City")
        
        ranked_list.append(uni_data)

    # Sort by total score descending
    ranked_list.sort(key=lambda x: x["scores"]["total"], reverse=True)
    
    # Assign Position
    for i, uni in enumerate(ranked_list):
        uni["rank"] = i + 1

    # Write JS file
    js_content = f"const universities = {json.dumps(ranked_list, indent=2)};"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(js_content)

rank_universities('universities.json', 'universities.js')
