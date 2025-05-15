from flask import Flask, render_template, request

from models import db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db.init_app(app)

with app.app_context():
    db.create_all()


'''
{
    "key": "value,
    "key2": "value2"
}
'''

@app.route('/')
def hello_world():
    return {"message": 'Hello, World!'}

@app.route('/hello/<name>')
def hello(name):
    return {"message": f'Hello, {name}!'}
    
'''@app.route('/page1')
def page1():
    return render_template('page1.html')'''

@app.route('/page2')
def page2():
    backend_name = 'prokriti'
    # return render_template('page2.html', frontend_name=backend_name)
    return {"frontend_name":backend_name}

@app.route('/page2/<path_name>')
def page2_path(path_name):
    backend_name = path_name
    return render_template('page2.html', frontend_name=backend_name)

@app.route('/page3', methods=["GET", "POST"])
def page3():
    if request.method == "POST":
        backend_name = request.form['name']
        return render_template('page3.html', frontend_name=backend_name)
    return render_template('page3.html', frontend_name=backend_name)

@app.route('/page4', methods=["GET", "POST"])
def page4():
    if request.method == "POST":
        backend_name = request.json['name']
        backend_age = request.json['age']
        if backend_age:
            backend_age = int(backend_age)
        else:
            backend_age = 0
        new_user = User(name=backend_name, age=backend_age)
        db.session.add(new_user)
        db.session.commit()
        return {"frontend_name":backend_name, "frontend_age":backend_age}
        # return render_template('page4.html', frontend_name=backend_name, frontend_age=backend_age)
    return {"frontend_name":"", "frontend_age":0}

if __name__ == "__main__":
    app.run(debug=True)
