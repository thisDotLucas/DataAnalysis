import json
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('seaborn-whitegrid')

nordic_countries = ["Finland", "Sweden", "Iceland", "Denmark", "Norway"]

def main():
    data = load_data('projekt3/covid_data.json')
    
    dictionary = create_structure(data)

    nordic_countries_plot(dictionary, "cases")
    nordic_countries_plot(dictionary, "deaths")
    nordic_countries_bar(dictionary, "cases")
    nordic_countries_bar(dictionary, "deaths")
    
    
    #for dt in dictionary["Europe"]["Finland"]:
    #    print(dt["countriesAndTerritories"] + "   -    " + dt["dateRep"] + "   -    " + dt[measure])
    

    

def nordic_countries_plot(data, measure):
    
    country_map = {}

    for country in nordic_countries:

        if country not in country_map.keys():
            country_map[country] = {"dates": [], measure: []}
        
        counter = 0

        for datesAndMeasure in data["Europe"][country]:
            
            if counter % 5 == 0:
                country_map[country]["dates"].append(datesAndMeasure["dateRep"])
                country_map[country][measure].append(int(datesAndMeasure[measure]))
            
            counter = counter + 1
        
       
        country_map[country]["dates"] = country_map[country]["dates"][::-1] #reverse list
        country_map[country][measure] = country_map[country][measure][::-1] #reverse list
        

    fig, ax = plt.subplots()
    
    for country in nordic_countries:
        if country == nordic_countries[0]:
            plt.plot("dates", measure, data=country_map[country], label=country)
        else:
            plt.plot(measure, data=country_map[country], label=country)
        
    ax.xaxis.set_tick_params(rotation=90, labelsize=8)
    plt.ylabel("New " + measure)
    plt.title("New " + measure + " / day in Nordic countries")
    plt.legend(fancybox=True, framealpha=1, shadow=True, borderpad=1, loc='upper left', ncol=1, title='Countries')
    plt.show()



def nordic_countries_bar(data, measure):
    
    total_measure_map = {}

    for country in nordic_countries:

        if country not in total_measure_map.keys():
            total_measure_map[country] = 0


        for datesAndMeasure in data["Europe"][country]:
            
            total_measure_map[country] = total_measure_map[country] + int(datesAndMeasure[measure])
        
    y_pos = np.arange(len(nordic_countries))

    height = []

    for key in nordic_countries:
        height.append(total_measure_map[key])

    fig, ax = plt.subplots()
    ax = plt.axes(facecolor='#E6E6E6')
    ax.set_axisbelow(True)
    plt.grid(color='w', linestyle='solid')
    plt.bar(y_pos, height, color=[(0.2, 0.4, 0.6, 0.6), (0.2, 0.4, 0.6, 0.7), (0.2, 0.4, 0.6, 0.8), (0.2, 0.4, 0.6, 0.9), (0.2, 0.4, 0.6, 1.0)])
    
    plt.xticks(y_pos, nordic_countries)

    plt.title('Total number of ' + measure + ' in Nordic Countries')
    plt.show()    



# Dictionary1 nycklar = världsdelar, Dictionary2 nycklar = länder
# ex dictionary["Europe"]["Finland"] = lista med alla Json inlägg för Finland.

def create_structure(data): 

    our_dict = {}

    for element in data['records']: #Ifall ny världsdel skapa en ny dict
        if element["continentExp"] not in our_dict.keys():
            our_dict[element["continentExp"]] = {}

        if element["countriesAndTerritories"] not in our_dict[element["continentExp"]].keys(): #Ifall nytt land skapa en lista för det landet
            our_dict[element["continentExp"]][element["countriesAndTerritories"]] = []

        
        our_dict[element["continentExp"]][element["countriesAndTerritories"]].append(element)


    return our_dict



def load_data(file):
    with open(file, 'r') as f:
        data = json.load(f)
    
    return data



if __name__ == "__main__":
    main()
