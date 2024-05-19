import psycopg2

#connect to database

con=psycopg2.connect(
    user="postgres",
    dbname="myduka",
    password="IloveK3!2024",
    port="5432",
    host="localhost"
)

#open a cursor to perform database operation
curr=con.cursor()

# def get_product():
#     curr.execute("SELECT * FROM product;")
#     prods=curr.fetchall()
#     print(prods)

# get_product("sales")
# get_product("product")
#write a function to get sales ,
# insert data

def get_data(table_name):
    curr.execute(f"SELECT * FROM {table_name};")
    data=curr.fetchall()
    return data

def insert_products(values):
    insert="insert into products (name,buying_price,selling_price,stock_quantity)values(%s,%s,%s,%s)"
    curr.execute(insert,values)   
    con.commit()


# product_values=("tilapia",200,500,8)    
# insert_products(product_values)

# get_data("sales")

def insert_sales(values):
    sales="insert into sales (pid,quantity,created_at)values(%s,%s,now())"
    curr.execute(sales,values)   
    con.commit() 

# sale_values=(1,30,)    
# insert_sales(sale_values)
# get_data('sales')

def profits():
    profits ="select name,sum((selling_price-buying_price)*quantity) from products join sales on products.id=sales.pid group by name;"
    curr.execute(profits)
    data=curr.fetchall()
    return data
 
profits()

def profit_day():
    profit="select date(sales.created_at)as sales_date,sum((selling_price-buying_price)*quantity)as profits from products join sales on sales.pid=products.id group by sales_date order by sales_date ASC;"  
    curr.execute(profit)
    data=curr.fetchall()
    return data

profit_day()

def sales_product():
    query= "select p.name,sum(quantity*selling_price)as total_sales_per_product from products as p join sales on sales.pid=p.id group by p.name;"
    curr.execute(query)
    data=curr.fetchall()
    return data

def sales_day():
    query= "select date(sales.created_at)as sales_date,sum(selling_price*quantity)as profits from products join sales on sales.pid=products.id group by sales_date order by sales_date ASC;" 
    curr.execute(query)
    data=curr.fetchall()
    return data 

sales_day()

#define a function to insert users
def insert_user(values):
    insert=" insert  into users(full_name,email,password)values(%s,%s,%s);"
    curr.execute(insert,values)   
    con.commit()

#in the register route get for data from register form.

def check_email(email):
    query='select * from users where email=%s'
    curr.execute(query,(email,))
    data=curr.fetchone()
    return data

def confirm_email_password(email, password):
    query='select * from users where email=%s and password=%s'
    curr.execute(query,(email,password,))
    data=curr.fetchall()
    return data





 









 



    
