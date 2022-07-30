import re
import json
import requests
jsonurl = "https://ci.turkpatent.gov.tr/Data/GetList?Name=&FileNumber=&ApplicationDate=&ApplicationDateEnd=&RegistrationDate=&RegistrationDateEnd=&TypeId=&ProductGroupId=&CityId=&StatusId="
photourl = "https://ci.turkpatent.gov.tr/Pictures/GeographicalSigns/"
Tr2Eng = str.maketrans("çğıöşüİ", "cgiosui")


nftData = {
  "name": "",
  "description": "",
  "image": "",
  "attributes":"",
  "external_url": "https://ruzgarerik.com"
}

def fromfile():
    global data
    f = open('veritabani.json', "r", encoding="utf8")
    data = json.loads(f.read())
    f.close() 

def fromAPI():
    global data
    url = requests.get(jsonurl)
    text = url.text    
    data = json.loads(text)

def parseJson():
    global data
    global productinfo
    fromAPI()
    productinfo = data['data']
    for i in productinfo:
        if i["StatusName"] == "Tescilli":
            jsonname = i['Name'].replace("İ", "i").replace("/", "").replace(" ", "_").lower().translate(Tr2Eng).replace("̇", "").replace("\t", "")
            nftData["name"] = i['Name']
            nftData["image"] = photourl + i["Picture"]
            nftData["description"] = i['Name']
            tesciltarihi = i["RegistrationDate"]
            try:
                tesciltarihi = re.findall(r'\d+',tesciltarihi)
                tesciltarihi = tesciltarihi[0]
            except:
                tesciltarihi = 0
            nftData["attributes"] = [{"display_type": "date", "trait_type": "Tescil Tarihi", "value": int(tesciltarihi)}, {"trait_type": "Id", "value": i["Id"]}, {"trait_type": "Türü", "value": i["ProductGroupName"]},{"trait_type": "Sehir", "value": i["CityName"]}]
            try:
                with open(f'{jsonname}.json', 'w', encoding="utf8" ) as f:
                    json.dump(nftData, f, indent=4, ensure_ascii=False)
                    print("Created",jsonname)
            except:
                print("Hata")     
        
parseJson()
