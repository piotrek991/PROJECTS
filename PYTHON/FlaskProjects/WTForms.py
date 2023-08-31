
from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField
from wtforms.validators import DataRequired,Email,Length
import email_validator



class LoginForm(FlaskForm):
    email = EmailField(label = 'Email', validators=[DataRequired(),Email(check_deliverability=True)])
    password = PasswordField(label ='Password',validators=[DataRequired(),Length(min = 8)])
    submit = SubmitField(label="Log In")


app = Flask(__name__)
app.secret_key = "secret"


@app.route("/")
def home():
    return render_template("./templates_wtforms/index.html")


@app.route("/login",methods = ["POST","GET"])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        if login_form.email.data == "admin@email.com" and login_form.password.data == "12345678":
            return render_template("./templates_wtforms/success.html")
        else:
            return render_template("./templates_wtforms/denied.html")
    return render_template('./templates_wtforms/login.html', form=login_form)


if __name__ == '__main__':
    app.run(debug=True)