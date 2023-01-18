from flask import Flask,  request, redirect
from flask import render_template
from data_handling import get_visits, get_restaurants, create_new_visit, get_restaurant_name_by_id, get_new_visit_id, \
    delete_existing_visit, get_visit_by_id, edit_existing_visit, get_restaurant_by_id, get_restaurant_statistics, \
    get_new_restaurant_id, create_new_restaurant, delete_restaurant_by_id, edit_restaurant_by_id, get_visits_ranking, \
    get_food_ranking, get_visits_by_restaurant_id

app = Flask("RestaurantSnackTracker")

# HOW THIS FILE IS STRUCTURED 1. I like to keep my routes short. Therefore, most of the handling is done in
# data_handling.py 2. First all the routes related to restaurants are shown, then all the routes related to visits 3.
# Lastly we have the homepage ("/") and before that some error handling code in case someone decided to type in a
# nonsensical URL


# this route is used to delete a restaurant with a given restaurant ID
@app.route("/restaurant/delete/<restaurant_id>")
# get restaurant ID from URL
def delete_restaurant(restaurant_id):
    # deletes the restaurant, takes a numerical ID value as parameter
    delete_restaurant_by_id(int(restaurant_id))
    # redirect to the restaurants overview
    return redirect("/restaurants")


# this route is used to edit a restaurant's data
@app.route("/restaurant/edit/<restaurant_id>", methods=["GET", "POST"])
# get restaurant ID from URL
def edit_restaurant(restaurant_id):
    # since we display the form here, we need the GET request to serve that template
    if request.method == "GET":
        # Displaying the restaurant information in the form requires us to get the restaurant information in the
        # first place, this function gets us that by taking the numerical restaurant ID as a parameter
        restaurant = get_restaurant_by_id(int(restaurant_id))
        # now we have the restaurant info, so we pass it through for the form and serve the template
        return render_template("edit_restaurant.html", restaurant=restaurant)
        # POST request is needed to handle the editing
    if request.method == "POST":
        # makes ugly request into beautiful dictionary
        new_values = request.form.to_dict()
        # To edit the restaurant, we need to both get its ID and the new (edited) information.
        # The ID we get from the URL, the new values we get from the dictionary we just made
        edit_restaurant_by_id(int(restaurant_id), new_values)
        # redirect to the restaurant we just edited
        return redirect("/restaurant/" + str(restaurant_id))


# this route is used to create a new restaurant for the database
@app.route("/restaurant/new", methods=["GET", "POST"])
def new_restaurant():
    # GET method is needed to display the form required to add new restaurant
    if request.method == "GET":
        # this just serves the template with the form
        return render_template("new_restaurant.html")
        # this is where the magic happens - POST request needed to
    if request.method == "POST":
        # makes ugly request into beautiful dictionary
        new_values = request.form.to_dict()
        # first we generate the new restaurant ID, so we can use it for the redirect and creation of database entry
        new_id = get_new_restaurant_id()
        # Adds a new restaurant to the database. To do that we need the new values and the ID.
        create_new_restaurant(new_id, new_values)
        # redirect to the restaurant we just edited
        return redirect("/restaurant/" + str(new_id))


# this route displays one of the restaurants identified by its ID
@app.route("/restaurant/<restaurant_id>")
# here we get the restaurant ID from the URL
def show_restaurant(restaurant_id):
    # to display the restaurant data we need the restaurant data - this function gets that
    # parameter is just the ID made into an integer
    restaurant = get_restaurant_by_id(int(restaurant_id))
    # Since we can also compare restaurants with the displayed restaurants we need to get the names from the others.
    # they then get put into the dropdown selector
    restaurants = get_restaurants()
    # the page also displays some useful statistics. to get them we call this function, parameter is the ID as usual
    statistics = get_restaurant_statistics(int(restaurant_id))
    # we also want to display the visits for that restaurant, so we get those with this function
    visits = get_visits_by_restaurant_id(int(restaurant_id))
    # Now we have the restaurant, the restaurants, the restaurant visits, and the statistics
    # serve the render template and pass through all that data
    return render_template("restaurant.html", restaurant=restaurant, statistics=statistics, restaurants=restaurants,
                           visits=visits)


# this route shows us a comparison between two restaurants based on some values about them
# POST request because this loads upon sending the form on a single restaurant's page
@app.route("/restaurants/compare/<restaurant_id>", methods=["POST"])
# here we get the restaurant ID from the URL
def compare_restaurants(restaurant_id):
    # so to compare two restaurants we need two IDs. First one comes from the URL
    id_1 = int(restaurant_id)
    # second one comes by taking the ugly request and making it into a beautiful dictionary
    id_2 = int(request.form.to_dict()["restaurant"])
    # so this basically takes the ID and returns us a list of restaurant info and restaurant statistics
    restaurant_1 = [get_restaurant_by_id(id_1), get_restaurant_statistics(id_1)]
    # same as above but for the other restaurant
    restaurant_2 = [get_restaurant_by_id(id_2), get_restaurant_statistics(id_2)]
    # now to display that info & the statistics we serve the template and pass through both restaurants details
    return render_template("/compare.html", restaurant_1=restaurant_1, restaurant_2=restaurant_2)


# this just displays the restaurants overview
@app.route("/restaurants")
def show_restaurants():
    # gets the restaurants data
    restaurants = get_restaurants()
    # serves render template and passes through the restaurants data
    return render_template("restaurants.html", restaurants=restaurants)


# this route is used to display a single visit's edit form and also handles the actual edit POST request
@app.route("/visit/edit/<visit_id>", methods=["GET", "POST"])
# we need the visit ID, here it is
def edit_visit(visit_id):
    # GET request to display the form
    if request.method == "GET":
        # since I like to display the current info I need that info first
        # this function gets the visit data by the visit ID
        visit = get_visit_by_id(int(visit_id))
        # we need all the restaurants as well in case we want to assign a new restaurant
        # the restaurant names go into the dropdown, this function gets the names (and more)
        restaurants = get_restaurants()
        # serve render template and pass through visit and restaurants info
        return render_template("edit_visit.html", restaurants=restaurants, visit=visit)
    # POST request handles the actual editing of the visit
    if request.method == "POST":
        # makes ugly request into beautiful dictionary
        new_values = request.form.to_dict()
        # this function overwrites previous values of a visit by ID with the new ones
        edit_existing_visit(int(visit_id), new_values)
        # Late addition: redirect to the visit's restaurant
        # added this so users can instantly see when they edit from a restaurant's "Besuch bearbeiten" button
        return redirect("/restaurant/" + str(new_values["restaurant"]))


# So we can edit visits (see above) but we also need to make new ones. That's what we do here.
# However, it's not so easy. Create isn't just create in this case. This route adds a visit to a SPECIFIC restaurant
# there will be another route that lets you create a new visit and also CHOOSE a restaurant
# notice the "restaurant_id" in the URL? We need it because this new visit is assigned to a specific restaurant
@app.route("/visit/add/<restaurant_id>", methods=["GET", "POST"])
def add_visit(restaurant_id):
    # GET request handles the display of the "add new visit" form
    if request.method == "GET":
        # we need the restaurant name for the h1 on the page, so we can display it there
        restaurant = get_restaurant_name_by_id(int(restaurant_id))
        # serves the render template, passing through restaurant (for the name display)
        # also passes through restaurant ID because it's needed for an invisible input on the form
        # this way the user can't change it (easily) but it also allows us to identify the restaurant in the request
        return render_template("add_visit.html", restaurant=restaurant, id=restaurant_id)
    # POST request handles saving the data from the form
    if request.method == "POST":
        # make ugly request into beautiful dictionary
        new_values = request.form.to_dict()
        # this function creates a new visit, parameters are a new unique visit ID and the new values
        # Visit ID is generated by a function
        create_new_visit(get_new_visit_id(), new_values)
        # redirect to the specific restaurant where we added the entry to
        return redirect("/restaurant" + "/" + restaurant_id)


# This route creates a new visit using a provided form
# unlike above we don't need a restaurant ID because the user can choose the restaurant
@app.route("/visit/new", methods=["GET", "POST"])
def new_visit():
    # GET request for displaying the form
    if request.method == "GET":
        # to select a restaurant, we need a list of them. this function get it
        restaurants = get_restaurants()
        # late addition here. The user should not be able to create a new visit, if there are no restaurants.
        # hence we get the length of the restaurants list, we can use that to display information if there are none.
        restaurants_amount = len(restaurants)
        # serves render template with restaurant names
        return render_template("new_visit.html", restaurants=restaurants, amount=restaurants_amount)
    # POST request takes form data and saves a new visit
    if request.method == "POST":
        # make ugly request into beautiful dictionary
        new_values = request.form.to_dict()
        # this function creates a new visit, parameters are a new unique visit ID and the new values
        # Visit ID is generated by a function
        create_new_visit(get_new_visit_id(), new_values)
        return redirect("/visits")


# So: we can add, but we also want to delete. this route handles that
@app.route("/visit/delete/<visit_id>")
# get visit ID from URL
def delete_visit(visit_id):
    # this function purges that visit from existence. bye bye.
    delete_existing_visit(int(visit_id))
    # redirect to visits overview
    return redirect("/visits")


# Late in the project I added the functionality to display visit lists for the restaurants individually
# this route is needed for when a visit is deleted whilst being on a specific restaurant page
# in that case we want to redirect to that restaurant when we're done.
@app.route("/restaurant/<restaurant_id>/delete/<visit_id>")
# get visit ID and restaurant ID from URL
def delete_visit_and_return(visit_id, restaurant_id):
    # this function purges that visit from existence. bye bye.
    delete_existing_visit(int(visit_id))
    # redirect to the restaurant we were just looking at
    return redirect("/restaurant/" + str(restaurant_id))


# this route displays all visits.
@app.route('/visits')
def show_visits():
    # gets all visits
    visits = get_visits()
    # serves render template passing through those visits
    return render_template("visits.html", visits=visits)


# last but not least we also need to display the landing page
@app.route('/')
def show_index():
    # to show a (visits) ranking, we need to get that ranking using this function
    visits_ranking = get_visits_ranking()
    # to show a (restaurants) ranking, we need to get that ranking using this function
    restaurant_ranking = get_food_ranking()
    # serves template with the rankings info to display
    return render_template("index.html", visits_ranking=visits_ranking, restaurant_ranking=restaurant_ranking)


# error handling in case someone decides to go to /admin or sth
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    # serves template and displays path because why not
    return render_template("error.html", path=path)


# the glue that holds it all together
if __name__ == "__main__":
    app.run(debug=True, port=3000)
