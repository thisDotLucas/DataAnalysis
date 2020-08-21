import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import urllib.request, json
import os.path
import csv


scandinavian_countries = ["Sweden", "Denmark", "Norway"] # lista med skandinaviska länder


def main(): 
    
    # laddar ner data från olika källor för vidare analys
    world_data = load_data("covid_world_data.json", "https://opendata.ecdc.europa.eu/covid19/casedistribution/json/", True)
    finland_city_data = load_data("covid_finland_city_data.json", None, False)
    finland_age_data = load_data("covid_finland_age_data.json", None, False)
    finnish_municipalities_data = csv.reader(open('finnish_municipalities.csv', 'rt', encoding="utf-8"), delimiter=";")


    # data, som laddades ner, sparas i dictionaries
    world_dictionary = create_structure_for_world_data(world_data)
    finland_city_dictionary = create_structure_for_finland_city_data(finland_city_data)
    finland_age_dictionary = create_structure_for_finland_age_data(finland_age_data)
    finnish_municipalities_dictionary = create_structure_for_finnish_municipalities(finnish_municipalities_data)


    print("\n\nLänkar till använd data:\n")
    print("https://opendata.ecdc.europa.eu/covid19/casedistribution/json/")
    print("https://sampo.thl.fi/pivot/prod/sv/epirapo/covid19case/fact_epirapo_covid19case.json?column=hcdmunicipality2020-445268L")
    print("https://sampo.thl.fi/pivot/prod/sv/epirapo/covid19case/fact_epirapo_covid19case.json?column=ttr10yage-444309")
    print("https://www.kommunforbundet.fi/statistik-och-fakta/antalet-kommuner-och-stader\n\n")

    # anropar funktioner, som utför visualizering av data för uppgifter på nivå 3/5 och 5/5(3 sista funktioner) 
    print("Fråga 1: Hur mycket har antalet fall ökat per dag i de Skandinaviska länderna?")
    scandinavian_countries_plot(world_dictionary, "cases")
    
    print("Fråga 2: Hur mycket har antalet dödsfall ökat per dag i de Skandinaviska länderna?")
    scandinavian_countries_plot(world_dictionary, "deaths")
 
    print("Fråga 3: Hur många fall har uppkommit i de Skandinaviska länderna?")
    scandinavian_countries_bar(world_dictionary, "cases")

    print("Fråga 4: Hur många dödsfall har uppkommit i de Skandinaviska länderna?")
    scandinavian_countries_bar(world_dictionary, "deaths") 
    
    print("Fråga 5: Hur många fall i relation till population i de Skandinaviska länderna?")
    print("Fråga 6: Hur många dödsfall i relation till population i de Skandinaviska länderna?")
    print("Fråga 7: Hur många dödsfall i relation till fall i de Skandinaviska länderna?")
    data_per_population_table(world_dictionary, 1000000)

    print("Fråga 8: Hur ser fördelningen av antalet fall ut mellan kontinenterna?")
    continents_pie(world_dictionary, "cases")
    
    print("Fråga 9: Hur ser fördelningen av antalet dödsfall ut mellan kontinenterna?")
    continents_pie(world_dictionary, "deaths")
    
    print("Fråga 10: Hur många fall har uppkommit per kommun?")
    finnish_bar(finland_city_dictionary, 'Total number of COVID-19 cases in Finnish municipalities')
    
    print("Fråga 11: Vad är fördelningen avantal fall för olika åldersgrupper?")
    finnish_bar(finland_age_dictionary, "Total number of COVID-19 cases per age group in Finland")
    
    print("Fråga 12: Hur stor procent av invånarna i Finlands kommuner har konstaterats smittade?")
    finnish_municipalities_procentual_bar(finland_city_dictionary, finnish_municipalities_dictionary)
    

    
def continents_pie(data, measure): # visualizering av antal fall och dödsfall kontinentvis, measure = cases or deaths
    
    continent_map = {} # map med kontinenter

    for continent in data.keys(): # data läggs i map med kontinenter
        
        if continent == "Other": continue 

        if continent not in continent_map.keys():
            continent_map[continent] = 0

        for country in data[continent].keys():
            continent_map[continent] = continent_map[continent] + sum((int(date[measure]) for date in data[continent][country]))

   # visualizering parametrizeras
    labels = list(continent_map.keys())
    sizes =  [continent_map[key] for key in continent_map.keys()]
 
    colors = ['#ff9999','#66b3ff','#99ff99','#ffcc99','#fafa93']
    
    fig1, ax1 = plt.subplots(figsize=(20,10))
    ax1.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=90)
    ax1.axis('equal')

    figure_title = ("Distribution of COVID-19 " + measure + " between continents")

    plt.text(0.5, 1.08, figure_title, horizontalalignment='center', fontsize=12, transform=ax1.transAxes) 
    plt.tight_layout()
    plt.show()


def scandinavian_countries_plot(data, measure): # linjär graf för antal fall och dödsfall per dag i skandinaviska länder
    
    country_map = {} # map med länder

    for country in scandinavian_countries: # mappen med länderna fylls med datan

        if country not in country_map.keys():
            country_map[country] = {"dates": [], measure: []}
        
        counter = 0

        for datesAndMeasure in data["Europe"][country]:
            
            if counter % 2 == 0:
                country_map[country]["dates"].append(datesAndMeasure["dateRep"])
                country_map[country][measure].append(int(datesAndMeasure[measure]))
            
            counter = counter + 1
        
       
        country_map[country]["dates"] = country_map[country]["dates"][::-1] # reverse lista
        country_map[country][measure] = country_map[country][measure][::-1] # reverse lista
        

    fig, ax = plt.subplots(figsize=(20,10))
    
    for country in scandinavian_countries:
        if country == scandinavian_countries[0]:
            plt.plot("dates", measure, data=country_map[country], label=country)
        else:
            plt.plot(measure, data=country_map[country], label=country)
        
    ax.xaxis.set_tick_params(rotation=90, labelsize=10)

    plt.ylabel("New " + measure)
    plt.title("New " + measure + " / day in Scandinavian countries")
    plt.legend()
    plt.show()



def scandinavian_countries_bar(data, measure): # bar graf med total antal av fall och dödsfall i skandinaviska länder
    
    total_measure_map = {}

    for country in scandinavian_countries:

        if country not in total_measure_map.keys():
            total_measure_map[country] = 0


        for datesAndMeasure in data["Europe"][country]:
            
            total_measure_map[country] = total_measure_map[country] + int(datesAndMeasure[measure])
    
    y_pos = np.arange(len(scandinavian_countries))

    height = []

    for key in scandinavian_countries:
        height.append(total_measure_map[key])

    fig, ax = plt.subplots(figsize=(20, 10))
    plt.bar(y_pos, height, color=['blue', 'orange', 'green', 'red', 'purple'])
    plt.xticks(y_pos, scandinavian_countries)

    plt.title('Total number of ' + measure + ' in Scandinavian Countries')
    plt.show()    


def data_per_population_table(data, namnare): # visualizering av antal dödsfall och fall i relation med population samt relation mellan fall och dödsfall. 
   
    our_map = {}

    for country in scandinavian_countries:
    
        if country not in our_map.keys():
            our_map[country] = {"cases": 0, "deaths": 0, "population": data["Europe"][country][0]["popData2018"]}

        for casesAndDeaths in data["Europe"][country]:
                
                our_map[country]["cases"] = our_map[country]["cases"] + int(casesAndDeaths["cases"])
                our_map[country]["deaths"] = our_map[country]["deaths"] + int(casesAndDeaths["deaths"])


    y_pos = np.arange(len(scandinavian_countries))

    result_map = {}

    for key in scandinavian_countries:
        result_map[key] = {"casePerPop": round(our_map[key]["cases"]/(float(our_map[key]["population"])/namnare), 2), "deathPerPop": round(our_map[key]["deaths"]/(float(our_map[key]["population"])/namnare), 2), "deathsPerCases": round(float(our_map[key]["deaths"]/our_map[key]["cases"]), 2)}


    columns = ("Country", "Case per million", "Death per million", "Death per case")   
    
    fig, ax = plt.subplots(figsize=(20,10))
    fig.patch.set_visible(False)
    
    ax.axis('off')
    ax.axis('tight')

    df = pd.DataFrame([(key, result_map[key]["casePerPop"], result_map[key]["deathPerPop"], result_map[key]["deathsPerCases"]) for key in result_map.keys()], columns=columns)

    ax.table(cellText=df.values, colLabels=df.columns, bbox=[0.4, 0.4, 0.4, 0.4], loc='left')

    fig.tight_layout()
    
    plt.show()             
            
            
def finnish_bar(data, title): # visualizering av antal fall stadvis samt åldergruppsvis i Finland

    cities = list(data.keys())
    cases = [data[city] for city in data.keys()]

    fig, ax = plt.subplots(figsize=(20, 10))    
    plt.bar(cities, cases)
    plt.xticks(cities, rotation=90)

    plt.title(title)
    plt.show()  


def finnish_municipalities_procentual_bar(case_data, population_data): # antalet invånare i finska städer i förhållande till total antal invånare i landet
    
    percentage_map = {}

    for city in population_data.keys():

        if city in case_data.keys():
            percentage_map[city] = round((case_data[city]/population_data[city]) * 100.0, 4)
    
    fig, ax = plt.subplots(figsize=(20, 10))
    plt.bar(list(percentage_map.keys()), [percentage_map[city] for city in percentage_map.keys()])
    plt.xticks(list(percentage_map.keys()), rotation=90)

    plt.title("% of population with COVID-19 in municipalities")
   
    plt.show()  

    

# Dictionary1 nycklar = världsdelar, Dictionary2 (innre dictionaryn) nycklar = länder
# ex dictionary["Europe"]["Finland"] = lista med alla Json inlägg för Finland.

# https://opendata.ecdc.europa.eu/covid19/casedistribution/json/
def create_structure_for_world_data(data): # skapar dictionary med data från covid_world_data.json filen , (key = världsdel, value = (key = land i världsdel, value= lista med alla datum för land))

    our_dict = {}

    for element in data['records']: #Ifall ny världsdel skapa en ny dict
        if element["continentExp"] not in our_dict.keys():
            our_dict[element["continentExp"]] = {}

        if element["countriesAndTerritories"] not in our_dict[element["continentExp"]].keys(): #Ifall nytt land skapa en lista för det landet
            our_dict[element["continentExp"]][element["countriesAndTerritories"]] = []

        
        our_dict[element["continentExp"]][element["countriesAndTerritories"]].append(element)


    return our_dict
    

# https://sampo.thl.fi/pivot/prod/sv/epirapo/covid19case/fact_epirapo_covid19case.json?column=hcdmunicipality2020-445268L 
def create_structure_for_finland_city_data(data): #skapar dictionary för städer i Finland, (key = stad, value = antal besmittade för stad)

    our_dict = {}

    for city in data["dataset"]["dimension"]["hcdmunicipality2020"]["category"]["label"]:
        
        if data["dataset"]["value"][str(data["dataset"]["dimension"]["hcdmunicipality2020"]["category"]["index"][city])] == "..": continue # .. = ingen data available för denna stad

        our_dict[data["dataset"]["dimension"]["hcdmunicipality2020"]["category"]["label"][city]] = int(data["dataset"]["value"][str(data["dataset"]["dimension"]["hcdmunicipality2020"]["category"]["index"][city])])
    
    return our_dict


# https://sampo.thl.fi/pivot/prod/sv/epirapo/covid19case/fact_epirapo_covid19case.json?column=ttr10yage-444309
def create_structure_for_finland_age_data(data): #skapar dictionary för antalet fall i förhållande till åldersgrupper i Finland, (key = åldersgrupp, value = antal besmittade i åldergrupp)
    
    our_dict = {}

    for age in data["dataset"]["dimension"]["ttr10yage"]["category"]["label"]:
        
        if "Alla åldersgrupper" != data["dataset"]["dimension"]["ttr10yage"]["category"]["label"][age]:
            our_dict[data["dataset"]["dimension"]["ttr10yage"]["category"]["label"][age]] = int(data["dataset"]["value"][str(data["dataset"]["dimension"]["ttr10yage"]["category"]["index"][age])])

    return our_dict

# https://www.kommunforbundet.fi/statistik-och-fakta/antalet-kommuner-och-stader
def create_structure_for_finnish_municipalities(data): #skapar dictionary med kommunerer i Finland, (key = stad, value = invånarantal)
    
    our_dict = {}

    for row in data:
        our_dict[row[0]] = int(row[1].replace(" ", ""))

    return our_dict

def load_data(file, url, availableOnline): #laddar senaste json-filen vid behov.

    if availableOnline:
        if (not os.path.isfile(file)) or isEmpty(file) or (not isLatestDate(file)): # om fil inte existerar eller filen är tom eller filen inte är up-to-date så hämtas den från webben. 
            
            with urllib.request.urlopen(url) as url:
                
                data = json.loads(url.read().decode())
                json_object = json.dumps(data, indent = 4) 

                with open(file, 'w') as filetowrite:
                    filetowrite.write(json_object)
    
    with open(file, 'r', encoding="utf-8") as f:
        data = json.load(f)   

    return data



def isEmpty(file): # returnerar true ifall filen är tom.
    return os.stat(file).st_size == 0



def isLatestDate(file): # returnerar true ifall sparade file är up-to-date.

    with open(file, 'r') as f:
        data = json.load(f)

    return data["records"][0]["dateRep"] == datetime.today().strftime('%m/%d/%Y') # jämför första inläggets datum från json datan med dagens datum.
    


if __name__ == "__main__":
    main()
