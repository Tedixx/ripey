# Ripey

## Overview
Ripey is a Python script designed to search and retrieve information from the RIPE database. This tool leverages the Playwright library for web automation to fetch this data from the `apps.db.ripe.net` website, and provides options to extract specific data such as email addresses, subnets, or save the results to a CSV file.

## What is the RIPE database?
The RIPE Database, managed by the RIPE NCC, holds useful information about Internet resources, such as IP addresses and routing policies. It includes:

1.  **Internet Number Resources**: Details of who holds specific IP addresses and how they are allocated.
2.	**Routing Information**: Data on network routing policies to help operators configure their networks.
3.	**Contact Information**: Details of organizations and people responsible for managing these resources.

This database helps ensure the unique use of IP addresses, supports network coordination, and aids in resolving network issues. More information is available [here](https://apps.db.ripe.net/docs/What-is-the-RIPE-Database/Purpose-and-Content-of-the-RIPE-Database/#criteria-for-a-mirrored-database).

## Features
- **Subnet lookup**: Extracts, calculates and prints subnet ranges found in the RIPE records.
- **Email lookup**: Extracts and prints email addresses found in the RIPE records.
- **Database lookup**: Fetches and prints results from the RIPE database based on the input query.
- Saves results to a CSV file for further analysis.
- Uses asynchronous programming for efficient web scraping.
- Simple CLI for easy operation.

## Requirements
To run this script, you will need Python 3.7 or newer. The following Python packages are also required:

- `asyncio`
- `argparse`
- `re`
- `ipaddress`
- `playwright`
- `pandas`

These dependencies are listed in the requirements.txt file for easy installation.

## Installation

First, clone this repository or download the script to your local machine. Then, navigate to the script's directory in your terminal and run the following commands:

1. **Install dependencies:**
`pip install -r requirements.txt`

2. **Install Playwright browsers:**
`playwright install`


## Usage

To use Ripey, run the script from the command line with the appropriate arguments. Here are some example commands:

1. Extract and print subnet ranges:
`python3 ripey.py -subnet "your search query"`

2. Extract and print email addresses:
`python3 ripey.py -email "your search query"`

3. Search for a query and print results:
`python3 ripey.py "your search query"`

4. Save results to a CSV file:
`python3 ripey.py -csv -o outputfile.csv "your search query"`


**Too frequent usage of this tool may result in a temporary IP blacklist by RIPE**.​

## Output

The script will print results to the console based on the specified arguments. If the `-email` or `-subnet` options are used, it will print only the extracted email addresses or subnet ranges respectively. If the `-csv` option is used, it will save the results to the specified CSV file.

### Sample output subnet

```
python3 ripey.py -subnet hackerone

45.8.84.0/22
45.8.84.0/23
45.8.86.0/23
144.178.70.248/29
```
### Sample output email

```
python3 ripey.py -email hackerone

abuse@hackerone.com
hostmaster@hackerone.com
privacy-redacted@hackerone.com
```

## Note

This script is intended for educational and ethical use only. Ensure you have permission to scrape the website and are compliant with their terms of service and any legal requirements.

## Contributing

Contributions to the DMARC Domain Fetcher are welcome. Please open an issue or pull request to suggest improvements or add new features.

## License

This script is released under the MIT License. See the LICENSE file for details.
