import os
import requests
from bs4 import BeautifulSoup
import re

# Function to clean up text
def clean_text(text):
    text = re.sub(r'\n+', '\n', text)  # Replace multiple line breaks with one
    text = re.sub(r' +', ' ', text)    # Replace consecutive spaces with one
    return text

# Create a directory for saving the files
if not os.path.exists("WebData"):
    os.mkdir("WebData")

# Read URLs from a text file
with open('urls.txt', 'r') as file:
    urls = file.read().splitlines()

# Iterate through the list of URLs
for url in urls:
    # Send an HTTP GET request to the URL
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the webpage
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the div element with the class 'itemFullText'
        item_full_text_div = soup.find('div', class_='itemFullText')

        if item_full_text_div:
            # Extract the text from the div element
            text = item_full_text_div.get_text()
            text = clean_text(text)

            # Get the page name from the URL
            page_name = url.split('/')[-1].replace('.html', '').replace('/', '_')

            # Save the result to a text file in the "WebData" directory
            file_path = os.path.join("WebData", f"{page_name}.txt")
            with open(file_path, 'w', encoding='utf-8') as output_file:
                output_file.write(text)
                print(f"Saved result from {url} to {file_path}")
        else:
            print(f"itemFullText div not found on {url}.")
    else:
        print(f"Failed to retrieve the webpage (Status code: {response.status_code}) for {url}")
