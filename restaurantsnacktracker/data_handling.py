from csv import reader
import json
import datetime


# GETS VISITS DATA
def get_visits():
    file = open("visits.JSON")
    visits_data = json.load(file)
    return visits_data


# GETS THE NAME OF A RESTAURANT BY SPECIFIC ID
def get_restaurant_name_by_id(id):
    file = open("restaurants.JSON")
    restaurants_data = json.load(file)
    for restaurant in restaurants_data:
        if restaurant["id"] == id:
            return restaurant["name"]


# GETS ALL THE DATA OF A RESTAURANT BY SPECIFIC ID
def get_restaurant_by_id(id):
    file = open("restaurants.JSON")
    restaurants_data = json.load(file)
    for restaurant in restaurants_data:
        if restaurant["id"] == id:
            return restaurant


# GETS THE STATISTICS FOR A RESTAURANT BY SPECIFIC ID
def get_restaurant_statistics(id):
    visits = get_visits()
    statistics = {
        "times_visited": 0,
        "food_avg": 0,
        "service_avg": 0,
        "value_avg": 0,
        "price_avg": 0,
        "wait_avg": 0,
        "last_visit": datetime.date(1900, 1, 1)}  # DUMMY VALUE WILL NEVER BE DISPLAYED
    food_scores = 0
    service_scores = 0
    value_scores = 0
    price = 0
    wait = 0
    for visit in visits:
        if visit["restaurant"]["id"] == id:
            statistics["times_visited"] = statistics["times_visited"] + 1  # COUNT TIMES VISITED
            food_scores = food_scores + visit["ratings"]["food"]  # COUNT UP FOOD SCORES
            service_scores = service_scores + visit["ratings"]["service"]  # COUNT UP SERVICE SCORES
            value_scores = value_scores + visit["ratings"]["value"]  # COUNT UP VALUE SCORES
            price = price + visit["price"]
            wait = wait + visit["wait"]
            date = visit["date"].split("-")  # GET THE DATE OF THAT VISIT AND SPLIT IT FOR datetime.date
            date = datetime.date(int(date[0]), int(date[1]), int(date[2]))  # MAKE IT INTO A datetime.date
            if date > statistics["last_visit"]:  # COMPARE IF IT IS LARGER THAN LAST VISIT
                statistics["last_visit"] = date  # SET AS LAST VISIT IF IT IS
    if statistics["times_visited"] > 0:  # GET AVERAGE IF VISITS > 0
        statistics["food_avg"] = round(food_scores / statistics["times_visited"], 2)
        statistics["service_avg"] = round(service_scores / statistics["times_visited"], 2)
        statistics["value_avg"] = round(value_scores / statistics["times_visited"], 2)
        statistics["price_avg"] = round(price / statistics["times_visited"])
        statistics["wait_avg"] = round(wait / statistics["times_visited"])
    return statistics


# GETS A NEW RESTAURANT ID
def get_new_restaurant_id():
    restaurants = get_restaurants()
    used_ids = []
    for restaurant in restaurants:
        used_ids.append(restaurant["id"])
    new_id = 0;
    while new_id in used_ids:
        new_id = new_id + 1
    return new_id


# CREATES A NEW RESTAURANT ENTRY
def create_new_restaurant(id, data):
    file = open("restaurants.JSON")
    restaurants_data = json.load(file)
    new_restaurant = {
        "id": id,
        "name": data["name"],
        "address": data["address"],
        "code": int(data["code"]),
        "town": data["town"],
        "cuisine": data["cuisine"]
    }
    restaurants_data.append(new_restaurant)
    save_restaurants(restaurants_data)
    return


# GETS DATA ON ONE VISIT BY SPECIFIC ID
def get_visit_by_id(id):
    file = open("visits.JSON")
    visits_data = json.load(file)
    for visit in visits_data:
        if visit["id"] == id:
            return visit;


# GETS THE RESTAURANTS DATA
def get_restaurants():
    file = open("restaurants.JSON")
    restaurants_data = json.load(file)
    return restaurants_data


# CREATES A NEW VISIT; REQUIRES AN ID (USE get_new_visit_id) AND THE DATA FROM THE FORM
def create_new_visit(id, data):
    file = open("visits.JSON")
    visits_data = json.load(file)
    restaurant_name = get_restaurant_name_by_id(int(data["restaurant"]))
    new_visit = {
            "id": id,
            "restaurant":
                {
                    "id": int(data["restaurant"]),
                    "name": restaurant_name
                },
            "date": data["date"],
            "dish": data["dish"],
            "drink": data["drink"],
            "price": int(data["price"]),
            "wait": int(data["wait"]),
            "ratings": {
                "food": int(data["rating_food"]),
                "service": int(data["rating_service"]),
                "value": int(data["rating_value"])
            }
    }
    visits_data.append(new_visit)
    save_visits(visits_data)
    return


# GETS A NEW UNIQUE VISIT ID
def get_new_visit_id():
    visits = get_visits()
    used_ids = []
    for visit in visits:
        used_ids.append(visit["id"])
    new_id = 0;
    while new_id in used_ids:
        new_id = new_id + 1
    return new_id


# DELETES A VISIT WITH A SPECIFIC ID
def delete_existing_visit(visit_id):
    visit_id = int(visit_id)
    visits_data = []
    visits = get_visits()
    for visit in visits:
        if visit_id != visit["id"]:
            visits_data.append(visit)
    save_visits(visits_data)
    return


# DELETES A RESTAURANT AND ITS VISITS
def delete_restaurant_by_id(id):
    delete_visits_by_restaurant_id(id)
    restaurants = get_restaurants()
    restaurants_data = []
    for restaurant in restaurants:
        if restaurant["id"] != id:
            restaurants_data.append(restaurant)
    save_restaurants(restaurants_data)
    return


# EDITS A RESTAURANT AND THE VISITS (RESTAURANT NAME)
def edit_restaurant_by_id(id, data):
    new_name = data["name"]
    visits = get_visits()
    visits_data = []  # FIRST WE CHANGE THE VISITS BECAUSE THE ALSO CONTAIN THE NAME
    for visit in visits:
        if visit["restaurant"]["id"] == id:
            visit["restaurant"]["name"] = new_name
        visits_data.append(visit)
    save_visits(visits_data)  # SAVE THE UPDATED VISITS
    restaurants = get_restaurants()
    restaurants_data = []  # NEXT WE CHANGE THE RESTAURANT NAME
    for restaurant in restaurants:
        if restaurant["id"] == id:
            restaurant["name"] = new_name
        restaurants_data.append(restaurant)
    save_restaurants(restaurants_data)  # SAVE THE UPDATED RESTAURANT
    return data


# DELETE ALL VISITS OF A CERTAIN RESTAURANT
def delete_visits_by_restaurant_id(id):
    visits = get_visits()
    visits_data = []
    for visit in visits:
        if visit["restaurant"]["id"] != id:
            visits_data.append(visit)
    save_visits(visits_data)
    return


# EDITS AN EXISTING VISIT
def edit_existing_visit(id, data):
    id = int(id)
    delete_existing_visit(id)
    create_new_visit(id, data)
    return


# UPDATES THE VISITS JSON WITH THE PROVIDED DATA
def save_visits(data):
    json_string = json.dumps(data)
    file = open("visits.JSON", "w")
    file.write(json_string)
    file.close
    return


# UPDATES THE RESTAURANTS JSON WITH THE PROVIDED DATA
def save_restaurants(data):
    json_string = json.dumps(data)
    file = open("restaurants.JSON", "w")
    file.write(json_string)
    file.close
    return


# GETS A LIST OF THE RESTAURANTS VISITED IN ORDER
def get_visits_ranking():
    visits = get_visits()
    ranking = []
    for visit in visits:
        temp = []
        date = visit["date"].split("-")  # GET THE DATE OF THAT VISIT AND SPLIT IT FOR datetime.date
        date = datetime.date(int(date[0]), int(date[1]), int(date[2]))  # MAKE IT INTO A datetime.date
        temp.append(date)
        temp.append(visit["id"])
        ranking.append(temp)
    ranking = sorted(ranking)
    ranking.reverse()
    for entry in ranking:
        entry[0] = str(entry[0])
        entry[1] = get_visit_by_id(entry[1])
    return ranking[:3]


# GETS A LIST OF THE BEST FOOD RESTAURANTS
def get_food_ranking():
    restaurants = get_restaurants()
    food_ranking = []  # FIRST WE GET THE FOOD RANKING
    for restaurant in restaurants:
        statistics = get_restaurant_statistics(restaurant["id"])
        food_stats = [
            statistics["food_avg"],
            restaurant["id"],
            statistics["times_visited"],
            restaurant["name"],
            statistics["wait_avg"]
        ]
        if food_stats[2] != 0:
            food_ranking.append(food_stats)
        food_ranking = sorted(food_ranking)
        food_ranking.reverse()
    for x in range(len(food_ranking)):
        food_ranking[x][3] = str(x + 1) + ". " + food_ranking[x][3]
    value_ranking = []  # THEN WE GET THE VALUE RANKING
    for restaurant in restaurants:
        statistics = get_restaurant_statistics(restaurant["id"])
        value_stats = [
            statistics["value_avg"],
            restaurant["id"],
            statistics["times_visited"],
            restaurant["name"],
            statistics["price_avg"]
        ]
        if value_stats[2] != 0:
            value_ranking.append(value_stats)
        value_ranking = sorted(value_ranking)
        value_ranking.reverse()
    for x in range(len(value_ranking)):
        value_ranking[x][3] = str(x + 1) + ". " + value_ranking[x][3]

    return food_ranking[:3], value_ranking[:3]
