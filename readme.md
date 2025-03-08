# EU CBDC Data Scraper

Welcome to the **CBDC Data Scraper**! This tool is designed to automate the collection of data related to Central Bank Digital Currencies (CBDCs) and the digital euro from reliable online sources. By leveraging advanced Google search operators, this scraper targets white papers, legal documents, academic publications, and technical reports from official websites, research institutes, and more.

## Purpose

The primary goal of this project is to gather high-quality, structured data on CBDCs and the digital euro for research, analysis, or development purposes. Whether you're studying the legal frameworks, technical designs, privacy challenges, or interoperability of digital currencies, this scraper simplifies the process of finding relevant documents and resources.

## Features

This scraper uses tailored Google search queries to:
* Find specific white papers and official documents in PDF format
* Limit searches to authoritative websites (e.g., central banks, EU institutions, academic platforms)
* Target legal frameworks, regulations, and compliance-related content
* Explore technical challenges and solutions, including blockchain and DLT integration
* Collect academic research from trusted repositories

## Search Operators and Use Cases

Below are the key search strategies implemented in the scraper:

### 1. Specific White Papers
* `"CBDC" OR "digital euro" filetype:pdf`
* `"digital euro white paper" site:.eu filetype:pdf`
* `"central bank digital currency" AND "legal framework" filetype:pdf`

### 2. Official Websites
* `site:ecb.europa.eu "digital euro"`
* `site:europa.eu "CBDC legal framework"`
* `site:ceps.eu "digital euro report"`

### 3. Legal Documents
* `"CBDC regulation" OR "digital euro law" filetype:pdf`
* `"MiCA regulation" AND "CBDC" site:.eu`
* `"CBDC compliance" AND "European Union"`

### 4. Specific Topics or Challenges
* `"privacy challenges" AND "CBDC"`
* `"AML compliance" AND "digital euro"`
* `"technical design" AND "central bank digital currency"`

### 5. Academic Publications
* `site:ssrn.com "CBDC artificial intelligence"`
* `site:mpra.ub.uni-muenchen.de "digital euro"`
* `"CBDC research paper" site:.edu`

### 6. Interoperability and Technology
* `"DLT interoperability" AND "CBDC"`
* `"blockchain infrastructure" AND "digital euro"`

## Installation

1. Clone the repository:
```bash
git clone https://github.com/gillesduif/EU-CBDC-Data-Scraper.git
```

2. Navigate to the project directory:
```bash
cd EU-CBDC-Data-Scraper
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Setup

Before using the scraper, you'll need to:

1. Get a Google API key:
   - Visit the [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project
   - Enable the "Custom Search API"
   - Generate an API key

2. Create a Custom Search Engine:
   - Go to [Google Programmable Search Engine](https://programmablesearch.google.com/create)
   - Set up a new search engine
   - Configure it to search the entire web
   - Note your Search Engine ID (cx)

## Usage

1. Open the script and replace the API keys:
```python
API_KEY = "YOUR_GOOGLE_API_KEY"
CSE_ID = "YOUR_CUSTOM_SEARCH_ENGINE_ID"
```

2. Run the scraper:
```bash
python cbdc_scraper.py
```

3. Check the `./cbdc_data` directory for:
   - Downloaded PDF documents organized by category
   - CSV and Excel files containing all search results and metadata
   - Analysis report with statistics on collected data

## Customization

You can customize the scraper by:
- Adding or modifying search queries in the `search_queries` dictionary
- Changing the output directory in the constructor
- Adjusting the `max_results_per_query` parameter to control the amount of data collected

## Requirements

* Python 3.7+
* Google API key
* Custom Search Engine ID
* Libraries:
  - google-api-python-client
  - pandas
  - beautifulsoup4
  - requests

## Contributing

Contributions are welcome! If you'd like to add new search operators, improve the scraper's efficiency, or fix bugs, please:

1. Fork the repository
2. Create a new branch (`git checkout -b feature-branch`)
3. Make your changes
4. Submit a pull request with your changes

## License

This project is licensed under the MIT License.

## Contact

For questions or suggestions, feel free to open an issue.
