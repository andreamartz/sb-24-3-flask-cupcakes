"""Flask app for Cupcakes"""

from flask import Flask, request, jsonify, render_template
# from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, Cupcake
from forms import AddCupcakeForm

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "oh-so-secret"

connect_db(app)
# db.create_all()

# Having the Debug Toolbar show redirects explicitly is often useful;
# however, if you want to turn it off, you can uncomment this line:
#
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

# toolbar = DebugToolbarExtension(app)


@app.errorhandler(404)
def page_not_found(error):
    """Handle 404 errors by showing custom 404 page."""

    return render_template('404.html'), 404


@app.route("/")
def root():
    """Render homepage."""

    form = AddCupcakeForm()
    return render_template("index.html", form=form)


@app.route('/api/cupcakes', methods=["GET"])
def list_cupcakes():
    """Show info about all cupcakes."""

    all_cupcakes = [cupcake.serialize() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes=all_cupcakes)


@app.route('/api/cupcakes/<int:cupcake_id>', methods=["GET"])
def get_cupcake(cupcake_id):
    """Show info about a single cupcake"""

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    return jsonify(cupcake=cupcake.serialize())


@app.route('/api/cupcakes', methods=["POST"])
def create_cupcake():
    """Add cupcake, and return data about new cupcake.

    Returns JSON like:
        {cupcake: [{id, flavor, rating, size, image}]}
    """

    # It would be best to do error handling for when a user does not pass in all the required fields,
    # but for now we're keeping this simple.
    try:
        new_cupcake = Cupcake(
            flavor=request.json["flavor"],
            size=request.json["size"],
            rating=request.json["rating"],
            image=request.json.get("image", None)
        )
        db.session.add(new_cupcake)
        db.session.commit()
        response_json = jsonify(cupcake=new_cupcake.serialize())
        return (response_json, 201)
    except:
        response_json = jsonify(
            message="A required field is missing. Please try again.")
        # return render_template('index.html')
        # what status code should I include?
        return (response_json)


