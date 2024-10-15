# HuggingFace Dataset Scraper

This is a Python project that scrapes dataset details from the [HuggingFace](https://huggingface.co/) website, specifically for datasets listed under `huggingface.co/datasets`. The script collects information such as descriptions, size, modalities, formats, tags, and libraries of various datasets.

## Features
- Extract dataset descriptions, size, and various categories from HuggingFace dataset pages.
- Processes multiple dataset links from a specified folder.
- Saves both raw and cleaned dataset information in JSON format.
- User-friendly console progress updates for each step.

## Prerequisites
- Python 3.x
- Required packages listed in `requirements.txt` (install them with `pip install -r requirements.txt`)

## Usage

### Folder Structure
Ensure you have the following folder structure before running the scraper:

```
.
|-- links/
|   |-- example.txt  # Example file containing dataset links (you can create more link files here)
|-- data/            # Folder where raw and cleaned JSON output will be saved
|-- huggingface_scraper.py  # Main Python script
```

### Step-by-Step Guide

1. **Add Dataset Links**:
   - Create a file in the `links` folder named, for example, `datasets_links.txt`.
   - Add URLs of HuggingFace datasets, one per line. You can use the following format as an example:

```
https://huggingface.co/datasets/fka/awesome-chatgpt-prompts
https://huggingface.co/datasets/HuggingFaceFW/fineweb
```

  You can also check the [`links/example.txt`](links/example.txt) file for more examples.

2. **Run the Scraper**:
   - Use the command:
   ```
   python huggingface_scraper.py
   ```
   This will scrape all datasets listed in your link files and save the results in the `data` folder.

3. **Output Files**:
   - `datasets_info_raw.json`: Raw dataset information with all extracted content.
   - `datasets_info_clean.json`: Cleaned dataset information, with whitespace and unnecessary characters removed.

### Example Output
You can find an example of an output JSON file (`example_output.json`) in the repository under [`data/example_output.json`](data/example_output.json).

## Notes
- This scraper only works for dataset pages on HuggingFace (`huggingface.co/datasets`).
- Make sure to use only valid HuggingFace dataset links to avoid any issues while fetching data.
- You can add as many link files in the `links` folder as needed, and the script will process them all.

## Disclaimer
Use this tool responsibly, respecting the HuggingFace website's terms of service. This script is designed for educational purposes. And was randomly done in a few hours under well known illness named "boredom and irresponsibility". Will work in 1 out of 100 cases, if you are lucky. Good luck, human!

