from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import csv
import requests
from datetime import datetime

url = "https://api.co2signal.com/v1/latest"
orange_countries = ["Botswana", "Burkina Faso", "Cameroon", "Egypt", "Guinea Bissau", "Guinea Conakry", "Ivory Coast",
                    "Jordan", "Liberia", "Mali", "Morocco", "Centrafrican Republic", "Democratic Republic of Congo",
                    "Senegal", "Sierra Leone", "Tunisia", "Madagascar", "Mauritius", "Belgium", "France", "Luxembourg",
                    "Moldova", "Poland", "Romania", "Slovakia", "Spain"]
orange_country_codes_fixed = ["BW", "BF", "CM", "EG", "GW", "GN", "CI", "JO", "LR", "ML", "MA", "CF", "CD", "SN", "SL",
                              "TN", "MG", "MU"]
orange_country_codes_dynamic = ["BE", "FR", "LU", "MD", "PL", "RO", "SK", "ES"]
carbon_intensity_fixed = [794.5205, 611.4286, 278.26086, 469.63, 750, 208.63307, 410.74686, 391.12537, 304.34784,
                          463.12686, 630.7506, 0, 25.36232, 523.1317, 47.61905, 469.428, 483.25363, 611.1111]
carbon_intensity_dynamic = [0, 0, 0, 0, 0, 0, 0, 0]
carbon_intensity_fixed_dict = dict(zip(orange_country_codes_fixed, carbon_intensity_fixed))
carbon_intensity_dynamic_dict = dict(zip(orange_country_codes_dynamic, carbon_intensity_dynamic))

app = FastAPI()

'''the browser will send these params to the API'''


class Client_request(BaseModel):
    country_code: str
    life_cycle_step: str


@app.post("/carbonfootprint")
async def get_all_data(client_request: Client_request):
    # Read CSV file, get all the data
    keys = []
    values = []
    usage = []
    filename = client_request.life_cycle_step + "_data.csv"
    with open(filename, encoding='utf-8', newline='') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            if len(row) >= 3:
                keys.append(row[0])
                values.append(row[1])
                usage.append(row[2])
            else:
                print(f"Row does not have enough columns: {row}")

    # Print keys and values to debug
    print(f"Keys: {keys}")
    print(f"Values: {values}")

    # Delete all the empty elements in usage list
    avg_usage = [val for val in usage if val]

    # Check if avg_usage has enough elements
    if len(avg_usage) < 4:
        raise HTTPException(status_code=500, detail="CSV file does not contain enough data")

    # Check if the required keys exist in the filedata dictionary
    filedata = dict(zip(keys, values))
    required_keys = ["After conversion kWh", "Operating System Name", "CPU Model", "GPU Model", "duration"]
    missing_keys = [key for key in required_keys if key not in filedata]
    if missing_keys:
        raise HTTPException(status_code=500, detail=f"Missing keys in CSV file: {', '.join(missing_keys)}")

    power_consumption = float(filedata["After conversion kWh"])
    os_info = filedata["Operating System Name"]
    CPU_info = filedata["CPU Model"]
    GPU_info = filedata["GPU Model"]
    run_time = float(filedata["duration"])
    CPU_avg_usage = avg_usage[1]
    RAM_avg_usage = avg_usage[2]
    GPU_avg_usage = avg_usage[3]

    # Based on the country codes, get the relevant carbon intensity
    if client_request.country_code in orange_country_codes_fixed:
        carbon_intensity = carbon_intensity_fixed_dict[client_request.country_code]
        data_time = datetime.now()
    elif client_request.country_code in orange_country_codes_dynamic:
        r = requests.get(url, params={"countryCode": client_request.country_code})
        carbon_intensity = r.json()["data"]["carbonIntensity"]
        data_time = r.json()["data"]["datetime"]
        # Update the dynamic dictionary
        carbon_intensity_dynamic_dict.update({client_request.country_code: carbon_intensity})
    else:
        raise HTTPException(status_code=404, detail="The country code is not an Orange country")

    # Compute the final carbon emission in unit g and km driven by a car and trees seeding per month
    carbon_emission = power_consumption * carbon_intensity
    km_driven_by_a_car = carbon_emission / 217.6
    trees_seeding_per_month = carbon_emission / 504.5

    # Return all the data
    return {
        "energy consumption (Wh)": power_consumption * 1000,
        "carbon emission (gCO2e)": carbon_emission,
        "km driven by a car (Km)": km_driven_by_a_car,
        "trees seeding per month": trees_seeding_per_month,
        "os": os_info,
        "CPU": CPU_info,
        "GPU": GPU_info,
        "CPU average usage (%)": CPU_avg_usage,
        "RAM average usage (%)": RAM_avg_usage,
        "GPU average usage (%)": GPU_avg_usage,
        "runtime (s)": run_time,
        "data&time": data_time
    }
