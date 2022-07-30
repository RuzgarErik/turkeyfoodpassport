import re
import json
import requests
import os

jsonurl = "https://ci.turkpatent.gov.tr/Data/GetList?Name=&FileNumber=&ApplicationDate=&ApplicationDateEnd=&RegistrationDate=&RegistrationDateEnd=&TypeId=&ProductGroupId=&CityId=&StatusId="
photourl = "https://ci.turkpatent.gov.tr/Pictures/GeographicalSigns/"
Tr2Eng = str.maketrans("çğıöşüİ", "cgiosui")
jsonmetadataurl= "https://ruzgarerik.com/turkeyfoodpassport/"


nftData = {
  "Name": "",
  "CityName": "",
  "image": "",
  "jsonURL":""
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
    
    
sehirler = ["Adana", "Adıyaman", "Afyonkarahisar", "Ağrı", "Aksaray", "Amasya", "Ankara", "Antalya", "Ardahan", "Artvin", "Aydın", "Balıkesir", "Bartın", "Batman", "Bayburt", "Bilecik", "Bingöl", "Bitlis", "Bolu", "Burdur", "Bursa", "Çanakkale", "Çankırı", "Çorum", "Denizli", "Diyarbakır", "Düzce", "Edirne", "Elazığ", "Erzincan", "Erzurum", "Eskişehir", "Gaziantep", "Giresun", "Gümüşhane", "Hakkâri", "Hatay", "Iğdır", "Isparta", "İstanbul", "İzmir", "Kahramanmaraş", "Karabük", "Karaman", "Kars", "Kastamonu", "Kayseri", "Kilis", "Kırıkkale", "Kırklareli", "Kırşehir", "Kocaeli", "Konya", "Kütahya", "Malatya", "Manisa", "Mardin", "Mersin", "Muğla", "Muş", "Nevşehir", "Niğde", "Ordu", "Osmaniye", "Rize", "Sakarya", "Samsun", "Şanlıurfa", "Siirt", "Sinop", "Sivas", "Şırnak", "Tekirdağ", "Tokat", "Trabzon", "Tunceli", "Uşak", "Van", "Yalova", "Yozgat", "Zonguldak"]

def parseJson():
    global data
    global productinfo
    fromAPI()
    productinfo = data['data']
    for j in sehirler:
        tempsehirlist = []
        for i in productinfo:
            apiData = {"name": "","CityName": "","code":"","jsonURL":""}
            tempList = []
            if i["StatusName"] == "Tescilli" and i["CityName"] == j:
                global proper_cityname
                proper_cityname = i['CityName'].replace("İ", "i").replace("/", "").replace(" ", "_").lower().translate(Tr2Eng).replace("̇", "").replace("\t", "")
                jsonname = i['Name'].replace("İ", "i").replace("/", "").replace(" ", "_").lower().translate(Tr2Eng).replace("̇", "").replace("\t", "")
                tesciltarihi = i["RegistrationDate"]
                try:
                    tesciltarihi = re.findall(r'\d+',tesciltarihi)
                    tesciltarihi = tesciltarihi[0]
                except:
                    tesciltarihi = 0
                try:
                    apiData["name"] = i['Name']
                    apiData["CityName"] = i['CityName']
                    apiData["code"] = [{"uri":photourl + i["Picture"]}]
                    apiData["jsonURL"] =  jsonmetadataurl +jsonname+ ".json"
                    tempsehirlist.append(apiData)

                except Exception as e:
                    print("Hata")
                    print(e)

        with open(f'./city/{proper_cityname}.json', 'w', encoding="utf8" ) as f:
            json.dump(tempsehirlist, f, indent=4, ensure_ascii=False)
            print("Created",proper_cityname)





    
    
parseJson()


