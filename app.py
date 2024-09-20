from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recipes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Recipes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    ingredients = db.Column(db.Text, nullable=False)
    instructions = db.Column(db.Text, nullable=False)

@app.route('/')
def index():
    recipes = Recipes.query.all()
    return render_template('index.html', recipes=recipes)

@app.route('/add', methods=('GET', 'POST'))
def add_recipe():
    if request.method == 'POST':
        title = request.form['title']
        ingredients = request.form['ingredients']
        instructions = request.form['instructions']

        new_recipe = Recipes(title=title, ingredients=ingredients, instructions=instructions)
        db.session.add(new_recipe)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('add_recipe.html')

@app.route('/edit/<int:id>', methods=('GET', 'POST'))
def edit_recipe(id):
    recipe = Recipes.query.get_or_404(id)

    if request.method == 'POST':
        recipe.title = request.form['title']
        recipe.ingredients = request.form['ingredients']
        recipe.instructions = request.form['instructions']

        db.session.commit()
        return redirect(url_for('index'))

    return render_template('edit_recipe.html', recipe=recipe)

@app.route('/delete/<int:id>', methods=('POST',))
def delete_recipe(id):
    recipe = Recipes.query.get_or_404(id)
    db.session.delete(recipe)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)