from sec_cik_mapper import StockMapper
import requests
import json

# for mapping the CIK (aka the primary key/id of every company registered in the SEC)

def edgar_scraper(ticker_name):

# mapper object

    cik_mapper = StockMapper()
    # ticker_to_cik is a dictionary, just index it by the ticker of the compnay you're interested in, 

    # e.g.
    print(f"{ticker_name}'s cik is {cik_mapper.ticker_to_cik[ticker_name]}")
    cik_Value_Of_Ticker = cik_mapper.ticker_to_cik[ticker_name]
    cik_Value_Of_Ticker = str(cik_Value_Of_Ticker).zfill(10)

    edgar_req_url = f'https://data.sec.gov/submissions/CIK{cik_Value_Of_Ticker}.json'
    # if you leave this out, you'll get a 401 response
    user_agent_header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"}
    edgar_json_response = requests.get(edgar_req_url, headers = user_agent_header).json()
    # it's formatted in dict form now
    pretty_print = json.dumps(edgar_json_response, indent = 4)

    with open(f'{ticker_name}.response.json', 'w') as f:
        f.write(pretty_print)

    print("If you're seeing this, I executed.")

edgar_scraper("AAPL")