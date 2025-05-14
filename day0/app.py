from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/hello/<name>')
def hello(name):
    return f'Hello, {name}!'
    
@app.route('/page1')
def page1():
    return render_template('page1.html')

@app.route('/page2')
def page2():
    backend_name = 'prokriti'
    return render_template('page2.html', frontend_name=backend_name)

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

if __name__ == "__main__":
    app.run(debug=True)
