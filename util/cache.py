import csv
import json
import urllib

def cache():
    print("Tommy")

    toDump = {}
    
    # Income Dicts
    incomeDump = {}
    incomeData = {}

    #gdp Dicts
    gdpDump = {}
    gdpData = {}
    
    # co2 Dicts
    co2Dump = {}
    co2Data = {}

    # -------------------- Income into toDump Dictoionary --------------------
    r = urllib.request.urlopen(
        "https://apps.bea.gov/api/data/?&UserID=1B07B684-579E-4E91-8517-DA093A82DA43&method=GetData&datasetname=Regional&TableName=SAINC1&GeoFIPS=STATE&LineCode=3&Year=2017&ResultFormat=JSON"  # Some API link goes here
    )
    income = json.loads(r.read())
    incomeDump['description'] = income['BEAAPI']['Results']['Statistic']
    incomeDump['units'] = income['BEAAPI']['Results']['UnitOfMeasure']
    for member in income['BEAAPI']['Results']['Data']:
        incomeData[ member['GeoName'].replace('*', '') ] = member['DataValue']

        # Deleting Regional Data Entries
    del incomeData['United States']
    del incomeData['New England']
    del incomeData['Mideast']
    del incomeData['Great Lakes']
    del incomeData['Plains']
    del incomeData['Southeast']
    del incomeData['Southwest']
    del incomeData['Rocky Mountain']
    del incomeData['Far West']

    incomeDump['data'] = incomeData
    toDump['income'] = incomeDump

    # -------------------- GDP into toDump Dictoionary --------------------
    g = urllib.request.urlopen(
        "https://apps.bea.gov/api/data/?&UserID=1B07B684-579E-4E91-8517-DA093A82DA43&method=GetData&datasetname=Regional&TableName=SAGDP2N&GeoFIPS=STATE&LineCode=3&Year=2017&Frequency=A&ResultFormat=JSON"  # Some API link goes here
    )
    gdp = json.loads(g.read())
    gdpDump['description'] = gdp['BEAAPI']['Results']['Statistic']
    gdpDump['units'] = gdp['BEAAPI']['Results']['UnitOfMeasure']
    for member in gdp['BEAAPI']['Results']['Data']:
        gdpData[ member['GeoName'].replace('*', '') ] = member['DataValue']

        # Deleting Regional Data Entries
    del gdpData['United States']
    del gdpData['New England']
    del gdpData['Mideast']
    del gdpData['Great Lakes']
    del gdpData['Plains']
    del gdpData['Southeast']
    del gdpData['Southwest']
    del gdpData['Rocky Mountain']
    del gdpData['Far West']
    
    gdpDump['data'] = gdpData
    toDump['gdp'] = gdpDump

    # -------------------- CO2 into toDump Dictoionary --------------------
    p = urllib.request.urlopen(
        "https://api.eia.gov/series/?api_key=a646920f26214e3dbdad25a3908f9c5f&series_id=EMISS.CO2-TOTV-TT-TO-US.A"
    )
    co2 = json.loads(p.read())
    co2Dump['description'] = co2['series'][0]['name'][:58]
    co2Dump['units'] = co2['series'][0]['units']
    
    with open("./data/id-to-alpha.csv", "r") as infile:
        alphaCodes = {}
        reader = csv.reader(infile)
        for row in reader:
            alphaCodes[ row[0] ] = row[1]
        
        print("##########")
        print(alphaCodes)
        print("##########")

        for member in alphaCodes:
            c = urllib.request.urlopen(
                "https://api.eia.gov/series/?api_key=a646920f26214e3dbdad25a3908f9c5f&series_id=EMISS.CO2-TOTV-TT-TO-{}.A".format(alphaCodes[member])
            )
            thisCo2 = json.loads(c.read())
            co2Data[thisCo2['series'][0]['name'][60:]] = thisCo2['series'][0]['data'][0][1]
                         
    co2Dump['data'] = co2Data
    toDump['co2'] = co2Dump
        
    f = "http://flags.ox3.in/svg/us/US.svg"

    with open("./data/JSON/cache.json", 'w') as outfile:
        json.dump(toDump, outfile, indent=4)

if __name__ == "__main__":
    app.debug = True
    app.run()
