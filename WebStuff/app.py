from flask import Flask,request,render_template
from DigiScore import main

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Get the input value from the HTML form
        input_value = request.form.get("input_field")
        # Call your main function with the input value
        result = main(input_value)
        # Return the result to the HTML page
        return render_template("result.html", result=result)
    # If the request method is GET, return the HTML form
    return render_template("index.html")
