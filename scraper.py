import requests
import json

# for mapping the CIK (aka the primary key/id of every company registered in the SEC)


# mapper object
from sec_cik_mapper import StockMapper

cik_mapper = StockMapper()
# ticker_to_cik is a dictionary, just index it by the ticker of the compnay you're interested in, 

# e.g.
print(f"TSLA's cik is {cik_mapper.ticker_to_cik['AAPL']}")

tesla_edgar_req_url = "https://data.sec.gov/submissions/CIK0001318605.json"
# if you leave this out, you'll get a 401 response
user_agent_header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"}

tesla_edgar_req_json = requests.get(tesla_edgar_req_url, headers = user_agent_header).json()

# it's formatted in dict form now
pretty_print = json.dumps(tesla_edgar_req_json, indent = 4)
# print(pretty_print)