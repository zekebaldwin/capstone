from flask import Flask, render_template, redirect, session, flash, json, jsonify, request
import requests
from models import connect_db, db, User, Drink
from forms import LoginForm, RegisterForm, SearchForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///capstone"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "shhhhh"
connect_db(app)


@app.route("/")
def base():
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if "username" in session:
        return redirect("/search")
        
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.authenticate(username, password)
        if user: 
            session['username'] = user.username
            return redirect('/search')
            
        else:
            form.username.errors = ['invalid']
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        if User.query.filter(User.username == username).first():
            flash('Username Taken')
        else:
            user = User.register(username, password)
            db.session.commit()
            session['username'] = user.username
            return redirect('/search')
    return render_template('register.html', form=form)

@app.route('/random')
def random():
    url = "https://the-cocktail-db.p.rapidapi.com/randomselection.php"

    headers = {
	"X-RapidAPI-Key": "03717fdd31mshb1d00b9a7391513p1c188fjsn508c2f258506",
	"X-RapidAPI-Host": "the-cocktail-db.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers)
    json = response.json()
    drinks = json['drinks']
    drink_1_name = drinks[0]['strDrink']
    drink_1_img = drinks[0]['strDrinkThumb']
    drink_2_name = drinks[1]['strDrink']
    drink_2_img = drinks[1]['strDrinkThumb']
    drink_3_name = drinks[2]['strDrink']
    drink_3_img = drinks[2]['strDrinkThumb']
    drink_4_name = drinks[3]['strDrink']
    drink_4_img = drinks[3]['strDrinkThumb']
    drink_5_name = drinks[4]['strDrink']
    drink_5_img = drinks[4]['strDrinkThumb']
    drink_6_name = drinks[5]['strDrink']
    drink_6_img = drinks[5]['strDrinkThumb']
    drink_7_name = drinks[6]['strDrink']
    drink_7_img = drinks[6]['strDrinkThumb']
    drink_8_name = drinks[7]['strDrink']
    drink_8_img = drinks[7]['strDrinkThumb']
    drink_9_name = drinks[8]['strDrink']
    drink_9_img = drinks[8]['strDrinkThumb']
    drink_10_name = drinks[9]['strDrink']
    drink_10_img = drinks[9]['strDrinkThumb']
    return render_template('home.html', 
    drink_1_name=drink_1_name, drink_1_img=drink_1_img, drink_2_name=drink_2_name, drink_2_img= drink_2_img, drink_3_name=drink_3_name, drink_3_img= drink_3_img, drink_4_name=drink_4_name, drink_4_img= drink_4_img,drink_5_name=drink_5_name, drink_5_img= drink_5_img, drink_6_name=drink_6_name, drink_6_img= drink_6_img, drink_7_name=drink_7_name, drink_7_img= drink_7_img, drink_8_name=drink_8_name, drink_8_img= drink_8_img, drink_9_name=drink_9_name, drink_9_img= drink_9_img, drink_10_name=drink_10_name,drink_10_img=drink_10_img)

@app.route('/search', methods=['GET','POST'])
def search():
    form = SearchForm()
    url = "https://the-cocktail-db.p.rapidapi.com/search.php"
    if form.validate_on_submit():
        query = form.query.data
        querystring = {"s":f"{query}"}
        headers = {
	    "X-RapidAPI-Key": "03717fdd31mshb1d00b9a7391513p1c188fjsn508c2f258506",
	    "X-RapidAPI-Host": "the-cocktail-db.p.rapidapi.com"
        }
        response = requests.request("GET", url, headers=headers, params=querystring)
        responses = response.json()
        name = responses['drinks'][0]
        ingrediants = {}
        for k, v in name.items():
            if (k == 'strIngredient1' and v != None) or (k == 'strIngredient2' and v != None) or (k == 'strIngredient3' and v != None) or (k == 'strIngredient4' and v != None) or (k == 'strIngredient5' and v != None) or (k == 'strIngredient6' and v != None) or (k == 'strIngredient7' and v != None) or (k == 'strIngredient8' and v != None) or (k == 'strIngredient9' and v != None) or (k == 'strIngredient10' and v != None) or (k == 'strIngredient11' and v != None) or (k == 'strIngredient12' and v != None) or (k == 'strIngredient13' and v != None) or (k == 'strIngredient14' and v != None) or (k == 'strIngredient15'and v != None):
                ingrediants[k] = v 
        instructions = name['strInstructions']
        image = name['strDrinkThumb']
        drink_id = name['idDrink']
        drink_name = name['strDrink']
        return render_template('show.html', name=name, instructions=instructions, image=image, ingrediants=ingrediants, drink_id=drink_id, drink_name=drink_name)
    return render_template('search.html', form=form)

@app.route('/favorites', methods=['GET','POST'])
def favorites():
    username = session['username']
    if request.method == 'POST':
        value = request.form.get('drink')
        if Drink.query.filter(Drink.drink_name == value, Drink.username == username).first():
            return redirect('/favorites')
        else:
            new_drink = Drink(drink_name=f'{value}', username=username)
            db.session.add(new_drink)
            db.session.commit()
    else:
        drinks = Drink.query.filter_by(username=username).all()
        return render_template("favorites.html", drinks=drinks)
    drinks = Drink.query.filter_by(username=username).all()
    return render_template("favorites.html", value=value, drinks=drinks)

@app.route('/favorites/<drink>')
def display_drink(drink):
    url = "https://the-cocktail-db.p.rapidapi.com/search.php"

    querystring = {"s":f"{drink}"}

    headers = {
	"X-RapidAPI-Key": "03717fdd31mshb1d00b9a7391513p1c188fjsn508c2f258506",
	"X-RapidAPI-Host": "the-cocktail-db.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    responses = response.json()
    name = responses['drinks'][0]
    instructions = name['strInstructions']
    image = name['strDrinkThumb']
    drink_id = name['idDrink']
    drink_name = name['strDrink']
    return render_template('drinks.html', instructions=instructions, image=image, drink_id=drink_id, drink_name=drink_name)

@app.route('/delete', methods=['GET', 'POST'])
def delete():
    username = session['username']
    if request.method == 'POST':
        value = request.form.get('drink')
        delete = Drink.query.filter(Drink.drink_name == value, Drink.username == username).first()
        db.session.delete(delete)
        db.session.commit()
    return redirect('/favorites')

@app.route('/logout')
def logout():
    session.pop("username")
    return redirect("/login")
