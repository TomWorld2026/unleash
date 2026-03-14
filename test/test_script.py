import requests
import time
import concurrent.futures

TOKEN = "eyJraWQiOiIxVWRkbUNOcTlxMTRUQ0M4elhFUXR4MTB3R043bzhBMklLUjlGclB1Q2cwPSIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiIyNDM4MDRmOC1mMDExLTcwMDktNjIyNC03MzQwNGY4OTY3ZDMiLCJpc3MiOiJodHRwczpcL1wvY29nbml0by1pZHAudXMtZWFzdC0xLmFtYXpvbmF3cy5jb21cL3VzLWVhc3QtMV92UTZjR1ZvdUMiLCJjb2duaXRvOnVzZXJuYW1lIjoidGhvbWFzLnlhbmcyQGdtYWlsLmNvbSIsIm9yaWdpbl9qdGkiOiJkMjQyYzQ5Zi1iNTU1LTQ0ZWItYmU4Mi0zM2UzZDQxNTZlNDMiLCJhdWQiOiIzZXFwZGRxdjQyYnAzcWIyNHJqcGg3dHQzciIsImV2ZW50X2lkIjoiN2E4YzhhZGQtOWY0Mi00NDcyLWFjODUtYTgwZDQzMjg4ZDg2IiwidG9rZW5fdXNlIjoiaWQiLCJhdXRoX3RpbWUiOjE3NzM0NzgzNjEsImV4cCI6MTc3MzQ4MTk2MSwiaWF0IjoxNzczNDc4MzYxLCJqdGkiOiIwMzgwNTEwOS04YWY3LTQyNTktYTI4ZS01NjYwNThlYWIwNDgiLCJlbWFpbCI6InRob21hcy55YW5nMkBnbWFpbC5jb20ifQ.OhORi_1qUXysCc5Wq8mX0nRr5KtgH7aQUED7_hjrX6SjRp55rMn_yoDclD5JwmWHYkhhdnkC2P39xMe7PJgkplExyxu0EBYRL_e77qpR3oVJ7bULlY_F_5_CL-RANzicEzg24Bi2XOIsKWaWf_c1tMDx9zigYaN_HZ5Ea96AdCsRuRuz-ECgCPCHxrA-2wwymGjpu8KptL21s3s32Tczz6jGeVWITal2Rq3hzuD1IWVRUZ59yN-qJKbYD0AKGSc1VSoPIcV0_ceWVr93j444nJA4P0PpmLX1ucFng6Bif_5MEx5Rq9Zl4gPUPmDdD3-scagM-Kca6gks8rjAfK1SWQ"

API_US = "https://v63wsmaqna.execute-api.us-east-1.amazonaws.com"
API_EU = "https://7c285csbog.execute-api.eu-west-1.amazonaws.com"

apis = [
    f"{API_US}/greet",
    f"{API_EU}/greet",
    f"{API_US}/dispatch",
    f"{API_EU}/dispatch"    
]

def call_api(url):

    start = time.time()

    r = requests.post(
        url,
        headers={
            "Authorization": f"Bearer {TOKEN}",
            "Content-Type": "application/json"
        },
        json={}
    )

    latency = time.time() - start

    return url, r.status_code, r.text, latency


with concurrent.futures.ThreadPoolExecutor() as executor:
    results = executor.map(call_api, apis)

for r in results:
    print(r)