#importing the flask class
from flask import Flask ,render_template,request,redirect,url_for,flash,session
from database import get_data,insert_products,insert_sales,profits,profit_day,sales_product,sales_day,insert_user,check_email,confirm_email_password

#creating flask instance
app=Flask(__name__)
app.secret_key='bxsjhxbvwkhxjsjhkxshkxj'
#route

@app.route("/")
def hello():
    return render_template("index.html")

@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/products")
def products():
    if "email" not in session:
        flash("login to access this page")
        return redirect (url_for("login"))
    products=get_data("products")
    return render_template("products.html",products=products)

@app.route("/login",methods=["POST","GET"])
def login():
    if request.method=="POST":
    #get form data
        email=request.form["email"]
        password=request.form["password"]
    #check if email exist
        ck_email=check_email(email)

        if ck_email==None:
                flash("email does not exist")
                return redirect(url_for("register"))
        else:
            #compare email and password
                check_password=confirm_email_password(email,password)
                if len(check_password)<1:
                    flash("invalid email and password")
                else:
                    session["email"]=email

                    flash("Login successful")
                    return redirect(url_for("dashboard"))
    return render_template("login.html")

@app.route("/register" ,methods=["POST","GET"])
def register():
    #get form data
    if request.method=="POST":
        f_name=request.form["full_name"]
        email=request.form["email"]
        pwd=request.form["password"]
        #check email
        c_email=check_email(email)

        if c_email==None:
            new_user=(f_name,email,pwd)
            insert_user(new_user)
            flash("registration successful")
            return redirect(url_for("login"))
        else:
            flash("email already exist use a different email or login")
    return render_template("register.html")

    



#add products from a form
@app.route("/add_products" ,methods=["POST","GET"])
def add_prod():
    p_name=request.form["Product Name"]
    b_price=request.form["Buying Price"]
    s_price=request.form["Selling Price"]
    s_quantity=request.form["Stock Quantity"]

    new_prods=(p_name,b_price,s_price,s_quantity)
    insert_products(new_prods)
    return  redirect(url_for("products"))

#inserting from d


@app.route("/sales")
def sales():
    if "email" not in session:
        flash("login to access this page")
        return redirect (url_for("login"))
    sales=get_data("sales")
    products=get_data("products")
    return render_template("sales.html",sales=sales, products=products)

#making a sale
@app.route("/make_sales",methods=["POST","GET"])
def make_sale():
    pid=request.form["pid"]
    quantity=request.form["quantity"]
    new_sales=(pid,quantity)
    insert_sales(new_sales)
    return redirect(url_for("sales"))

@app.route("/dashboard")
def dashboard():
    if "email" not in session:
        flash("login to access this page")
        return redirect (url_for("login"))
    
    pr_profit=profits()
    p_name=[]
    p_profit=[]

    for i in pr_profit:
        p_name.append(i[0])
        p_profit.append(float(i[1]))

    day_profit=profit_day()  

    dates=[]
    date_profit=[]

    for i in day_profit:
        dates.append(str(i[0]))
        date_profit.append(float(i[1]))

    sa_sales=sales_product()
    print(sa_sales)
    pr_name=[]
    quantity=[] 

    for i in sa_sales:
        quantity.append(float(i[1]))

    da_sales=sales_day() 
    
    dates_sales=[] 

    for i in da_sales:
        
        dates_sales.append(float(i[1]))
    

    return render_template("dashboard.html",p_name=p_name,p_profit=p_profit,dates=dates,date_profit=date_profit,pr_name=pr_name,quantity=quantity,dates_sales=dates_sales)

#log out
@app.route("/logout")
def logout():
     #remove the email from the session
    session.pop("email",None)
    flash("You are logged out,login")
    return redirect(url_for("login"))


if __name__== "__main__":

    app.run(debug=True)

