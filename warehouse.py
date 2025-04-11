from flask import Flask, render_template, request, redirect
import mysql.connector
import matplotlib.pyplot as plt
import os

app = Flask(__name__)

# Connect to MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="warehouse_db"
)
cursor = db.cursor(dictionary=True)

# Knapsack logic (profit per unit space)
def fractional_knapsack(capacity, items):
    items = [item for item in items if item["value"] > 0]
    items.sort(key=lambda x: x["weight"] / x["value"], reverse=True)
    total_profit = 0
    selected = []

    for item in items:
        if capacity >= item["value"]:
            selected.append({**item, "fraction": 1})
            capacity -= item["value"]
            total_profit += item["weight"]
        else:
            fraction = capacity / item["value"]
            selected.append({
                "name": item["name"],
                "value": capacity,
                "weight": item["weight"] * fraction,
                "fraction": round(fraction, 2)
            })
            total_profit += item["weight"] * fraction
            break

    return selected, total_profit

# Generate pie chart
def generate_pie_chart(selected_items):
    if not os.path.exists("static"):
        os.makedirs("static")

    labels = [item["name"] for item in selected_items]
    sizes = [item["value"] for item in selected_items]

    plt.figure(figsize=(6, 6))
    plt.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=140)
    plt.title("Storage Allocation")
    plt.savefig("static/storage_chart.png")
    plt.close()

# Home route
@app.route("/")
def home():
    cursor.execute("SELECT * FROM inventory")
    items = cursor.fetchall()  #fetches all the items form the database

    cursor.execute("SELECT max_capacity FROM config WHERE id = 1")
    result = cursor.fetchone()              #Gets max storage capacity from config table.
    capacity = result["max_capacity"] if result else 0          #Safely sets capacity to 0 if config is missing.

    return render_template("index.html", inventory=items, max_capacity=capacity)

# Set max capacity
@app.route("/set_capacity", methods=["POST"])
def set_capacity():
    capacity = int(request.form["max_capacity"])            #Gets capacity value from the form.
    cursor.execute("UPDATE config SET max_capacity = %s WHERE id = 1", (capacity,))
    db.commit()                                               #Updates it in the database.
    return redirect("/")                 #Redirects to homepage.

# Add item
@app.route("/add_item", methods=["POST"])
def add_item():
    name = request.form["item_name"]
    value = int(request.form["value"])
    weight = int(request.form["weight"])
    cursor.execute("INSERT INTO inventory (name, value, weight) VALUES (%s, %s, %s)", (name, value, weight))
    db.commit()
    return redirect("/")

# Delete item
@app.route("/delete/<int:index>")
def delete_item(index):
    cursor.execute("DELETE FROM inventory WHERE id = %s", (index,))
    db.commit()
    return redirect("/")

# Edit item
@app.route("/edit/<int:item_id>")
def edit_item(item_id):
    cursor.execute("SELECT * FROM inventory WHERE id = %s", (item_id,))
    item = cursor.fetchone()
    return render_template("edit_item.html", item=item)

# Update item
@app.route("/update_item/<int:item_id>", methods=["POST"])
def update_item(item_id):
    name = request.form["item_name"]
    value = int(request.form["value"])
    weight = int(request.form["weight"])
    cursor.execute(
        "UPDATE inventory SET name = %s, value = %s, weight = %s WHERE id = %s",
        (name, value, weight, item_id)
    )
    db.commit()
    return redirect("/")

# Calculate knapsack and show result on a separate page
@app.route("/calculate_knapsack", methods=["POST"])
def calculate_knapsack():
    cursor.execute("SELECT * FROM inventory")
    items = cursor.fetchall()

    cursor.execute("SELECT max_capacity FROM config WHERE id = 1")
    result = cursor.fetchone()
    capacity = result["max_capacity"] if result else 0

    selected_items, total_profit = fractional_knapsack(capacity, items)
    generate_pie_chart(selected_items)

    return render_template(
        "knapsack_result.html",
        selected_items=selected_items,
        total_profit=round(total_profit, 2)
    )

if __name__ == "__main__":
    app.run(debug=True)
