from flask import Flask,render_template,redirect,url_for,request
from flask_sqlalchemy import SQLAlchemy

# create the extension
db = SQLAlchemy()
# create the app
app = Flask(__name__)
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////Users/METEHAN/Desktop/flasktodo/todo.db"
# initialize the app with the extension
db.init_app(app)

@app.route("/")
def index():
    todos = Todo.query.all() #veri tabanından bütün verileri çekti
    return render_template("index.html", todos=todos) 

@app.route("/add",methods = ["POST"]) #submit edilen değeri almak için
def addTodo():
    title = request.form.get("title")
    newTodo = Todo(title = title,complete = False)
    db.session.add(newTodo) #verileri ekliyor.
    db.session.commit() #verileri işliyor.

    return redirect(url_for("index"))

@app.route("/complete/<string:id>") #
def complateTodo(id):
    todo = Todo.query.filter_by(id=id).first() #gelen id ile ayn olan veriyi veri tabanından çek demek
    # if todo.complete == True:
    #     todo.complete = False
    # else:
    #     todo.complate = True
    todo.complete = not todo.complete
    db.session.commit() #değişiklik yaptık yapıtığımız değişiklikleri işlemek için
    return redirect(url_for("index"))

@app.route("/delete/<string:id>")
def deleteTodo(id):
    todo = Todo.query.filter_by(id=id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("index"))



class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    complete = db.Column(db.Boolean)

if __name__ == "__main__":
    with app.app_context():
        db.create_all() #Veri tabanına tabloyu uygulama çalışmadan oluşturuyor.
    app.run(debug=True)

