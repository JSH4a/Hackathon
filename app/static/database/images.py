import requests
import random
import re

#import requests
#from bs4 import BeautifulSoup

from bing_image_urls import bing_image_urls

class Fetcher:
    def __init__(self):
        print("making")
        self.headers = {
            "accept": "application/json",
            "authorization": "Bearer 030e7b4744c5fdfb77836e9213a5cef8"
        }

        self.exampleProduct = [("iPhone 13", "apple"), ("iPad air", "apple"), ("HP pavillion", "HP")]
        self.exampleProduct2 = [("Smartwatch", "Samsung"), ("Electric toothbrush", "Philips"), ("Yoga mat", "Lululemon"), ("Hair straightener", "GHD"), ("Running shoes", "Nike"), ("Bluetooth speaker", "JBL"), ("Drone", "DJI"), ("Espresso machine", "De'Longhi"), ("Gaming laptop", "Alienware"), ("Cordless vacuum", "Dyson"), ("Wireless headphones", "Bose"), ("Action camera", "GoPro"), ("Gaming console", "Sony"), ("Air fryer", "Ninja"), ("Fitness tracker", "Fitbit"), ("Pressure cooker", "Instant Pot"), ("Smart thermostat", "Nest"), ("Outdoor grill", "Weber"), ("Portable power bank", "Anker"), ("Wireless charger", "Belkin"), ("Projector", "Epson"), ("Camera lens", "Canon"), ("Standing desk", "Vari"), ("Mechanical keyboard", "Corsair"), ("3D printer", "Creality"), ("Rice cooker", "Zojirushi"), ("Sous vide machine", "Anova"), ("Home security camera", "Ring"), ("VR headset", "Oculus"), ("Desktop computer", "HP"), ("Air purifier", "Coway"), ("Electric kettle", "Breville"), ("Bread maker", "Cuisinart"), ("Robot vacuum", "Roomba"), ("Bluetooth earbuds", "Sony"), ("Gaming mouse", "Razer"), ("Portable speaker", "Sony"), ("Smart scale", "Withings"), ("Outdoor speaker", "Sonos"), ("Car dash camera", "Garmin"), ("Wireless mouse", "Logitech"), ("Smart plug", "TP-Link"), ("Hair dryer", "Conair"), ("Portable air conditioner", "Honeywell"), ("GPS watch", "Garmin"), ("Smart lock", "August"), ("Noise-cancelling headphones", "Sony"), ("Dash cam", "Blackvue"), ("Smart bulb", "Philips Hue"), ("Water filter", "Brita")]
        self.exampleCompanies = ["Walmart", "Amazon", "Apple", "ExxonMobil", "Berkshire Hathaway", "Toyota Motor", "McKesson", "CVS Health", "UnitedHealth Group", "AmerisourceBergen", "Samsung Electronics", "AT&T", "Ford Motor", "General Motors", "Chevron", "Cardinal Health", "Costco Wholesale", "Verizon Communications", "Kroger", "General Electric", "Walgreens Boots Alliance", "Fannie Mae", "JPMorgan Chase", "Boeing", "Honda Motor", "Comcast", "Valero Energy", "Phillips 66", "Anthem", "Microsoft", "Citigroup", "Aetna", "State Farm Insurance", "American Airlines Group", "Pfizer", "Johnson & Johnson", "Exelon", "Walt Disney", "Procter & Gamble", "Delta Air Lines", "Hess", "United Technologies", "The Home Depot", "Caterpillar", "The Boeing Company", "Intel", "PepsiCo", "The Coca-Cola Company", "Bristol-Myers Squibb", "MetLife", "Ford Motor Company", "The Goldman Sachs Group", "Morgan Stanley", "Honeywell International", "ConocoPhillips", "Cisco Systems", "Oracle", "The Dow Chemical Company", "American Express", "United Parcel Service", "The Travelers Companies", "The Charles Schwab Corporation", "Deere & Company", "3M", "The Blackstone Group", "The Williams Companies", "The Southern Company", "The AES Corporation", "The Southern California Edison Company", "The Berkshire Hathaway Energy Company", "The Sempra Energy Company", "The NextEra Energy Company", "The Exelon Corporation", "The Dominion Energy Company", "The National Grid plc", "The Enbridge Energy Company", "The Spectra Energy Partners Company", "The Williams Partners Company", "The Duke Energy Company", "The General Electric Company", "The FirstEnergy Corporation", "The Eversource Energy Company", "The American Electric Power Company", "The Xcel Energy Company", "The Entergy Corporation", "The PG&E Corporation", "The Edison International Company", "The Tenet Healthcare Corporation", "The Community Health Systems Company", "The HCA Healthcare Company", "The Universal Health Services Company", "The Anthem Health Insurance Company", "The Cigna Health Insurance Company", "The Humana Health Insurance Company", "The Aetna Health Insurance Company", "The UnitedHealthcare Health Insurance Company", "The Blue Cross Blue Shield Association", "The Kaiser Permanente Health Insurance Company"]

    def getCO2Product(self, product, company):
        #url = "https://api.ditchcarbon.com/v1.0/product?name=",product,"%2014&manufacturer=",company #,"&category_name=phone"
        #url = "https://api.ditchcarbon.com/v1.0/product?name=iPhone%2013&manufacturer=apple"
        url = "https://api.ditchcarbon.com/v1.0/product?name="+product+"&manufacturer="+company
        #print(url)


        response = requests.get(url, headers=self.headers)

        if(response != b'{"errors":[{"status":400,"detail":"Price can\'t be blank"}]}'):
            print("RESPONSE: ", response.content)

        return response.text
    
    def getRandomProduct(self):
        product = self.exampleProduct[ random.randint(0, len(self.exampleProduct))-1 ]
        outt = self.getCO2Product(product[0], product[1])
        #outt = {"carbon_footprint":316.07832,"name":"HP Pavilion 13 Laptop PC","manufacturer":"HP","unit":"count","manufacturer_declared_carbon_footprint":335.0,"source_url":"https://h20195.www2.hp.com/v2/GetDocument.aspx?docname=c07645383","methodology":"product","manufacturer_reported_kgco2":335.0,"kgco2":316.07832,"model":"HP Pavilion 13 Laptop PC"}
        
        print("1",outt)
        print("1.5",type(outt))
        print("2",product[0])
        
        split = list( filter(None, re.split("[{,:}]+", outt)) )
        cf = -1
        print("2.5",split)

        for i in range(0, len(split)):
            if(split[i] == "\"carbon_footprint\""):
                cf = (float)(split[i+1])
                break
        print("3", cf )


        return (product[0], cf)

    def getAllProducts(self):
        ret = []
        for product in self.exampleProduct:
            outt = self.getCO2Product(product[0], product[1])
            
            split = list( filter(None, re.split("[{,:}]+", outt)) )
            cf = -1

            for i in range(0, len(split)):
                if(split[i] == "\"carbon_footprint\""):
                    cf = (float)(split[i+1])
                    break
            ret.append( (product[0], cf) )
        return ret

    def getCompanyEm(self, company):
        url = "https://api.ditchcarbon.com/v1.0/supplier?name="+company+"&currency=GBP"

        response = requests.get(url, headers=self.headers).json()

        #print("1: ",type(response) )

        co2 = response["ef_kg_co2eq"]

        #print("3: ", co2 )

        return (company, co2)
    
    def getRandomCompany(self):
        ranComp = self.exampleCompanies[random.randint(0, len(self.exampleCompanies) -1)]
        return self.getCompanyEm( ranComp )
    
    def randCompWithImage(self):
        outt = self.getRandomCompany()
        image = Fetcher.getImage(outt[0])
        return (outt[0], outt[1], image)

    def getImage(objectt):
        url = bing_image_urls(objectt, limit=1)[0]
        return url

print(Fetcher.getImage("Apple"))