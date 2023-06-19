import json
import os

import requests

# Quick Instructions:
# 1. I used chrom's "copy as curl" to get a request from rotten tomatoes.com
# 2. Use https://curlconverter.com/ to get the python code for it
# 3. Put the ID and COOKIe in env vars
# 4. Run with `rt.py` >> `tv.json` or `movie.json` depending on the TYPE

USER_ID = os.getenv("ROTTEN_TOMATOES_ID")
COOKIE = os.getenv("ROTTEN_TOMATOES_COOKIE")
TYPE = "movie"  # either "tv" or "movie"


cookies = {
    "akacd_RTReplatform": "2177452799~rv=57~id=758b5bbdfcff4c0bbc93dbf0d81752b0",
    "usprivacy": "1YNN",
    "_cb": "fQ1-f-T1zgDs7AFE",
    "QuantumMetricUserID": "37eaa39b4397fc119082408cdc014565",
    "_ALGOLIA": "anonymous-5108a5c8-10a6-4513-89e8-5f7c834f205d",
    "_admrla": "2.2-f55ccf64309eaf6b-a1656264-bd60-11ed-b0cb-ae864e56871a",
    "OneTrustWPCCPAGoogleOptOut": "false",
    "eXr91Jra": "AyTjPr-GAQAAos8-CjKuXARJc_4Olozn8ZQZKc-9PMfDXKE2tvt326DRtdTNARgR26WucuFZwH8AAOfvAAAAAA|1|1|b8f1d9c28bbf4321265d8328e22f50c56847bc3e",
    "fw_vcid2": "e809110c-3866-4421-a8eb-8c4480413c0a",
    "_ga": "GA1.2.782542003.1686369277",
    "sailthru_hid": "54caf7407a1f7aee0958196ad779bdeb5e59db6949cbe9034bbf16d52419c55deb3996c72667312e708e7599",
    "number_of_review_starts": "15",
    "check": "true",
    "algoliaUT": "fa4a70dc-a4b2-41f3-8a83-a9cad13c95f1",
    "AMCVS_8CF467C25245AE3F0A490D4C%40AdobeOrg": "1",
    "s_cc": "true",
    "__host_color_scheme": "N3TnnGPn-e80hVbgkAar08ep4ATSS1Ntu6n8GF0t0FK39u1A4fDQ",
    "__host_theme_options": "1687115897609",
    "s_sq": "%5B%5BB%5D%5D",
    "cto_bundle": "XSxz719pY0o1OWl2bEVNd2ZSckJtYkMwSXpoMjNwaGZUOE1uM0I0SzAlMkYlMkZ2eDZycWdzUXRSRklCSEtjT2xmZFdLWGdZOGdWZVJXUVpyQVZmWDZIN3AlMkI3OHJRJTJCUEl6U0hjcHk3dzA3dyUyQjdzQSUyRlFYak41bEJGeG9GJTJGYzE1dm16alElMkJVRGIlMkZlcDlIclFnY3FlQ0d3ZmlNbUdDQ0JLV3piWFFGd2hqdiUyRktmdCUyQlYxZkRrJTNE",
    "ak_bmsc": "1A8D008CFEAB8CEF6A7E575A028A66A5~000000000000000000000000000000~YAAQby4gFwkXPqiIAQAAd2nM0BSm5e0PDd3V2+Q5tT4qJ35xl95UFOEu9cMZMSowEpYFlFP52twP48oS5qclPqiPj4Es69WvVf/pvqE3g8ZSRamXya2/cyAKUT59qoFkgazoWXh11dAFKyIJgHyhpuE9bADhuZ+dLjW9YIEUfFeWkZYM8J+gMCsbiYCTmypc+fC04ZWRoN+UxBWTPEL+9g/zvit7kli90PiPRBXtMYflUJitzUGMw6ncMwaton+GS8IlYGRKOO2RGbvgsiHmEkc6qKDnSnQgRwoLj5iLk/7cqV7qP9/yR9fk5ZXSUD+zsqdNks6lH849vdDhoJAfTy7mbh+/Wt+XTWwG09a2hT8kO56Uj6X3R/HeU/aPrJ5QO6cBQZBCVMgjpCMzsqVgDWIZiVrLIkUDnBr8ryKgmVs/et7WhnoDGLCV3g==",
    "mbox": "PC#f4ba7f3062864bd4ad3074f020ec28c2.35_0#1741490615|session#a8a7b68b899c42eb925100b6c1c20558#1687132099",
    "OptanonConsent": "isGpcEnabled=0&datestamp=Sun+Jun+18+2023+16%3A17%3A18+GMT-0700+(Pacific+Daylight+Time)&version=202209.1.0&isIABGlobal=false&hosts=&consentId=bedd19ff-b8a5-4f6d-888d-24602a74f4e9&interactionCount=1&landingPath=NotLandingPage&groups=1%3A1%2C4%3A1%2C6%3A1%2C7%3A1%2CSPD_BG%3A1%2Cdummy%3A1%2CFOOF%3A1&AwaitingReconsent=false",
    "mps_uuid": "29eda6ce-3d79-4e25-8c51-ceed4bb8778b",
    "AMCV_8CF467C25245AE3F0A490D4C%40AdobeOrg": "-408604571%7CMCMID%7C85110964928604003970679454560439689123%7CMCAAMLH-1687735039%7C9%7CMCAAMB-1687735039%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1687137439s%7CNONE%7CvVersion%7C4.6.0%7CMCIDTS%7C19526",
    "cognito": "%7B%22accessToken%22%3A%22eyJraWQiOiIyb21zK2VhNml0UCs1RHZmUGxrXC9qdG5uWWpXTzFqR0dzUUJEWHdOQXJQWT0iLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJkNDM5NTZiMS01MGI4LTQ3MjktOTcyOC1mZGMwODI1Mzc5ODUiLCJldmVudF9pZCI6ImE3N2QxOGM5LTk0MmMtNDhmNS1iZWE2LWM1NDY0OGMzZWEyMyIsInRva2VuX3VzZSI6ImFjY2VzcyIsInNjb3BlIjoiYXdzLmNvZ25pdG8uc2lnbmluLnVzZXIuYWRtaW4iLCJhdXRoX3RpbWUiOjE2ODcwMzQ4NzQsImlzcyI6Imh0dHBzOlwvXC9jb2duaXRvLWlkcC51cy13ZXN0LTIuYW1hem9uYXdzLmNvbVwvdXMtd2VzdC0yXzRMMFpYNGIxVSIsImV4cCI6MTY4NzEzMzgzOCwiaWF0IjoxNjg3MTMwMjM4LCJqdGkiOiIxODZlOWJhNS0zYWMxLTRmM2UtOWZlMS01NDQ3MjE4ZThmMDciLCJjbGllbnRfaWQiOiI3cHU0OHY4aTJuMjV0NHZoZXMwZWRjazMxYyIsInVzZXJuYW1lIjoiZDQzOTU2YjEtNTBiOC00NzI5LTk3MjgtZmRjMDgyNTM3OTg1In0.ZqBywd1I8RcNiRHxcKVHGw-be2qi9v53sk31_JVG5MSwtcO1bCvV4WTWH268HKkQkzVQ8O1HQOi2IMktDXaBGpptFYblAL3YZC_4cvWG2orLC3gTJtbjFIoxbduIwgt3tViYwPxmhl72WwO75R5kOfU_uH74A2ESBgLSlD09PSYml4i2xfDKnI7qudo54N9XO_HGKE6FvJW7A8eINeLaiYs65IBpUuLAZQsJY6nErK8397Hmn2tnG2cWxtxV1HPAHtaPBLhr0xeVniotURlb6Alk_oU5evNIsp3yDY3FhqHnM4Mg82DrPqOjAzoOJynoI7DqJ3Mr7prGXEYklM_uHQ%22%2C%22refreshToken%22%3A%22eyJjdHkiOiJKV1QiLCJlbmMiOiJBMjU2R0NNIiwiYWxnIjoiUlNBLU9BRVAifQ.nJv-yfoBhibVoF9UBQri4pJn6uR-XdcM5LWZAzJrdFHwHGlDh5nAf-ubvQ_bLE97l7MPFekqepBzP00zQYckkjbaUTbBsAFhKFfFvP8XdYHtGjxsua4F5qkjXv2T4PfziSy-F6ecc116pcWFcAPy7u7GjXtk9_um4ybUqOJbvYOMqDvEwK07AJWY7Z4PxFVj7djcYaSPvTXXCpav9woI8vNGFrAGBrvpZLvBPcn7OPq0oRof3ouiuVav9jdbe8UgsrqOcsB-mmQX-wODH_FVtchhRAJOukRvPCPiAD-QOIar3hA-jqyjVhKkPL-cfCIHuF3vVIAGVnX7Wg0NO9WOGQ.q0EFibcnk99FeO67.GYIlZL700sjbXWqT1fGs25vnvSaohq6ebtk_f8EHO03lkWbJMKzWsXHUmhbmlLV5EzT7XaK-ju7Acau_7j3qzMr50CFv7bTKj99pIddyGzoyX9T994sFNrI266MuUQ7iUxiHFdYggyO_YjKthAJm4IJr5gQd00T7qpteHV7ZjQTOiPG9dA1W-onavTUGLCreL11Q_DLiO1YyfT9J1NrmDseLj_BdzUT60sUtInKTd-SqCcHQmV892f_Eu2TKU8cuRszvzru3NWHFS67WN-pdNsHslOEc6bS9-L73cAaXW1IpxbUgqkcIM0Lw04kMucp_xJJ7L_UK17FKrZbtq64qh5G7fn9WIvfc_bC3zFRvCC1g33WohfFOO8pCtYVDVm9foCBagSKIHZU24RzFHQK4kNldI1o0mSgzdr_HHVDP-fAm24hXycsAFq8ZPTjYHcqQD_omlMG0cSaIapog95YayBxebv9m8unt1PgkUVkhQjqRAifHr2RmEBhvYDWYqKCOtVbjyK2XhwZnp1KaUxNw-hRa-URkkN5sIjdtkfkwZlnHSIv5YTgIYEokwhhNMSyfN3evX0lcELtKv5VvRu-oakdEapHqHqMmDJoG_mnFOZjnSPDHhCG_QqgohQYt4NSYCvbn_R6onCQ4hPIFsW8txQGkVkRR16O4e1mIB9HiFVeKdpBzi1YMM53rRqxdaU1Qy-ra-0ApkReOoLxWWoaI3r_a8qiN9v0WaRzTjnF-ouMLCm1C83xksTrjQEYhKxcGSaUTNneqx5ZvIu-F08pQT-oWS8EBAEarBxOgttrQcLHGuZkHuleQB2Q280xqHHO8j4NHsLEPioXjXqgwlqjOFPoJbu1mTg1g-joBL-Lxu8RDeKA12vzMP0bzWtAXEhAqe1ziUt3XZYiWo7YCWQ49GK0hMw5uwnXvHmu6HLQBWMAJSLhksUtE9vSBMG6PbLJ1e5v5wykkZD6wWGwwwrvF__7ijlWj0SrYgwLj9M18q8uerZQ7c1jNYLSWu0hbwuj-7AJXxrtKKm5pEBAt7BJWrcIRL04ZWAFOsvYfbWnTBfDbl3woBx3RM2cu4RAdUBvqrQu-s9HbI0pv9XNzO9MEFMK7snHtvQ4mGFezuTUP4L9RTgJVfIy936jrQbu-TunSPJKC7lGyC1OG5WTLKwkrZFZvrVafYD8USvGzYnYwmAs0qsI3ic6sINzE1biow9SGg6ID6lwF9uzjPuiNjMuhQdN2GfxaWWuSgZQScYK122CKFfyGvIqKRdEKdssPRICsW-RrClgxTJfPkXSVYYLF4h6K8DSJsa2PrlcMJCx9h8jKOEL3LMpw1q7Lpwivlg.HvQMfnFmJf0vexZkQ9_Esw%22%7D",
    "id_token": "eyJraWQiOiIxZVQySkNHWGdmRStSSis0bW5YYnNcLzVXU2NPU0hyM2NYV1pmWWpmeHhFST0iLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJkNDM5NTZiMS01MGI4LTQ3MjktOTcyOC1mZGMwODI1Mzc5ODUiLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsImlzcyI6Imh0dHBzOlwvXC9jb2duaXRvLWlkcC51cy13ZXN0LTIuYW1hem9uYXdzLmNvbVwvdXMtd2VzdC0yXzRMMFpYNGIxVSIsImNvZ25pdG86dXNlcm5hbWUiOiJkNDM5NTZiMS01MGI4LTQ3MjktOTcyOC1mZGMwODI1Mzc5ODUiLCJnaXZlbl9uYW1lIjoiRGFuaWVsIiwicGljdHVyZSI6Imh0dHBzOlwvXC9saDMuZ29vZ2xldXNlcmNvbnRlbnQuY29tXC9hXC9BQWNIVHRkVk9hUEwyRXdSNDMxUjNHRWtDZjcyaG50QmVoRFUteGx2eUlJV0k4Zz1zOTYtYyIsImF1ZCI6IjdwdTQ4djhpMm4yNXQ0dmhlczBlZGNrMzFjIiwiaWRlbnRpdGllcyI6W3sidXNlcklkIjoiMTA4MTUzNTc4NDAwODczNDQ1MjI0IiwicHJvdmlkZXJOYW1lIjoiR29vZ2xlIiwicHJvdmlkZXJUeXBlIjoiR29vZ2xlIiwiaXNzdWVyIjpudWxsLCJwcmltYXJ5IjoiZmFsc2UiLCJkYXRlQ3JlYXRlZCI6IjE2ODYzNjc4OTIzNTcifV0sImV2ZW50X2lkIjoiYTc3ZDE4YzktOTQyYy00OGY1LWJlYTYtYzU0NjQ4YzNlYTIzIiwidG9rZW5fdXNlIjoiaWQiLCJjdXN0b206c2lnbnVwX2RhdGUiOiIyMDIyLTA4LTI5IDA0OjAyOjAyIFVUQyIsImN1c3RvbTpydF9pZCI6IjgwMzk0NTY5NyIsImF1dGhfdGltZSI6MTY4NzAzNDg3NCwiZXhwIjoxNjg3MTMzODM4LCJpYXQiOjE2ODcxMzAyMzgsImZhbWlseV9uYW1lIjoiT2xzaGFuc2t5IiwiZW1haWwiOiJvbHNoYW5za3kuZGFuaWVsQGdtYWlsLmNvbSIsImN1c3RvbTpjb3VudHJ5X2NvZGUiOiJVUyJ9.RhMM84Yq5T3fNVUFBhnXUXi_SQzxs4jpX4aOhgu6BL1U2_lSMChgoXfGvL9_Q_9ZHjjb0weSKomYE0AS0aoSwi7O5gtETt7XXFAt__B8MTPtkax8MgFbDyds0pVAvfCjb9R5RG5n65TeJ572nfywCeDLhDy4BtsdxSkpwvMHt168D8N70xf4R9H0N8ts14T4AVoXcfdgzZ9EFtfy01GEvUAsccQWrREgNtpHfYsdjqFoAFvj6tMpiu880EkqGZIU-1xE5f7TndsByIG3G46BMQ5eDZt6u-fvpHe08_3q71Ks2smUozlKuMNE7mcyX2zi_dRmahI-ba2wV0PW3XofsQ",
    "akamai_generated_location": '{"zip":"98003+98023+98063+98093","city":"FEDERALWAY","state":"WA","county":"KING","areacode":"253","lat":"47.3073","long":"-122.3138","countrycode":"US"}',
    "_chartbeat2": ".1678245814411.1687130239404.0000001000100011.BYMWc1DFrAtfoHvZPqEMxKDTOzYu.1",
    "_cb_svref": "https%3A%2F%2Fwww.rottentomatoes.com%2Fprofiles%2FGeDt0zCK1fenF8NTwehrduK0seeCXJTL4H28fjquRRCzRi1zIknSwBFllCxgFepIjgSZRuYYCdOcNG",
    "sailthru_pageviews": "1",
    "__gads": "ID=179166b90eedafd0:T=1678245826:RT=1687130240:S=ALNI_MZw4IjYbMrchaJa_cahXh02WDSs7g",
    "__gpi": "UID=000009584067082e:T=1678245826:RT=1687130240:S=ALNI_MZvjy0UnEGriYR-3UnwQTNZWgGrRA",
    "_awl": "2.1687130240.5-346d87533ac5b8aa0c428810ce6dc14b-6763652d75732d7765737431-7",
    "QuantumMetricSessionID": "db7b08ab51ee4585b7588988308ae629",
    "bm_sv": "4152DDFED41F6EE17D5FC62C2C33166C~YAAQby4gF8kYPqiIAQAAfIfM0BQ9z8cnAg3a4Pa5SENByl1N9IwKzZ0/Ppke0nSjZGW+qgKrv+2nrg5IU4A/myC1Oswm9tgbY65vt+yjI6CJUo2B8JC/xFcj3xDS9kG4IoEjxSOZc6iQEzUsTHsttcEdHXV1PPrJ5jpxW7JW/K87fTGyX9rce5pwXtDZw1my5bt7SHNMbOBxt2dIQu24FF3qxqKkzbXnrfGF4F4bDFB07tiqyh4Qn8/FsPIUbKFse2mqY9unCg4=~1",
}

headers = {
    "authority": "www.rottentomatoes.com",
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.9,ru;q=0.8",
    "content-type": "application/json",
    "cookie": COOKIE,
    "origin": "https://www.rottentomatoes.com",
    "referer": f"https://www.rottentomatoes.com/profiles/ratings/{USER_ID}/{TYPE}",
    "sec-ch-ua": '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"macOS"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
}

params = {
    # "after": "eyJyZWFsbV91c2VySWQiOiJSVF9kNDM5NTZiMS01MGI4LTQ3MjktOTcyOC1mZGMwODI1Mzc5ODUiLCJlbXNJZCI6Ijk4YmVhMzhjLWNjY2UtMzY5NS04MTAyLTY3MTIzOWI3ZDg5OCIsImNyZWF0ZURhdGUiOiIyMDIzLTAzLTE4VDE5OjQ2OjUwLjcwNVoifQ==",
    "pagecount": "1000",
}

json_data = {
    "_expiry": "1687115897609",
    "_token": "N3TnnGPn-e80hVbgkAar08ep4ATSS1Ntu6n8GF0t0FK39u1A4fDQ",
}

response = requests.post(
    f"https://www.rottentomatoes.com/napi/profiles/ratings/{USER_ID}/{TYPE}",
    params=params,
    # cookies=cookies,
    headers=headers,
    json=json_data,
)

print(json.dumps(response.json()))
