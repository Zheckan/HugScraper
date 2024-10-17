import requests
from bs4 import BeautifulSoup
import json
import os
import re
import time


# Read links from a file
def read_links_from_file(file_path):
    print(f"Reading links from {file_path}...")
    with open(file_path, "r", encoding="utf-8") as file:
        links = [line.strip() for line in file.readlines() if line.strip()]
    print(f"Found {len(links)} links in {file_path}.")
    return links


# Function to extract dataset details
def extract_dataset_details(url, current_index, total_urls):
    try:
        print(f"{current_index} out of {total_urls}")
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract dataset description
        description_tag = soup.find("div", {"class": "2xl:pr-6"})
        description = (
            description_tag.text.strip()
            if description_tag
            else "No description available"
        )

        # Extract size of the downloaded dataset files
        size_label_tag = soup.find(
            "div",
            {"class": "truncate text-xs text-gray-400"},
            string=lambda text: text and "Size of downloaded dataset files" in text,
        )
        size_tag = (
            size_label_tag.find_next("div", {"class": "truncate text-sm"})
            if size_label_tag
            else None
        )
        size = size_tag.text.strip() if size_tag else "Size not available"

        # Extract categories like modalities, formats, tags, libraries, etc.
        categories = ["Modalities:", "Formats:", "Tags:", "Libraries:"]
        extracted_categories = {}
        for category in categories:
            category_tag = soup.find(
                "span",
                {
                    "class": "mb-1 mr-1 p-1 text-sm leading-tight text-gray-400 md:mb-1.5"
                },
                string=lambda text: text and f"{category}" in text,
            )
            category_values = []
            if (category_tag):
                parent_div = category_tag.find_parent(
                    "div", {"class": "mr-1 flex flex-wrap items-center"}
                )
                value_tags = (
                    parent_div.find_all(
                        "a", {"class": "mb-1 mr-1 md:mb-1.5 md:mr-1.5 rounded-lg"}
                    )
                    if parent_div
                    else []
                )
                category_values = [value_tag.text.strip() for value_tag in value_tags]
            extracted_categories[
                category.lower().replace(":", "").replace(" ", "_")
            ] = category_values

        return {
            "id": current_index,
            "link": url,
            "size_of_downloaded_dataset_files": size,
            "description": description,
            "modalities": extracted_categories.get("modalities", []),
            "formats": extracted_categories.get("formats", []),
            "tags": extracted_categories.get("tags", []),
            "libraries": extracted_categories.get("libraries", []),
        }
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return {
            "id": current_index,
            "link": url,
            "size_of_downloaded_dataset_files": "Error fetching size",
            "description": "Error fetching description",
            "modalities": [],
            "formats": [],
            "tags": [],
            "libraries": [],
        }


# Clean the data by removing excessive whitespace, newlines, and non-text characters
def clean_text(text):
    return re.sub(r"\s+", " ", text).strip()


# Process each file in the links folder
links_folder = "links"
output_folder_raw = "data/raw"
output_folder_clean = "data/clean"
os.makedirs(output_folder_raw, exist_ok=True)
os.makedirs(output_folder_clean, exist_ok=True)

for file_name in os.listdir(links_folder):
    file_path = os.path.join(links_folder, file_name)
    urls = read_links_from_file(file_path)

    # Extract details for each URL and save to JSON
    print(f"Starting extraction of dataset details for {file_name}...")
    data_list = [extract_dataset_details(url, idx + 1, len(urls)) for idx, url in enumerate(urls)]

    # Save the raw data
    output_file_raw = os.path.join(output_folder_raw, f"{os.path.splitext(file_name)[0]}_raw.json")
    print(f"Saving raw data to {output_file_raw}...")
    with open(output_file_raw, mode="w", encoding="utf-8") as file:
        json.dump(data_list, file, indent=4, ensure_ascii=False)
    print(f"Raw data saved to {output_file_raw}")

    # Clean the data
    print(f"Cleaning extracted data for {file_name}...")
    data_list_cleaned = []
    for idx, data in enumerate(data_list, start=1):
        print(f"{idx} out of {len(data_list)}")
        cleaned_data = {
            "id": idx,
            "link": data["link"],
            "size_of_downloaded_dataset_files": clean_text(data["size_of_downloaded_dataset_files"]),
            "description": clean_text(data["description"]),
            "modalities": [clean_text(modality) for modality in data["modalities"]],
            "formats": [clean_text(fmt) for fmt in data["formats"]],
            "tags": [clean_text(tag) for tag in data["tags"]],
            "libraries": [clean_text(library) for library in data["libraries"]],
        }
        data_list_cleaned.append(cleaned_data)

    # Save the cleaned data
    output_file_clean = os.path.join(output_folder_clean, f"{os.path.splitext(file_name)[0]}_clean.json")
    print(f"Saving cleaned data to {output_file_clean}...")
    with open(output_file_clean, mode="w", encoding="utf-8") as file:
        json.dump(data_list_cleaned, file, indent=4, ensure_ascii=False)
    print(f"Cleaned data saved to {output_file_clean}")
