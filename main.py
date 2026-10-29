from pathlib import Path
import pandas as pd
import requests

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
POPULATION_FILE = DATA / "population.csv"
OUTPUT_FILE = DATA / "weather_demographics.csv"

POPULATION_URL = (
    "https://raw.githubusercontent.com/datasets/population/main/data/population.csv"
)

CAPITALS = [
    ("Kabul", "Afghanistan", 34.5553, 69.2075),
    ("Tirana", "Albania", 41.3275, 19.8187),
    ("Algiers", "Algeria", 36.7538, 3.0588),
    ("Andorra la Vella", "Andorra", 42.5063, 1.5218),
    ("Luanda", "Angola", -8.8390, 13.2894),
    ("Buenos Aires", "Argentina", -34.6037, -58.3816),
    ("Yerevan", "Armenia", 40.1792, 44.4991),
    ("Canberra", "Australia", -35.2809, 149.1300),
    ("Vienna", "Austria", 48.2082, 16.3738),
    ("Baku", "Azerbaijan", 40.4093, 49.8671),
    ("Nassau", "Bahamas", 25.0443, -77.3504),
    ("Manama", "Bahrain", 26.2285, 50.5860),
    ("Dhaka", "Bangladesh", 23.8103, 90.4125),
    ("Bridgetown", "Barbados", 13.0975, -59.6167),
    ("Minsk", "Belarus", 53.9006, 27.5590),
    ("Brussels", "Belgium", 50.8503, 4.3517),
    ("Belmopan", "Belize", 17.2510, -88.7590),
    ("Porto-Novo", "Benin", 6.4969, 2.6289),
    ("Thimphu", "Bhutan", 27.4728, 89.6390),
    ("La Paz", "Bolivia", -16.4897, -68.1193),
    ("Sarajevo", "Bosnia and Herzegovina", 43.8563, 18.4131),
    ("Gaborone", "Botswana", -24.6282, 25.9231),
    ("Brasilia", "Brazil", -15.7939, -47.8828),
    ("Bandar Seri Begawan", "Brunei", 4.9031, 114.9398),
    ("Sofia", "Bulgaria", 42.6977, 23.3219),
    ("Ouagadougou", "Burkina Faso", 12.3714, -1.5197),
    ("Gitega", "Burundi", -3.4264, 29.9308),
    ("Phnom Penh", "Cambodia", 11.5564, 104.9282),
    ("Yaounde", "Cameroon", 3.8480, 11.5021),
    ("Ottawa", "Canada", 45.4215, -75.6972),
    ("Praia", "Cape Verde", 14.9331, -23.5133),
    ("Bangui", "Central African Republic", 4.3947, 18.5582),
    ("N'Djamena", "Chad", 12.1348, 15.0557),
    ("Santiago", "Chile", -33.4489, -70.6693),
    ("Beijing", "China", 39.9042, 116.4074),
    ("Bogota", "Colombia", 4.7110, -74.0721),
    ("Moroni", "Comoros", -11.7172, 43.2473),
    ("Brazzaville", "Congo", -4.2634, 15.2429),
    ("San Jose", "Costa Rica", 9.9281, -84.0907),
    ("Yamoussoukro", "Cote d'Ivoire", 6.8276, -5.2893),
    ("Zagreb", "Croatia", 45.8150, 15.9819),
    ("Havana", "Cuba", 23.1136, -82.3666),
    ("Nicosia", "Cyprus", 35.1856, 33.3823),
    ("Prague", "Czechia", 50.0755, 14.4378),
    ("Copenhagen", "Denmark", 55.6761, 12.5683),
    ("Djibouti", "Djibouti", 11.5721, 43.1456),
    ("Roseau", "Dominica", 15.3010, -61.3881),
    ("Santo Domingo", "Dominican Republic", 18.4861, -69.9312),
    ("Quito", "Ecuador", -0.1807, -78.4678),
    ("Cairo", "Egypt", 30.0444, 31.2357),
    ("San Salvador", "El Salvador", 13.6929, -89.2182),
    ("Malabo", "Equatorial Guinea", 3.7504, 8.7371),
    ("Asmara", "Eritrea", 15.3229, 38.9251),
    ("Tallinn", "Estonia", 59.4370, 24.7536),
    ("Mbabane", "Eswatini", -26.3054, 31.1367),
    ("Addis Ababa", "Ethiopia", 8.9806, 38.7578),
    ("Suva", "Fiji", -18.1248, 178.4501),
    ("Helsinki", "Finland", 60.1699, 24.9384),
    ("Paris", "France", 48.8566, 2.3522),
    ("Libreville", "Gabon", 0.4162, 9.4673),
    ("Banjul", "Gambia", 13.4549, -16.5790),
    ("Tbilisi", "Georgia", 41.7151, 44.8271),
    ("Berlin", "Germany", 52.5200, 13.4050),
    ("Accra", "Ghana", 5.6037, -0.1870),
    ("Athens", "Greece", 37.9838, 23.7275),
    ("Guatemala City", "Guatemala", 14.6349, -90.5069),
    ("Conakry", "Guinea", 9.6412, -13.5784),
    ("Bissau", "Guinea-Bissau", 11.8817, -15.6170),
    ("Georgetown", "Guyana", 6.8013, -58.1551),
    ("Port-au-Prince", "Haiti", 18.5944, -72.3074),
    ("Tegucigalpa", "Honduras", 14.0723, -87.1921),
    ("Budapest", "Hungary", 47.4979, 19.0402),
    ("Reykjavik", "Iceland", 64.1466, -21.9426),
    ("New Delhi", "India", 28.6139, 77.2090),
    ("Jakarta", "Indonesia", -6.2088, 106.8456),
    ("Tehran", "Iran", 35.6892, 51.3890),
    ("Baghdad", "Iraq", 33.3152, 44.3661),
    ("Dublin", "Ireland", 53.3498, -6.2603),
    ("Jerusalem", "Israel", 31.7683, 35.2137),
    ("Rome", "Italy", 41.9028, 12.4964),
    ("Kingston", "Jamaica", 17.9712, -76.7936),
    ("Tokyo", "Japan", 35.6762, 139.6503),
    ("Amman", "Jordan", 31.9454, 35.9284),
    ("Astana", "Kazakhstan", 51.1694, 71.4491),
    ("Nairobi", "Kenya", -1.2921, 36.8219),
    ("South Tarawa", "Kiribati", 1.4518, 172.9717),
    ("Pristina", "Kosovo", 42.6629, 21.1655),
    ("Kuwait City", "Kuwait", 29.3759, 47.9774),
    ("Bishkek", "Kyrgyzstan", 42.8746, 74.5698),
    ("Vientiane", "Laos", 17.9757, 102.6331),
    ("Riga", "Latvia", 56.9496, 24.1052),
    ("Beirut", "Lebanon", 33.8938, 35.5018),
    ("Maseru", "Lesotho", -29.3151, 27.4869),
    ("Monrovia", "Liberia", 6.2907, -10.7605),
    ("Tripoli", "Libya", 32.8872, 13.1913),
    ("Vaduz", "Liechtenstein", 47.1410, 9.5209),
    ("Vilnius", "Lithuania", 54.6872, 25.2797),
    ("Luxembourg", "Luxembourg", 49.6116, 6.1319),
    ("Antananarivo", "Madagascar", -18.8792, 47.5079),
    ("Lilongwe", "Malawi", -13.9626, 33.7741),
    ("Kuala Lumpur", "Malaysia", 3.1390, 101.6869),
    ("Male", "Maldives", 4.1755, 73.5093),
    ("Bamako", "Mali", 12.6392, -8.0029),
    ("Valletta", "Malta", 35.8992, 14.5141),
    ("Majuro", "Marshall Islands", 7.0897, 171.3803),
    ("Nouakchott", "Mauritania", 18.0735, -15.9582),
    ("Port Louis", "Mauritius", -20.1609, 57.5012),
    ("Mexico City", "Mexico", 19.4326, -99.1332),
    ("Palikir", "Micronesia", 6.9147, 158.1610),
    ("Chisinau", "Moldova", 47.0105, 28.8638),
    ("Monaco", "Monaco", 43.7384, 7.4246),
    ("Ulaanbaatar", "Mongolia", 47.8864, 106.9057),
    ("Podgorica", "Montenegro", 42.4304, 19.2594),
    ("Rabat", "Morocco", 34.0209, -6.8416),
    ("Maputo", "Mozambique", -25.9692, 32.5732),
    ("Naypyidaw", "Myanmar", 19.7633, 96.0785),
    ("Windhoek", "Namibia", -22.5609, 17.0658),
    ("Yaren", "Nauru", -0.5477, 166.9209),
    ("Kathmandu", "Nepal", 27.7172, 85.3240),
    ("Amsterdam", "Netherlands", 52.3676, 4.9041),
    ("Wellington", "New Zealand", -41.2866, 174.7756),
    ("Managua", "Nicaragua", 12.1150, -86.2362),
    ("Niamey", "Niger", 13.5116, 2.1254),
    ("Abuja", "Nigeria", 9.0765, 7.3986),
    ("Oslo", "Norway", 59.9139, 10.7522),
]

ALIASES = {
    "Egypt, Arab Rep.": "Egypt",
    "Iran, Islamic Rep.": "Iran",
    "Czech Republic": "Czechia",
    "Cote d'Ivoire": "Cote d'Ivoire",
    "Côte d'Ivoire": "Cote d'Ivoire",
    "Congo, Rep.": "Congo",
    "Republic of the Congo": "Congo",
    "United States": "United States",
    "United States of America": "United States",

    # Country names used in the population dataset
    "Bahamas": "Bahamas, The",
    "Brunei": "Brunei Darussalam",
    "Cape Verde": "Cabo Verde",
    "Gambia": "Gambia, The",
    "Kyrgyzstan": "Kyrgyz Republic",
    "Laos": "Lao PDR",
    "Micronesia": "Micronesia, Fed. Sts.",
}


def load_population():
    DATA.mkdir(parents=True, exist_ok=True)

    if not POPULATION_FILE.exists():
        print("Downloading population dataset...")
        response = requests.get(POPULATION_URL, timeout=30)
        response.raise_for_status()
        POPULATION_FILE.write_bytes(response.content)

    df = pd.read_csv(POPULATION_FILE)

    country_col = next(
        (c for c in ["Country Name", "Country", "country", "Entity"] if c in df.columns),
        None,
    )
    population_col = next(
        (c for c in ["Value", "Population", "population", "Population (historical)"]
         if c in df.columns),
        None,
    )
    year_col = next((c for c in ["Year", "year", "Time"] if c in df.columns), None)

    if not country_col or not population_col:
        raise ValueError(f"Could not identify country/population columns: {list(df.columns)}")

    keep_cols = [country_col, population_col]
    if year_col:
        keep_cols.append(year_col)

    df = df[keep_cols].copy()
    rename = {country_col: "Country", population_col: "Population"}
    if year_col:
        rename[year_col] = "Population_Year"
    df.rename(columns=rename, inplace=True)

    df["Country"] = df["Country"].astype(str).str.strip().replace(ALIASES)
    df["Population"] = pd.to_numeric(df["Population"], errors="coerce")

    if "Population_Year" in df.columns:
        df["Population_Year"] = pd.to_numeric(df["Population_Year"], errors="coerce")
        df.sort_values("Population_Year", inplace=True)

    df = df.dropna(subset=["Population"])
    df = df.drop_duplicates(subset=["Country"], keep="last")
    return df[["Country", "Population"] + (
        ["Population_Year"] if "Population_Year" in df.columns else []
    )]



def fetch_weather():
    import time
    import requests

    records = []
    url = "https://api.open-meteo.com/v1/forecast"

    with requests.Session() as session:
        for city, country, latitude, longitude in CAPITALS:
            print(f"Fetching weather: {city}, {country}", flush=True)

            params = {
                "latitude": latitude,
                "longitude": longitude,
                "current": "temperature_2m,wind_speed_10m",
                "timezone": "UTC",
            }

            for attempt in range(1, 4):
                try:
                    response = session.get(
                        url,
                        params=params,
                        timeout=(10, 60),
                    )
                    response.raise_for_status()
                    current = response.json()["current"]

                    records.append({
                        "City": city,
                        "Country": country,
                        "Latitude": latitude,
                        "Longitude": longitude,
                        "Temperature_C": current["temperature_2m"],
                        "Wind_Speed_kmh": current["wind_speed_10m"],
                        "Weather_Time_UTC": current["time"],
                    })
                    break

                except (requests.RequestException, ValueError, KeyError) as exc:
                    print(
                        f"Attempt {attempt}/3 failed for {city}: {exc}",
                        flush=True,
                    )
                    if attempt < 3:
                        time.sleep(2 * attempt)
                    else:
                        print(f"Skipping {city} after 3 failed attempts.")

            time.sleep(0.2)

    if not records:
        raise RuntimeError(
            "No weather data was retrieved. Check your internet connection "
            "and try again."
        )

    return pd.DataFrame(records)



def main():
    weather = fetch_weather()
    population = load_population()

    # Match country names consistently before merging.
    weather["Country"] = weather["Country"].astype(str).str.strip().replace(ALIASES)
    result = weather.merge(population, on="Country", how="left")

    if "Population_Year" not in result.columns:
        result["Population_Year"] = pd.NA

    result["Population"] = pd.to_numeric(result["Population"], errors="coerce").round().astype("Int64")
    result["Population_Year"] = pd.to_numeric(result["Population_Year"], errors="coerce").astype("Int64")
    result["Temperature_F"] = (result["Temperature_C"] * 9 / 5 + 32).round(2)
    result["Temperature_Category"] = pd.cut(
        result["Temperature_C"],
        bins=[-float("inf"), 10, 25, float("inf")],
        labels=["Cold", "Mild", "Hot"],
        right=False,
    ).astype(str)

    missing = result.loc[result["Population"].isna(), ["City", "Country"]]
    if not missing.empty:
        print("\nCountries with unmatched population data:")
        print(missing.to_string(index=False))

    DATA.mkdir(parents=True, exist_ok=True)
    result.to_csv(OUTPUT_FILE, index=False)

    print(f"\nSaved {len(result)} rows to: {OUTPUT_FILE}")
    print(f"Unique cities: {result['City'].nunique()}")
    print(f"Missing populations: {result['Population'].isna().sum()}")
    print("\nSample data:")
    print(result.head(10).to_string(index=False))


if __name__ == "__main__":
    main()    
