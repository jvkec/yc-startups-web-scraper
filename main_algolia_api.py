import requests

APP_ID = "45BWZJ1SGC"
API_KEY = API_KEY = "MjBjYjRiMzY0NzdhZWY0NjExY2NhZjYxMGIxYjc2MTAwNWFkNTkwNTc4NjgxYjU0YzFhYTY2ZGQ5OGY5NDMxZnJlc3RyaWN0SW5kaWNlcz0lNUIlMjJZQ0NvbXBhbnlfcHJvZHVjdGlvbiUyMiUyQyUyMllDQ29tcGFueV9CeV9MYXVuY2hfRGF0ZV9wcm9kdWN0aW9uJTIyJTVEJnRhZ0ZpbHRlcnM9JTVCJTIyeWNkY19wdWJsaWMlMjIlNUQmYW5hbHl0aWNzVGFncz0lNUIlMjJ5Y2RjJTIyJTVE"
URL = "https://45bwzj1sgc-dsn.algolia.net/1/indexes/*/queries"

HEADERS = {
    "X-Algolia-Application-Id": APP_ID,
    "X-Algolia-API-Key": API_KEY,
    "Content-Type": "application/json"
}

all_companies = []
page = 0

while True:
    payload = {
        "requests": [
            {
                "indexName": "YCCompany_production",
                "params": f"hitsPerPage=1000&page={page}"
            }
        ]
    }

    res = requests.post(URL, headers=HEADERS, json=payload)
    hits = res.json()["results"][0]["hits"]

    if not hits:
        break

    all_companies.extend(hits)
    page += 1
    print(f"Fetched page {page}, total companies so far: {len(all_companies)}")

print(f"Done! Total companies collected: {len(all_companies)}")