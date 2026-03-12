import requests
import time
import concurrent.futures

TOKEN="eyJraWQiOiJOaUZYdUVxZkFTaXl1eHhBWGJRMDRNbm1hWTYzeHk4akZFVEliRjhLQ3BVPSIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiJiNDc4YjQ5OC1lMGYxLTcwNDQtMTJhZi1mZjI4NWFlMzQ0NjUiLCJpc3MiOiJodHRwczpcL1wvY29nbml0by1pZHAudXMtZWFzdC0xLmFtYXpvbmF3cy5jb21cL3VzLWVhc3QtMV91WjlERjZmRFUiLCJjb2duaXRvOnVzZXJuYW1lIjoidGhvbWFzLnlhbmcyQGdtYWlsLmNvbSIsIm9yaWdpbl9qdGkiOiIzODM2NGVhNS1jZjk3LTRlOTUtYmQxZi0zYjgzM2EyMjA5MTMiLCJhdWQiOiIzbzExMHNjZjE0anRjNHFtaWFiaXJqMWN1NyIsImV2ZW50X2lkIjoiOTFhM2YwNjYtMDhlMS00YzFlLTliNjQtOTg2N2RlZTIwNmE1IiwidG9rZW5fdXNlIjoiaWQiLCJhdXRoX3RpbWUiOjE3NzMzNTg0NjUsImV4cCI6MTc3MzM2MjA2NSwiaWF0IjoxNzczMzU4NDY1LCJqdGkiOiJjMzQ0MmY4NS1kODU4LTQ2NDQtYjQxZC1iN2EyYTU3YmRjMzUiLCJlbWFpbCI6InRob21hcy55YW5nMkBnbWFpbC5jb20ifQ.Xr6G_1ST7BRiui3P8GIqvt2y7RrAONsdYuOl8fkbHM3ZsGn3IaYZl93OPC4RkDaBL4YP0oCLUARt39loQSVp77LSvdY87Fp5ah6AL2hIPdtbECiL7cFN1YP05c01Uf0GI7mJ_t0kGOAJdMpO5VncPBF5aKcYeA6kypM37w5_dWkwOA-8ARubJJupwL6SWjK4v_rrjf_XbMw9baNrwgF4Qu5FlExyy7zovxlVgDgHBrSeyi3MW6B4Dv-cwbS0L5KDI23HcwfBaddFBMgn2yef8Tc9eBHRYQp0z0DzkiiAX0uSLyHqc_RNfrsJupyQtsR0R0qDmx37HitNQJZytaV8KQ"

EMAIL = "thomas.yang2@gmail.com"

CLIENT_ID = "129hgecjvg1tghuau8de3j1b4m"

API_US = "https://gx55zruuli.execute-api.us-east-1.amazonaws.com"
API_EU = "https://nuuvabun6f.execute-api.eu-west-1.amazonaws.com"

apis = [
    f"{API_US}/greet",
    f"{API_EU}/greet"
]

def call_api(url):

    start = time.time()

    r = requests.post(
        url,
        headers={"Authorization":TOKEN}
    )

    latency = time.time() - start

    return url, r.text, latency

with concurrent.futures.ThreadPoolExecutor() as executor:

    results = executor.map(call_api, apis)

for r in results:
    print(r)