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
        incomeData[ member['GeoName'] ] = member['DataValue']

        # Deleting Regional Data Entries
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
    
    p = urllib.request.urlopen(
        "https://api.eia.gov/series/?api_key=a646920f26214e3dbdad25a3908f9c5f&series_id=EMISS.CO2-TOTV-TT-TO-US.A"
    )
    co2 = json.loads(p.read())
    
    f = "http://flags.ox3.in/svg/us/US.svg"

    with open("/Users/Joey/Desktop/compSci/SoftDev/atmosphere/data/JSON/cache.json", 'w') as outfile:
        json.dump(toDump, outfile, indent=4)

if __name__ == "__main__":
    app.debug = True
    app.run()
