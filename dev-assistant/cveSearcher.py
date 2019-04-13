def cveSearcher(query):

    import requests
    import json

    cookies = {
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:66.0) Gecko/20100101 Firefox/66.0',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'DNT': '1',
        'Connection': 'keep-alive',
        'TE': 'Trailers',
    }


    params = (
        ('rsz', 'filtered_cse'),
        ('num', '10'),
        ('hl', 'en'),
        ('source', 'gcsc'),
        ('gss', '.com'),
        ('cx', '001970827437957689766:wsv7kcniwgs'),
        ('q', query),
        ('safe', 'off'),
        ('cse_tok', 'AKaTTZhN3s13VOWGnU35VTDL2z-T:1555125434946'),
        ('exp', 'csqr'),
        ('callback', 'google.search.cse.api8456'),
    )

    response = requests.get('https://cse.google.com/cse/element/v1', headers=headers, params=params, cookies=cookies)
    apiOutput = response.text[34:-2]
    cveJson = json.loads(apiOutput)
    allResults = cveJson['results']

    cveDetails = []

    for result in allResults:
        cveTitle = result['title'].split(" ")[0]
        cveUrl = result['url']

        cveDetails.append({"title": cveTitle, "url": cveUrl})

    return cveDetails

# cveSearcher('Possible hardcoded password')