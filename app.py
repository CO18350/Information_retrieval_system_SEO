from searching import *
from flask import Flask, render_template, request
from flask import jsonify

app = Flask(__name__)

@app.route('/', methods=["GET","POST"])
def search():
    if request.method == "GET":
        clear_search()
        return render_template("search.html")
    else:
        sentence = request.form.get("sentence")
        page = int(request.form.get("page"))

        sentence = sentence.lower()

        op = main(sentence, page)
        return render_template("display.html",data=op,page=page,key=sentence)

if __name__ == '__main__':
    app.run(debug=True)