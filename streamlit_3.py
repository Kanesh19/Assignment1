import streamlit as st
import pandas as pd
import pymysql
from dataset_1 import Datas

data_set = Datas()


mydb = pymysql.connect(
    host="localhost",
    user="root",
    password="MySQL123@",
    database="zomatto")
mycursor = mydb.cursor()


r = st.sidebar.radio('Navigation',['Home', 'CRUD', 'Query'])
st.sidebar.title("Zomato Data Insight")


if r == 'Home':
    st.title("Zomato Data Insight")
    H_pg = st.selectbox('Select table', ['Customer','Restaurant', 'Order', 'Delivery'])
    if H_pg == "Customer":
        customer_data = data_set.customer_table()
        st.subheader("Customer Table")
        st.dataframe(customer_data)
    elif H_pg == "Restaurant":
        restaurant_data = data_set.restaurant_table()
        st.subheader("Restaurant Table")
        st.dataframe(restaurant_data)
    elif H_pg == "Order":
        order_data = data_set.order_table()
        st.subheader("Order Table")
        st.dataframe(order_data)
    elif H_pg == "Delivery":
        delivery_data = data_set.delivery_table()
        st.subheader("Delivery Table")
        st.dataframe(delivery_data)


if r == 'CRUD':
    st.title("CRUD operation")
    option = st.sidebar.selectbox("Select Operation",['CREATE', 'READ', 'DELETE'])

    if option == 'CREATE':
        st.subheader("Create Table")
        s = st.selectbox("Select table", ['customer_table', 'restaurant_table', 'order_table', 'delivery_table'])

        if s == 'customer_table':
            customer_id = st.text_input("Enter Customer ID")
            name = st.text_input("Enter Name")
            email = st.text_input("Enter Email")
            if st.button("Create"):
                sql = "INSERT INTO customer_table(customer_id, name, email) VALUES(%s, %s, %s)"
                val = (customer_id, name, email)
                mycursor.execute(sql, val)
                mydb.commit()
                st.success("Created Successfully")

        elif s == 'restaurant_table':
            restaurant_id = st.text_input("Enter Restaurant ID")
            name = st.text_input("Enter Name")
            if st.button("Create"):
                sql = "INSERT INTO restaurant_table(restaurant_id, name) VALUES(%s, %s)"
                val = (restaurant_id, name)
                mycursor.execute(sql, val)
                mydb.commit()
                st.success("Created Successfully")

        elif s == 'order_table':
            order_id = st.text_input("Enter Order ID")
            status = st.text_input("Enter Status")
            if st.button("Create"):
                sql = "INSERT INTO order_table(order_id, status) VALUES(%s, %s)"
                val = (order_id, status)
                mycursor.execute(sql, val)
                mydb.commit()
                st.success("Created Successfully")

        elif s == 'delivery_table':
            delivery_id = st.text_input("Enter Delivery ID")
            delivery_status = st.text_input("Enter Delivery Status")
            if st.button("Create"):
                sql = "INSERT INTO delivery_table(delivery_id, delivery_status) VALUES(%s, %s)"
                val = (delivery_id, delivery_status)
                mycursor.execute(sql, val)
                mydb.commit()
                st.success("Created Successfully")

        query = f"SELECT * FROM {s}"
        mycursor.execute(query)
        result = mycursor.fetchall()
        columns = [i[0] for i in mycursor.description]

        df = pd.DataFrame(result, columns=columns)
        st.subheader(f"New {s} Data")
        st.dataframe(df)
 

    elif option == 'READ':
        st.subheader("Read Table Data")
        t = st.selectbox("Select table", ['customer_table', 'restaurant_table', 'order_table', 'delivery_table'])
        query = f"select * from {t}"
        mycursor.execute(query)
        result = mycursor.fetchall()
        columns = [i[0] for i in mycursor.description]
        
        df= pd.DataFrame(result, columns=columns)
        st.dataframe(df)


    elif option == 'DELETE':
        st.subheader("Delete Record from Table")

        u = st.selectbox("Select table", ['customer_table', 'restaurant_table', 'order_table', 'delivery_table'])

        id_column = {
            'customer_table': 'customer_id',
            'restaurant_table': 'restaurant_id',
            'order_table': 'order_id',
            'delivery_table': 'delivery_id'
        }
        id_value = st.number_input(f"Enter {id_column[u]} to Delete", min_value=1, step=1)

        if st.button("Delete"):
            try:
                sql = f"DELETE FROM {u} WHERE {id_column[u]} = %s"
                mycursor.execute(sql, (id_value,))
                mydb.commit()
                st.success("Record Deleted Successfully")

                mycursor.execute(f"SELECT * FROM {u}")
                result = mycursor.fetchall()
                columns = [i[0] for i in mycursor.description]
                df = pd.DataFrame(result, columns=columns)

                st.subheader(f"Updated {u} Data")
                st.dataframe(df)

            except pymysql.Error as err:
                st.error(f"Error: {err}")

        

if r == 'Query':
    queries = [
        "SELECT COUNT(*) FROM ZOMATO.customer_table WHERE signup_date BETWEEN '01-10-2024' AND '31-01-2025'",
        "SELECT * FROM ZOMATO.customer_table WHERE is_premium = 1",
        "SELECT * FROM ZOMATO.customer_table WHERE total_orders > 70",
        "SELECT COUNT(*) FROM ZOMATO.customer_table WHERE preferred_cuisine ='Italy'",
        "SELECT * FROM ZOMATO.customer_table WHERE average_rating > 4.5",
        "SELECT * FROM ZOMATO.restaurant_table WHERE cuisine_type = 'Italy'",
        "SELECT * FROM ZOMATO.restaurant_table WHERE average_delivery_time <50",
        "SELECT COUNT(*) FROM ZOMATO.restaurant_table WHERE rating > 4",
        "SELECT COUNT(*) FROM ZOMATO.restaurant_table WHERE total_orders BETWEEN 700 AND 1000",
        "SELECT * FROM ZOMATO.restaurant_table WHERE is_active = 1",
        "SELECT * FROM ZOMATO.order_table WHERE order_date BETWEEN '01-07-2024' AND '31-01-2025'",
        "SELECT * FROM ZOMATO.order_table WHERE status = 'Delivered'",
        "SELECT COUNT(*) FROM ZOMATO.order_table WHERE total_amount >4000",
        "SELECT * FROM ZOMATO.order_table WHERE payment_mode = 'Credit Card'",
        "SELECT COUNT(*) FROM ZOMATO.order_table WHERE discount_applied > 15 ",
        "SELECT COUNT(*) FROM ZOMATO.order_table WHERE feedback_rating BETWEEN 3.5 AND 5",
        "SELECT * FROM ZOMATO.delivery_table WHERE delivery_status ='Delivered'",
        "SELECT * FROM ZOMATO.delivery_table WHERE distance > 3.5",
        "SELECT * FROM ZOMATO.delivery_table WHERE delivery_fee > 500",
        "SELECT COUNT(*) FROM ZOMATO.delivery_table WHERE vehicle_type = 'Bike'"
    ]
    query_title = ["signup date of last 4 month","premium customers","customers with max orders","customers preferred italy cuisine","customers with high rating",
                   "no.of famous italy cuisine restaurant","average delivery time","restaurant max rating","orders btwn 1000 & 700","active restaurant",
                   "orders btwn 1-7-24 & 31-1-25","delivered orders","order amount > 4000","payment via credit card","orders with more than 15 discount",
                   "great feedback rating","deliverd orders","distance more than 3.5 km","delivery fee more than 500", "delivery by bike"]
    select_query = st.selectbox("select a query",query_title)
    if select_query == "signup date of last 4 month":
        mycursor.execute(queries[0])
        data_set = mycursor.fetchall()
        df = pd.read_sql(queries[0], mydb)
        st.dataframe(df)
    elif select_query == "premium customers":
        mycursor.execute(queries[1])
        data_set = mycursor.fetchall()
        df = pd.read_sql(queries[1], mydb)
        st.dataframe(df)
    elif select_query == "customers with max orders":
        mycursor.execute(queries[2])
        data_set = mycursor.fetchall()
        df = pd.read_sql(queries[2], mydb)
        st.dataframe(df)
    elif select_query == "customers preferred italy cuisine":
        mycursor.execute(queries[3])
        data_set = mycursor.fetchall()
        df = pd.read_sql(queries[3], mydb)
        st.dataframe(df)
    elif select_query == "customers with high rating":
        mycursor.execute(queries[4])
        data_set = mycursor.fetchall()
        df = pd.read_sql(queries[4], mydb)
        st.dataframe(df)
    elif select_query == "no.of famous italy cuisine restaurant":
        mycursor.execute(queries[5])
        data_set = mycursor.fetchall()
        df = pd.read_sql(queries[5], mydb)
        st.dataframe(df)
    elif select_query == "average delivery time":
        mycursor.execute(queries[6])
        data_set = mycursor.fetchall()
        df = pd.read_sql(queries[6], mydb)
        st.dataframe(df)
    elif select_query == "restaurant max rating":
        mycursor.execute(queries[7])
        data_set = mycursor.fetchall()
        df = pd.read_sql(queries[7], mydb)
        st.dataframe(df)
    elif select_query == "orders btwn 1000 & 700":
        mycursor.execute(queries[8])
        data_set = mycursor.fetchall()
        df = pd.read_sql(queries[8], mydb)
        st.dataframe(df)
    elif select_query == "active restaurant":
        mycursor.execute(queries[9])
        data_set = mycursor.fetchall()
        df = pd.read_sql(queries[9], mydb)
        st.dataframe(df)
    elif select_query == "orders btwn 1-7-24 & 31-1-25":
        mycursor.execute(queries[10])
        data_set = mycursor.fetchall()
        df = pd.read_sql(queries[10], mydb)
        st.dataframe(df)
    elif select_query == "delivered orders":
        mycursor.execute(queries[11])
        data_set = mycursor.fetchall()
        df = pd.read_sql(queries[11], mydb)
        st.dataframe(df)
    elif select_query == "order amount > 4000":
        mycursor.execute(queries[12])
        data_set = mycursor.fetchall()
        df = pd.read_sql(queries[12], mydb)
        st.dataframe(df)
    elif select_query == "payment via credit card":
        mycursor.execute(queries[13])
        data_set = mycursor.fetchall()
        df = pd.read_sql(queries[13], mydb)
        st.dataframe(df)
    elif select_query == "orders with more than 15 discount":
        mycursor.execute(queries[14])
        data_set = mycursor.fetchall()
        df = pd.read_sql(queries[14], mydb)
        st.dataframe(df)
    elif select_query == "great feedback rating":
        mycursor.execute(queries[15])
        data_set = mycursor.fetchall()
        df = pd.read_sql(queries[15], mydb)
        st.dataframe(df)
    elif select_query == "deliverd orders":
        mycursor.execute(queries[16])
        data_set = mycursor.fetchall()
        df = pd.read_sql(queries[16], mydb)
        st.dataframe(df)
    elif select_query == "distance more than 3.5 km":
        mycursor.execute(queries[17])
        data_set = mycursor.fetchall()
        df = pd.read_sql(queries[17], mydb)
        st.dataframe(df)
    elif select_query == "delivery fee more than 500":
        mycursor.execute(queries[18])
        data_set = mycursor.fetchall()
        df = pd.read_sql(queries[18], mydb)
        st.dataframe(df)
    elif select_query == "delivery by bike":
        mycursor.execute(queries[19])
        data_set = mycursor.fetchall()
        df = pd.read_sql(queries[19], mydb)
        st.dataframe(df)