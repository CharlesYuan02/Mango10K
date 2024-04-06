from sec_cik_mapper import StockMapper
import requests
import json
import os 



def edgar_scraper(ticker_name):
    # mapper object to convert the ticker to cik
    cik_mapper = StockMapper()
    # ticker_to_cik is a dictionary, just index it by the ticker of the compnay you're interested in, 
    # e.g.
    print(f"{ticker_name}'s cik is {cik_mapper.ticker_to_cik[ticker_name]}")
    cik_Value_Of_Ticker = cik_mapper.ticker_to_cik[ticker_name]
    cik_Value_Of_Ticker = str(cik_Value_Of_Ticker).zfill(10) # pads to the left by 0s until it is 10 zeros long (doesn't add 10 zeros in total)

    edgar_req_url = f'https://data.sec.gov/submissions/CIK{cik_Value_Of_Ticker}.json'
    # if you leave this out, you'll get a 401 response
    user_agent_header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"}
    edgar_json_response = requests.get(edgar_req_url, headers = user_agent_header).json()
    # it's formatted in dict form now
    pretty_response = json.dumps(edgar_json_response, indent = 4)

    # create directory and write output 
    # we're using makedirs instead of mkdir because exist_ok checks if it already exists
    output_dir = f'{ticker_name}_filings'
    os.makedirs(output_dir, exist_ok= True)
    with open(f'{output_dir}/{ticker_name}.json', 'w') as f:
        f.write(pretty_response)

    print("If you're seeing this, I executed.")


if __name__ == "__main__":
    tickerName = input("Enter the company's ticker name")
    edgar_scraper(tickerName)


