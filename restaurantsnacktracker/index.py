from flask import Flask,  request, redirect
from flask import render_template
from data_handling import get_visits, get_restaurants, create_new_visit, get_restaurant_name_by_id, get_new_visit_id, \
    delete_existing_visit, get_visit_by_id, edit_existing_visit, get_restaurant_by_id, get_restaurant_statistics, get_new_restaurant_id, create_new_restaurant, delete_restaurant_by_id, edit_restaurant_by_id, get_visits_ranking, get_food_ranking

app = Flask("RestaurantSnackTracker")

get_food_ranking()


@app.route("/restaurant/delete/<visit_id>")
def delete_restaurant(visit_id):
    delete_restaurant_by_id(int(visit_id))
    return redirect("/restaurants")


@app.route("/restaurant/edit/<restaurant_id>", methods=["GET", "POST"])
def edit_restaurant(restaurant_id):
    if request.method == "GET":
        restaurant = get_restaurant_by_id(int(restaurant_id))
        return render_template("edit_restaurant.html", restaurant=restaurant)
    if request.method == "POST":
        new_values = request.form.to_dict()
        edit_restaurant_by_id(int(restaurant_id), new_values)
        return redirect("/restaurants")


@app.route("/restaurant/new", methods=["GET", "POST"])
def new_restaurant():
    if request.method == "GET":
        return render_template("new_restaurant.html")
    if request.method == "POST":
        new_values = request.form.to_dict()
        create_new_restaurant(get_new_restaurant_id(), new_values)
        return redirect("/restaurants")


@app.route("/restaurant/<visit_id>")
def show_restaurant(visit_id):
    restaurant = get_restaurant_by_id(int(visit_id))
    restaurants = get_restaurants()
    statistics = get_restaurant_statistics(int(visit_id))
    return render_template("restaurant.html", restaurant=restaurant, statistics=statistics, restaurants=restaurants)


@app.route("/restaurants/compare/<visit_id>", methods=["POST"])
def compare_restaurants(visit_id):
    id_1 = int(visit_id)
    id_2 = int(request.form.to_dict()["restaurant"])
    restaurant_1 = [get_restaurant_by_id(id_1), get_restaurant_statistics(id_1)]
    restaurant_2 = [get_restaurant_by_id(id_2), get_restaurant_statistics(id_2)]
    return render_template("/compare.html", restaurant_1=restaurant_1, restaurant_2=restaurant_2)


@app.route("/restaurants")
def show_restaurants():
    restaurants = get_restaurants()
    return render_template("restaurants.html", restaurants=restaurants)


@app.route("/visit/edit/<visit_id>", methods=["GET", "POST"])
def edit_visit(visit_id):
    if request.method == "GET":
        visit = get_visit_by_id(int(visit_id))
        restaurants = get_restaurants()
        return render_template("edit_visit.html", restaurants=restaurants, visit=visit)
    if request.method == "POST":
        new_values = request.form.to_dict()
        edit_existing_visit(visit_id, new_values)
        return redirect("/visits")


@app.route("/visit/add/<visit_id>", methods=["GET", "POST"])
def add_visit(visit_id):
    if request.method == "GET":
        restaurant = get_restaurant_name_by_id(int(visit_id))
        return render_template("add_visit.html", restaurant=restaurant, id=visit_id)
    if request.method == "POST":
        new_values = request.form.to_dict()
        create_new_visit(get_new_visit_id(), new_values)
        return redirect("/visits")


@app.route("/visit/new", methods=["GET", "POST"])
def new_visit():
    if request.method == "GET":
        restaurants = get_restaurants()
        return render_template("new_visit.html", restaurants=restaurants)
    if request.method == "POST":
        new_values = request.form.to_dict()
        create_new_visit(get_new_visit_id(), new_values)
        return redirect("/visits")


@app.route("/visit/delete/<visit_id>")
def delete_visit(visit_id):
    delete_existing_visit(int(visit_id))
    return redirect("/visits")


@app.route('/visits')
def show_visits():
    visits = get_visits()
    return render_template("visits.html", visits=visits)


@app.route("/")
def show_index():
    visits_ranking = get_visits_ranking()
    restaurant_ranking = get_food_ranking()
    return render_template("index.html", visits_ranking=visits_ranking, restaurant_ranking=restaurant_ranking)


if __name__ == "__main__":
    app.run(debug=True, port=3000)
