import base64
import requests
import os
import dotenv
# Set up API key
import pandas as pd
dotenv.load_dotenv()
from pathlib import Path
import os

os.environ["OPENAI_API_KEY"] = os.getenv("unifi_esg_extraction_key")

api_key = os.environ["OPENAI_API_KEY"]

# Load the data
pages = pd.read_excel("data/companies/Electrolux/extract_pages.xlsx")

# Convert 'year' to int
pages["year"] = pages["year"].astype(int)

# Filter rows where 'p_and_l' is not NaN and then convert 'p_and_l' to int
pages = pages[pages["p_and_l"].notna()]
pages["p_and_l"] = pages["p_and_l"].astype(int)

# Create the 'path' column
pages["path"] = pages.apply(lambda row: f"data/companies/Electrolux/{row['year']}/single_pages/Electrolux_{row['year']}_page_{row['p_and_l']}.jpeg", axis=1)



schema = [
        {
            "key": "year",
            "description": "The year for which the financial statement is being reported."
        },
        {
            "key": "taxes",
            "description": "Total taxes paid by the company, also called 'skatt' in Swedish"
        },
        {
            "key": "net_profit",
            "description": "Net profit earned by the company for the year, also called 'Nettovinst för året' in Swedish"
        }
]

# Function to encode the image to base64
def encode_image(image_path):
        with open(image_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode('utf-8')



# create a function that loops through the pages and makes the API call, passing the year and the path to the image
# add in a limit to the number of pages to loop through set by the user and a start page
def loop_through_pages(limit, start_page):
    start_page = start_page
    limit = start_page + limit
    for index, row in pages[start_page:limit].iterrows():
        print(f"Page {index}")
        prompt = f"Role: You're an expert at extracting data from tables and text of corporate reports. You are being given an excerpt from a report on the activity of Electrolux for year {row['year']}, containing the profit and loss statement, as well as a schema to structure your response. Task: You are asked to extract the values of the profit and loss statement. Use your intuition to return an answer even when you cannot get the exact thing that we are looking for. Answer only in RFC compliant JSON. \n\nHere is the schema {schema} \n\nHere is the image: \n\n" 
        image_path = row["path"]
        print(image_path)
        base64_image = encode_image(image_path)
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }

        payload = {
            "model": "gpt-4-vision-preview",
            "messages": [
            {
                "role": "user",
                "content": [
                {"type": "text", "text": prompt},
                {
                    "type": "image_url",
                    "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image}"
                    }
                }
                ]
            }
            ],
            "max_tokens": 1000
        }

        output_path = f"data/companies/Electrolux/extracted_data_2/{row['year']}_page_{row['p_and_l']}.txt"
        Path(f"data/companies/Electrolux/extracted_data_2").mkdir(parents=True, exist_ok=True)


        # Check if the output file already exists
        if os.path.exists(output_path):
            print("File already exists, skipping")
        else:
            # Make the API request and print out the response
            response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
            print(response.json())

            # Save the response to a text file in data/companies/Electrolux/extracted_data
            # Ensure that the folder exists
            with open(output_path, "w") as f:
                f.write(str(response.json()))

# loop through the pages
loop_through_pages(limit = 100, start_page=0)