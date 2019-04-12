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
        ('cse_tok', 'AKaTTZjLDKsWDS-YViFo3__PZqMn:1555000558345'),
        ('exp', 'csqr'),
        ('oq', query),
        ('gs_l', 'partner-generic.12...0.0.6.5998.0.0.0.0.0.0.0.0..0.0.gsnos,n=13...0.0....34.partner-generic..5.0.0.'),
        ('callback', 'google.search.cse.api10986'),
    )

    response = requests.get('https://cse.google.com/cse/element/v1', headers=headers, params=params, cookies=cookies)
    apiOutput = response.text[35:-2]
    cveJson = json.loads(apiOutput)
    allResults = cveJson['results']

    cveDetails = []

    for result in allResults:
        cveTitle = result['title'].split(" ")[0]
        cveUrl = result['url']

        cveDetails.append({"title": cveTitle, "url": cveUrl})

    return cveDetails

cveSearcher('Possible hardcoded password')