import urllib
import urllib2
import shutil

req = urllib2.Request('http://www.weg.net/catalog/weg/US/en/Electric-Motors/AC-Motors---NEMA/General-Purpose-ODP-TEFC/ODP/ODP-Rolled-Steel/W01-Rolled-Steel/W01-Rolled-Steel-Premium-Efficiency-%28DOE%29/Rolled-Steel-0-75-HP-4P-56C-3Ph-575-V-60-Hz-IC01---ODP---Footless/p/12809255/generateDocuments')
values = { 'datasheet': 'true',
'_datasheet': 'on',
'_graphics': 'on',
'_dimensionalCurvesRotation':'on',
'_dimensionalCurvesPotency':'on',
'_dimensionalCurvesThermic':'on',
'_dimensionalCurvesInversor':'on',
'unity':'lb/ft.lb/sq.ft.lb/lb',
'language': 'en',
'customer': '',
'customerRef': '',
'observation': '',
'tokenDocs':'wegDoc1499159479744'
}
req.add_data(urllib.urlencode(values))
resp = urllib2.urlopen(req)

with open('file.pdf', 'wb') as file:
    shutil.copyfileobj(resp.fp, file)

