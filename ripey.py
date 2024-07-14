## Ripey by @tedixh1

import asyncio
import argparse
import re
from ipaddress import ip_address, summarize_address_range
from playwright.async_api import async_playwright
import pandas as pd

async def fetch_all_results(inputvalue: str):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto('https://www.db.ripe.net/db-web-ui/fulltextsearch')

        # Enter the search term and submit the form
        await page.fill('#fullTextSearchInput', inputvalue)
        await page.click('#fullTextSearchButton')

        # Ensure the results are visible and stable
        await asyncio.sleep(0.2)  # Wait a few seconds to let the page fully load the results
        await page.wait_for_selector('.results', state='visible')

        results = []
        while True:
            # Ensure page content is stable
            await asyncio.sleep(0.2)  # Additional wait to stabilize page after loading new results
            current_results = await page.query_selector_all('.results')
            for result in current_results:
                text = await result.text_content()
                if text:
                    results.append(text.strip())

            # Handling pagination
            next_page_button = await page.query_selector('.pagination .page-item.active + .page-item a')
            if next_page_button:
                await next_page_button.click()  # Wait for the new page results to load completely
            else:
                break

        await browser.close()
        return results

def process_results_to_csv(results, file=''):

    data = []

    if file == '':
        file = 'ripe.csv'

    for result in results:
        # Assuming each result starts with a known category followed by a colon
        category_match = re.match(r'(\w+):\s*(.*)', result)
        if category_match:
            category, value = category_match.groups()
            data.append({'Category': category, 'Value': value.strip()})

    df = pd.DataFrame(data)
    # Sort the DataFrame by 'Category' before saving to CSV
    df_sorted = df.sort_values(by='Category')


    df_sorted.to_csv(file, index=False)

async def main(args):
    results = await fetch_all_results(args.query)

    if args.email:
        emails = set(re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', " ".join(results)))
        for email in sorted(emails):
            print(email)

    elif args.subnet:
        subnets_set = set()
        for result in results:
            if result.startswith('inetnum:'):
                ip_range = re.search(r'inetnum: (\d+\.\d+\.\d+\.\d+) - (\d+\.\d+\.\d+\.\d+)', result)
                if ip_range:
                    start_ip = ip_address(ip_range.group(1))
                    end_ip = ip_address(ip_range.group(2))
                    subnets = summarize_address_range(start_ip, end_ip)
                    for subnet in subnets:
                        subnets_set.add(subnet)
        for subnet in sorted(subnets_set):
            print(subnet)

    elif args.csv:
        if args.output:
            process_results_to_csv(results, args.output)
        else:
            process_results_to_csv(results)

    else:
        for i in results:
            print(i)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Search RIPE database for specific data.')
    parser.add_argument('-subnet', action='store_true', help='Print subnet values')
    parser.add_argument('-email', action='store_true', help='Print email addresses discovered in RIPE records')
    parser.add_argument('-csv', action='store_true', help='Save results to CSV file')
    parser.add_argument('-o', '--output', type=str, required=False, help='Define output file')
    parser.add_argument('query', type=str, help='The search query to use')
    args = parser.parse_args()

    asyncio.run(main(args))
