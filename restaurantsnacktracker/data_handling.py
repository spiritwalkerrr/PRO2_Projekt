import json
import datetime


# GETS ALL VISITS DATA
def get_visits():
    # open visits database
    file = open("database/visits.JSON")
    # load the data from database
    visits_data = json.load(file)
    # since we always want to display them in the order of most recently added to least recently added we reverse
    visits_data.reverse()
    # return that data
    return visits_data


# GETS THE RESTAURANTS DATA
def get_restaurants():
    # open restaurants database
    file = open("database/restaurants.JSON")
    # load the data from the database
    restaurants_data = json.load(file)
    # return that data
    return restaurants_data


# GETS THE NAME OF A RESTAURANT BY SPECIFIC ID
# parameter restaurant_id is a numerical unique ID
def get_restaurant_name_by_id(restaurant_id):
    # open restaurants database
    file = open("database/restaurants.JSON")
    # load the data from the database
    restaurants_data = json.load(file)
    # loop over all restaurants
    for restaurant in restaurants_data:
        # until a restaurant ID matches
        if restaurant["id"] == restaurant_id:
            # return the name of that restaurant
            return restaurant["name"]


# GETS ALL THE DATA OF A RESTAURANT BY SPECIFIC ID
# parameter restaurant_id is a numerical unique ID
def get_restaurant_by_id(restaurant_id):
    # open restaurants database
    file = open("database/restaurants.JSON")
    # load the data from the database
    restaurants_data = json.load(file)
    for restaurant in restaurants_data:
        # until a restaurant ID matches
        if restaurant["id"] == restaurant_id:
            # return the data of that restaurant
            return restaurant


# GETS THE STATISTICS FOR A RESTAURANT BY SPECIFIC ID
# parameter restaurant_id is a numerical unique ID
def get_restaurant_statistics(restaurant_id):
    # we need all the visits to then calculate the averages, this function gets them
    visits = get_visits()
    # In order to calculate the averages, we need to first set the keys
    # I also set them to 0 in case there are no visits
    statistics = {
        "times_visited": 0,
        "food_avg": 0,
        "service_avg": 0,
        "value_avg": 0,
        "price_avg": 0,
        "wait_avg": 0,
        # this value is actually never displayed, it either gets overwritten or not displayed at all
        # it's basically a dummy value in case a restaurant has no visits
        "last_visit": datetime.date(1900, 1, 1)}
    # next code block initializes some variables
    # we start with 0, so we can add to that and then divide by number of visits to get an average
    food_scores = 0
    service_scores = 0
    value_scores = 0
    price = 0
    wait = 0
    # loop over all visits
    for visit in visits:
        # see if that visit was at the restaurant we are looking to get statistics for
        if visit["restaurant"]["id"] == restaurant_id:
            statistics["times_visited"] = statistics["times_visited"] + 1  # COUNT TIMES VISITED
            food_scores = food_scores + visit["ratings"]["food"]  # ADD UP FOOD SCORES
            service_scores = service_scores + visit["ratings"]["service"]  # ADD UP SERVICE SCORES
            value_scores = value_scores + visit["ratings"]["value"]  # ADD UP VALUE SCORES
            price = price + visit["price"]  # ADD UP PRICES PAID
            wait = wait + visit["wait"]  # ADD UP WAIT TIMES
            # next we split up the date from the visit, so we can compare it later
            # we do this to find out the last visit, requires us to first split it into individual numbers
            date = visit["date"].split("-")
            # take the split numbers and make a datetime.date out of them (for comparison later)
            date = datetime.date(int(date[0]), int(date[1]), int(date[2]))
            # next we check if the last visit was before (this also overwrites the 1900 dummy value from above)
            if date > statistics["last_visit"]:
                # if the visit we are currently evaluating was after the last one saved, we overwrite that
                statistics["last_visit"] = date
    # now we still need to divide the added up values by amount of visits
    # also we use this opportunity to round some values because math isn't always pretty
    # we only do this if we actually have visits for that restaurant, otherwise we keep the 0 values set above
    if statistics["times_visited"] > 0:
        statistics["food_avg"] = round(food_scores / statistics["times_visited"], 2)  # get average and round
        statistics["service_avg"] = round(service_scores / statistics["times_visited"], 2)  # get average and round
        statistics["value_avg"] = round(value_scores / statistics["times_visited"], 2)  # get average and round
        # I don't know anymore why I don't round here - in the words of Todd Howard: "It just works!"
        statistics["price_avg"] = round(price / statistics["times_visited"])
        # I don't know anymore why I don't round here - in the words of Todd Howard: "It just works!"
        statistics["wait_avg"] = round(wait / statistics["times_visited"])
    # now we did the calculating, we can return those juicy statistics
    return statistics


# GETS A NEW RESTAURANT ID
# this is needed if we want to make a new restaurant
# the webapp uses an ID system to identify restaurants, so we need to be able to generate new unique ones
def get_new_restaurant_id():
    # first of all, get all restaurants data
    restaurants = get_restaurants()
    # prepare a list for already in use IDs
    used_ids = []
    # loop over all restaurants
    for restaurant in restaurants:
        # add those used IDs into the list we prepared
        used_ids.append(restaurant["id"])
    # start a new ID with 0
    new_id = 0
    # loop and increase new ID by 1 until there is no match in used_ids
    while new_id in used_ids:
        new_id = new_id + 1
    # return ID
    return new_id


# CREATES A NEW RESTAURANT ENTRY
# parameter new_id is the ID under which the restaurant should be saved
# parameter data is the data we use to create an entry (comes from a form)
def create_new_restaurant(new_id, data):
    # get the list of restaurants we have, so we can append the new one later
    restaurants_data = get_restaurants()
    # make a new restaurant dictionary using new_id and the data from the form
    new_restaurant = {
        "id": new_id,  # new ID
        "name": data["name"],  # name of the created restaurant
        "address": data["address"],  # address of the created restaurant
        "code": int(data["code"]),  # postal code as integer of the created restaurant
        "town": data["town"],  # town of the created restaurant
        "cuisine": data["cuisine"]  # type of cuisine of the  created restaurant
    }
    # add the new restaurant dictionary to the existing list of restaurants
    restaurants_data.append(new_restaurant)
    # this function saves that list in the database
    save_restaurants(restaurants_data)
    # return probably not needed but I think it's elegant
    return


# GETS DATA OF ONE VISIT BY SPECIFIC ID
# parameter visit_id is the visit's ID (surprising, right?)
def get_visit_by_id(visit_id):
    # we get the all visits list because we need to loop over them
    visits_data = get_visits()
    # loop over all visits
    for visit in visits_data:
        # see if ID matches
        if visit["id"] == visit_id:
            # return matching visit data
            return visit


# CREATES A NEW VISIT; REQUIRES AN ID AND THE DATA FROM THE FORM
# parameter new_id is a new unique identifier
# parameter data is the data we use to create a new entry
def create_new_visit(new_id, data):
    # get all visits so we can add to that
    visits_data = get_visits()
    # we know the restaurant ID from data, now we need to find the restaurant
    restaurant_name = get_restaurant_name_by_id(int(data["restaurant"]))
    # create a new visit dictionary to append to the list of visits
    # using a sub-dictionary at the key "restaurant" is cool I guess but caused more work than it's worth
    new_visit = {
        "id": new_id,  # assign newly generated ID
        "restaurant":
            {
                "id": int(data["restaurant"]),  # assign restaurant ID from form (as integer)
                "name": restaurant_name  # assign restaurant name from form
            },
        "date": data["date"],  # assign the date from form
        "dish": data["dish"],  # assign the dish from form
        "drink": data["drink"],  # assign the drink from form
        "price": int(data["price"]),  # assign the price from form (as integer)
        "wait": int(data["wait"]),  # assign the wait time from form (as integer)
        "ratings": {  # assign the ratings from the form (as integers)
            "food": int(data["rating_food"]),  # food rating
            "service": int(data["rating_service"]),  # service rating
            "value": int(data["rating_value"])  # value rating
            }
    }
    # append the new visit dictionary to the list of visits
    visits_data.append(new_visit)
    # save to database
    save_visits(visits_data)
    # return probably not needed but I think it's elegant
    return


# GETS A NEW UNIQUE VISIT ID
def get_new_visit_id():
    # first we get all visits in a list
    visits = get_visits()
    # prepare a list of used IDs
    used_ids = []
    # loop over all visits
    for visit in visits:
        # add their IDs to used_ids
        used_ids.append(visit["id"])
    # start a new ID with 0
    new_id = 0
    # while loop and increase by 1 until new ID doesn't match one from used_ids
    while new_id in used_ids:
        new_id = new_id + 1
    # return that new ID
    return new_id


# GETS ALL VISITS OF A CERTAIN RESTAURANT
# parameter restaurant_id is the unique identifier of the restaurant
def get_visits_by_restaurant_id(restaurant_id):
    # get all visits
    visits = get_visits()
    # prepare a fresh empty list for the visits
    restaurant_visits = []
    # loop over all visits
    for visit in visits:
        # see if the visit is for the restaurant we look for
        if visit["restaurant"]["id"] == restaurant_id:
            # if it does match, append to the list we made
            restaurant_visits.append(visit)
    # List is in wrong order, we want recently added entries to be shown first
    # return the list of visits we just generated
    return restaurant_visits


# DELETES A VISIT WITH A SPECIFIC ID
# parameter visit_id is the unique visit ID
def delete_existing_visit(visit_id):
    # prepare a new list of visits
    visits_data = []
    # get the list of all currently existing vistis
    visits = get_visits()
    # loop over list of visits
    for visit in visits:
        # if the ID does NOT match the one we want to delete
        if visit_id != visit["id"]:
            # append that visit (which we don't want to delete) to visits_data
            visits_data.append(visit)
    # save the new visits list
    save_visits(visits_data)
    # return probably not needed but I think it's elegant
    return


# DELETES A RESTAURANT AND ITS VISITS
# parameter restaurant_id is the numeric identifier ID
# this does the same as above except for restaurants instead of visits. Won't add comments therefore
def delete_restaurant_by_id(restaurant_id):
    delete_visits_by_restaurant_id(restaurant_id)
    restaurants = get_restaurants()
    restaurants_data = []
    for restaurant in restaurants:
        if restaurant["id"] != restaurant_id:
            restaurants_data.append(restaurant)
    save_restaurants(restaurants_data)
    return


# EDITS A RESTAURANT AND THE VISITS (RESTAURANT NAME)
# parameter restaurant_id is the restaurants numeric identifier
# data is the new restaurant data received from the form
# the challenge here is that we need to not only update the restaurant, but also it's visits
# reason for that is that the visits also store the restaurant name
# could be solved more elegantly, but it works
def edit_restaurant_by_id(restaurant_id, data):
    # we get the current list of visits because we'll update it at the end
    visits = get_visits()
    # prepare the new visits list
    visits_data = []
    # loop over existing visits
    for visit in visits:
        # see if restaurant ID matches the restaurant ID of a visit
        if visit["restaurant"]["id"] == restaurant_id:
            # set the new name
            # we don't need to update ID as it doesn't change
            visit["restaurant"]["name"] = data["name"]
        # append each visit to the new visits list (both the ones we edited and the ones we didn't)
        # this keeps the order as it was
        visits_data.append(visit)
    # save the visits list
    save_visits(visits_data)
    # now we need to handle the restaurant update
    # first we get all restaurants in a list
    restaurants = get_restaurants()
    # then we prepare a fresh empty list for the updated restaurants list
    restaurants_data = []
    # loop over the currently existing restaurants
    for restaurant in restaurants:
        # see if the ID matches the ID of the restaurant we just edited
        if restaurant["id"] == restaurant_id:
            # if it does, we change the restaurant data to the updated info
            restaurant["name"] = data["name"]
            restaurant["address"] = data["address"]
            restaurant["code"] = data["code"]
            restaurant["town"] = data["town"]
            restaurant["cuisine"] = data["cuisine"]
        # append the restaurant to the new restaurants list (wheter it was edited or not)
        restaurants_data.append(restaurant)
    # save the restaurants data
    save_restaurants(restaurants_data)
    # return probably not needed but I think it's elegant
    return


# DELETE ALL VISITS OF A CERTAIN RESTAURANT
# parameter restaurant_id is the ID of the restaurant we want to delete all visits for
# this function is needed because if we delete a restaurant, it should also delete all visits to it
def delete_visits_by_restaurant_id(restaurant_id):
    # first we get all visits as a list
    visits = get_visits()
    # then we create a new list for the updated visits
    visits_data = []
    # loop over the existing visits
    for visit in visits:
        # see if the visit's restaurant ID does NOT match the restaurant ID we want to delete
        if visit["restaurant"]["id"] != restaurant_id:
            # if it doesn't match append to the new list, so we keep that entry
            visits_data.append(visit)
    # save the visits data
    save_visits(visits_data)
    # return probably not needed but I think it's elegant
    return


# EDITS AN EXISTING VISIT
# parameter visit_id is the ID of the visit we want to edit
# parameter data is the new data for that visit
def edit_existing_visit(visit_id, data):
    # first we delete the visit from the database using its ID
    delete_existing_visit(visit_id)
    # then we create a new visit using the same ID and the new data
    create_new_visit(visit_id, data)
    # return probably not needed but I think it's elegant
    return


# GETS A LIST OF THE RESTAURANTS LAST VISITED IN ORDER
def get_visits_ranking():
    # if we want to rank visits, we need to get the visits first (what we do here)
    visits = get_visits()
    # create a fresh new list for the ranking
    ranking = []
    # loop over the visits
    for visit in visits:
        # initialize a temporary list for later use
        temp = []
        # first we split the date into the three numbers
        date = visit["date"].split("-")
        # now we can use that to create a datetime.date
        # we need to do this because datetime lets us use sorted()
        date = datetime.date(int(date[0]), int(date[1]), int(date[2]))
        # append the date to the temporary list
        temp.append(date)
        # append the visit ID to the temporary list
        temp.append(visit["id"])
        # append the temporary list to the list of rankings
        ranking.append(temp)
    # now we have a list of lists, where the first index of each sublist is the date
    # this lets us use sorted() to rank by date
    ranking = sorted(ranking)
    # however, that list starts with the oldest date, so we reverse it to fit our needs
    ranking.reverse()
    # we loop over the ranking list
    for entry in ranking:
        # not sure anymore why this is needed but to quote Todd Howard again: "It just works!"
        entry[0] = str(entry[0])
        # now we replace the visit ID in the ranking with the actual visit data
        # this is because we want to display some of that data, not the ID
        entry[1] = get_visit_by_id(entry[1])
    # return the list of rankings but shorten it to length 3, as we only do top 3
    return ranking[:3]


# GETS A LIST OF THE BEST FOOD RESTAURANTS
def get_food_ranking():
    # get all restaurants so we can loop over them
    restaurants = get_restaurants()
    # create a new empty list for food rankings
    food_ranking = []
    # loop over all restaurants
    for restaurant in restaurants:
        # get the statistics we calculated using this function as we need some of them
        statistics = get_restaurant_statistics(restaurant["id"])
        # create a new list of food stats (later gets appended to the food_ranking list
        food_stats = [
            statistics["food_avg"],  # needed to display average food score
            restaurant["id"],  # needed for the "Zum Restaurant" button (so we can link there)
            statistics["times_visited"],  # needed to display the times visited
            restaurant["name"],  # needed to display the name of the restaurant
            statistics["wait_avg"]  # needed to display average wait time
        ]
        # all of that only makes sense if there even are visits, so we check if visits != 0
        if food_stats[2] != 0:
            # basically if a restaurant has visits we add it to the ranking
            food_ranking.append(food_stats)
        # now we have a list of all the food rankings as sublists, but its unsorted
        # each sublist intentionally starts with the food avg, so we can sort by that
        food_ranking = sorted(food_ranking)
        # again its in ascending order, but we want descending, so we reverse
        food_ranking.reverse()
        # now the data is almost ready.
        # this little loop only loops over food rankings
        # we use the for x in because we need the X as a count of how many times we looped
    for x in range(len(food_ranking)):
        # this basically turns the restaurant name from e.g. "Hu Xin" to "1. Hu Xin" (# depends on position in ranking)
        food_ranking[x][3] = str(x + 1) + ". " + food_ranking[x][3]
    # now we also get the value ranking, we start by making a list for it
    value_ranking = []
    # loop over the restaurants
    for restaurant in restaurants:
        # get the statistics
        statistics = get_restaurant_statistics(restaurant["id"])
        # set these stats (not going into details this time)
        # important is we start with the value_avg to sort by that later
        value_stats = [
            statistics["value_avg"],
            restaurant["id"],
            statistics["times_visited"],
            restaurant["name"],
            statistics["price_avg"]
        ]
        # check if that restaurant even has visits
        if value_stats[2] != 0:
            # if it does append to the value_ranking list
            value_ranking.append(value_stats)
        # sort value ranking list by value avg (first index in sublist)
        value_ranking = sorted(value_ranking)
        # reverse because its ascending and we want descending
        value_ranking.reverse()
    # loop x times, where x is the ranking length to again adjust the name with the position
    for x in range(len(value_ranking)):
        # this basically turns for example "Hu Xin" into "1. Hu Xin"
        value_ranking[x][3] = str(x + 1) + ". " + value_ranking[x][3]
    # now we return both rankings shortened to three (we only do top 3)
    return food_ranking[:3], value_ranking[:3]


# UPDATES THE VISITS JSON WITH THE PROVIDED DATA
def save_visits(data):
    # makes JSON out of the list of dictionaries we give it
    json_string = json.dumps(data)
    # opens the database file
    file = open("database/visits.JSON", "w")
    # updates the file
    file.write(json_string)
    # closes the file
    file.close()
    # return we probably don't need
    return


# UPDATES THE RESTAURANTS JSON WITH THE PROVIDED DATA
# does basically the exact same as right above except for restaurants
def save_restaurants(data):
    json_string = json.dumps(data)
    file = open("database/restaurants.JSON", "w")
    file.write(json_string)
    file.close()
    return
