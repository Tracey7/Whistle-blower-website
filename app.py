from flask import Flask,render_template,url_for,request,redirect,session,flash
from flask_bcrypt import generate_password_hash,check_password_hash
from config import User,Mymessage

app = Flask(__name__)
app.secret_key="ujujtliuhoik"


@app.route('/',methods=["POST","GET"])
def home():  # put application's code here
    if request.method == "POST":
        email = request.form['u_email']
        password = request.form['u_pass']
        try:
            user = User.get(User.email == email)
            hashed_password = user.password
            if check_password_hash(hashed_password, password):
                session['is_active'] = True
                session["is_authenticated"] = True
                flash("Login successful")
                return redirect(url_for("index"))

            else:
                flash("Wrong email or password")
        except:
            flash("login not permitted")
    return render_template('home.html')


@app.route('/about',methods=["POST","GET"])
def about():  # put application's code here
    return render_template('about.html')
@app.route('/index',methods=["POST","GET"])
def index():  # put application's code here
    return render_template('index.html')


@app.route('/services',methods=["POST","GET"])
def services():  # put application's code here
    return render_template('services.html')


@app.route('/contact',methods=["POST","GET"])
def contact():  # put application's code here
    if not session.get("is_active"):
        return redirect(url_for("home"))
    if request.method == "POST":
        kampuni = request.form["u_organization"]
        idara = request.form["u_department"]
        ujumbe = request.form["u_anonymous"]
        Mymessage.create(organization=kampuni, department=idara, anonymous=ujumbe)
        return redirect(url_for('contact'))

    return render_template('contact.html')




@app.route('/messages',methods=["POST","GET"])
def messages():# put application's code here
    mymessages = Mymessage.select()
    if not session.get("is_active"):
        return redirect(url_for("home"))
    return render_template('messages.html', mymessages=mymessages)





#@app.route('/login.html',methods=["POST","GET"])
#def login():  # put application's code here

 #   return render_template("login.html")



@app.route('/signup',methods=["POST","GET"])
def signup():  # put application's code here
    if request.method == "POST":
        jina = request.form['u_name']
        arafa = request.form['u_email']
        siri = request.form['u_pass']
        siri = generate_password_hash(siri)
        User.create(name=jina, email=arafa, password=siri)
        flash('registration successful')
        return redirect(url_for('index'))
    return render_template('signup.html')



@app.route('/users')
def users():
    if not session.get("is_active"):
        return redirect(url_for("index"))

    users = User.select()
    return render_template('users.html',users=users)

@app.route('/delete/<int:id>')
def delete(id):
    if session.get("is_active")!= True:
        return redirect(url_for("home"))
    User.delete().where(User.id == id).execute()
    flash("User deleted successfully")

    return redirect(url_for("users"))


@app.route('/update/<int:id>', methods=["GET","POST"])
def update(id):
    if session.get("is_active")!= True:
        return redirect(url_for("home"))
    user=User.get(User.id == id)
    if request.method=="POST":
        updatedName = request.form["u_name"]
        updatedEmail = request.form["u_email"]
        updatedPassword = request.form["u_pass"]
        user.name=updatedName
        user.email = updatedEmail
        user.password = updatedPassword
        user.password=generate_password_hash(updatedPassword)
        user.save()
        flash("User updated successfully")
        return redirect(url_for("users"))

    return render_template('update.html',user=user)



if __name__ == '__main__':
    app.run(debug=True)
