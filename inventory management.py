import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import mysql.connector

# Connect to MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="varsha@12345",  
    database="inventory"
)
if db.is_connected():
    print("connection successfull")

cursor = db.cursor()


# Main Window
window = tk.Tk()
window.title("Inventory Management System")
window.geometry("500x600")

def open_product_window():
    prod_window = tk.Toplevel(window)
    prod_window.title("Product Management")
    prod_window.geometry("750x500")

    # Labels 
    tk.Label(prod_window, text="Product_Name").grid(row=0, column=0, padx=10, pady=5)
    name_entry = tk.Entry(prod_window)
    name_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(prod_window, text="Description").grid(row=1, column=0, padx=10, pady=5)
    desc_entry = tk.Entry(prod_window)
    desc_entry.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(prod_window, text="Unit_Price").grid(row=2, column=0, padx=10, pady=5)
    price_entry = tk.Entry(prod_window)
    price_entry.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(prod_window, text="Quantity").grid(row=3, column=0, padx=10, pady=5)
    quantity_entry = tk.Entry(prod_window)
    quantity_entry.grid(row=3, column=1, padx=10, pady=5)

    tk.Label(prod_window, text="Product ID").grid(row=4, column=0, padx=10, pady=5)
    product_id_entry = tk.Entry(prod_window)
    product_id_entry.grid(row=4, column=1, padx=10, pady=5)

    # Treeview to Display Products
    columns = ("product_id", "name", "description", "unit_price", "quantity")
    product_table = ttk.Treeview(prod_window, columns=columns, show='headings')
    for col in columns:
        product_table.heading(col, text=col)
        product_table.column(col, width=100)
    product_table.grid(row=6, column=0, columnspan=4, padx=10, pady=20)

    # Add Product Function
    def add_product():
        name = name_entry.get().strip()
        desc = desc_entry.get().strip()
        try:
            price = float(price_entry.get())
            quantity = int(quantity_entry.get())
            product_id = int(product_id_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers.")
            return

        if name == "":
            messagebox.showerror("Error", "Product Name cannot be empty!")
            return

        try:
            sql = "INSERT INTO items (product_id, product_name, description, unit_price, quantity) VALUES (%s, %s, %s, %s, %s)"
            values = (product_id, name, desc, price, quantity)
            cursor.execute(sql, values)
            db.commit()
            messagebox.showinfo("Success", f"Product '{name}' added successfully!")
            clear_entries()
            view_products()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add product: {e}")

    # View Products Function
    def view_products():
        for row in product_table.get_children():
            product_table.delete(row)
        cursor.execute("SELECT product_id, product_name, description, unit_price, quantity FROM items")
        products = cursor.fetchall()
        for product in products:
            product_table.insert('', tk.END, values=product)

    # Delete Product Function
    def delete_product():
        selected_item = product_table.selection()
        if not selected_item:
            messagebox.showerror("Error", "No product selected")
            return
        item_id = product_table.item(selected_item[0])['values'][0]
        cursor.execute("DELETE FROM items WHERE product_id=%s", (item_id,))
        db.commit()
        messagebox.showinfo("Success", "Product deleted successfully")
        view_products()

    # Update Product Function
    def update_product():
        selected_item = product_table.selection()
        if not selected_item:
            messagebox.showerror("Error", "No product selected")
            return
        item_id = product_table.item(selected_item[0])["values"][0]
        name = name_entry.get().strip()
        desc = desc_entry.get().strip()
        try:
            price = float(price_entry.get())
            quantity = int(quantity_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers.")
            return
        cursor.execute(
            "UPDATE items SET product_name=%s, description=%s, unit_price=%s, quantity=%s WHERE product_id=%s",
            (name, desc, price, quantity, item_id)
        )
        db.commit()
        messagebox.showinfo("Success", "Product updated successfully")
        clear_entries()
        view_products()

    # Clear entry boxes
    def clear_entries():
        name_entry.delete(0, tk.END)
        desc_entry.delete(0, tk.END)
        price_entry.delete(0, tk.END)
        quantity_entry.delete(0, tk.END)
        product_id_entry.delete(0, tk.END)

    # On Treeview Row Select
    def on_tree_select(event):
        selected_item = product_table.selection()
        if not selected_item:
            return
        values = product_table.item(selected_item[0], 'values')
        product_id_entry.delete(0, tk.END)
        product_id_entry.insert(0, values[0])
        name_entry.delete(0, tk.END)
        name_entry.insert(0, values[1])
        desc_entry.delete(0, tk.END)
        desc_entry.insert(0, values[2])
        price_entry.delete(0, tk.END)
        price_entry.insert(0, values[3])
        quantity_entry.delete(0, tk.END)
        quantity_entry.insert(0, values[4])

    product_table.bind("<<TreeviewSelect>>", on_tree_select)

    # Buttons
    tk.Button(prod_window, text="Add Product", command=add_product).grid(row=5, column=0, padx=10, pady=5)
    tk.Button(prod_window, text="View Products", command=view_products).grid(row=5, column=1, padx=10, pady=5)
    tk.Button(prod_window, text="Delete Product", command=delete_product).grid(row=5, column=2, padx=10, pady=5)
    tk.Button(prod_window, text="Update Product", command=update_product).grid(row=5, column=3, padx=10, pady=5)

    # Load products initially
    view_products()

def open_customer_window():
    customer_window = tk.Toplevel(window)
    customer_window.title("customer Management")
    customer_window.geometry("750x500")

    #labels
    tk.Label(customer_window, text="customer_id").grid(row=0, column=0 , padx=10, pady=5)
    customer_entry = tk.Entry(customer_window)
    customer_entry.grid(row=0, column=1 , padx=10, pady=5)
    tk.Label(customer_window, text="name").grid(row=1, column=0 , padx=10, pady=5)
    name_entry = tk.Entry(customer_window)
    name_entry.grid(row=1, column=1 , padx=10, pady=5)
    tk.Label(customer_window, text="Contact").grid(row=2, column=0 , padx=10, pady=5)
    contact_entry = tk.Entry(customer_window)
    contact_entry.grid(row=2, column=1 , padx=10, pady=5)

    columns = ("Customer_id", "name", "contact")
    Customer_table = ttk.Treeview(customer_window, columns=columns, show='headings')
    for col in columns:
        Customer_table.heading(col, text=col)
        Customer_table.column(col, width=100)
    Customer_table.grid(row=6, column=0, columnspan=3, padx=10, pady=20)

    def add_customers():
        name = name_entry.get()
        customer_id = customer_entry.get()
        contact = contact_entry.get()

        if name == "" or contact =="":
            messagebox.showerror("erroe","fields cannot be empty!!")
            return
        
        if not contact.isdigit() or len(contact) !=10:
            messagebox.showerror("error","The number should be of 10 digits!!")
            return
        
        try:
            sql = "INSERT INTO customers (customer_name, customer_id, contact) VALUES (%s, %s, %s)"
            values = (name, customer_id, contact)
            cursor.execute(sql, values)
            db.commit()
            messagebox.showinfo("Success", "Customer added successfully!")

            name_entry.delete(0, tk.END)
            customer_entry.delete(0, tk.END)
            contact_entry.delete(0, tk.END)

        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    def view_customers():
        for row in Customer_table.get_children():
            Customer_table.delete(row)
        cursor.execute("SELECT customer_id, customer_name, contact FROM customers")
        customers = cursor.fetchall()
        for customer in customers:
            Customer_table.insert('', tk.END, values=customer)

    # Delete Product Function
    def delete_customer():
        selected_item = Customer_table.selection()
        if not selected_item:
            messagebox.showerror("Error", "No customer selected")
            return
        customer_id = Customer_table.item(selected_item[0])['values'][0]
        cursor.execute("DELETE FROM customers WHERE customer_id=%s", (customer_id,))
        db.commit()
        messagebox.showinfo("Success", "cutomer details deleted successfully")
        view_customers()

    # Update Product Function
    def update_customer():
        selected_item = Customer_table.selection()
        if not selected_item:
            messagebox.showerror("Error", "No customer selected")
            return
        customer_id = Customer_table.item(selected_item[0])["values"][0]
        name = name_entry.get().strip()
        customer_id = customer_entry.get().strip()
        contact = contact_entry.get().strip()
        
       
        cursor.execute(
            "UPDATE customers SET customer_name=%s, contact=%s WHERE customer_id=%s",
            (name, customer_id,contact)
        )
        db.commit()
        messagebox.showinfo("Success", "Customer details updated successfully")
        clear_entries()
        view_customers()

    # Clear entry boxes
    def clear_entries():
        name_entry.delete(0, tk.END)
        customer_entry.delete(0, tk.END)
        contact_entry.delete(0, tk.END)           
    
    # On Treeview Row Select
    def on_tree_select(event):
        selected_item = Customer_table.selection()
        if not selected_item:
            return
        values = Customer_table.item(selected_item[0], 'values')
        customer_entry.delete(0, tk.END)
        customer_entry.insert(0, values[0])
        name_entry.delete(0, tk.END)
        name_entry.insert(0, values[1])
        contact_entry.delete(0, tk.END)
        contact_entry.insert(0, values[2])
       

    Customer_table.bind("<<TreeviewSelect>>", on_tree_select)

    # Buttons
    tk.Button(customer_window, text="Add ", command=add_customers).grid(row=5, column=0, padx=10, pady=5)
    tk.Button(customer_window, text="View ", command=view_customers).grid(row=5, column=1, padx=10, pady=5)
    tk.Button(customer_window, text="Delete", command=delete_customer).grid(row=5, column=2, padx=10, pady=5)
    tk.Button(customer_window, text="Update", command=update_customer).grid(row=5, column=3, padx=10, pady=5)

    # Load initially
    view_customers()

def open_supplier_window():
    supplier_window = tk.Toplevel(window)
    supplier_window.title("supplier Management")
    supplier_window.geometry("750x500")

    #labels
    tk.Label(supplier_window, text="supplier_id").grid(row=0, column=0 , padx=10, pady=5)
    supplier_entry = tk.Entry(supplier_window)
    supplier_entry.grid(row=0, column=1 , padx=10, pady=5)
    tk.Label(supplier_window, text="name").grid(row=1, column=0 , padx=10, pady=5)
    name_entry = tk.Entry(supplier_window)
    name_entry.grid(row=1, column=1 , padx=10, pady=5)
    tk.Label(supplier_window, text="Contact").grid(row=2, column=0 , padx=10, pady=5)
    contact_entry = tk.Entry(supplier_window)
    contact_entry.grid(row=2, column=1 , padx=10, pady=5)

    columns = ("supplier_id", "name", "contact")
    supplier_table = ttk.Treeview(supplier_window, columns=columns, show='headings')
    for col in columns:
        supplier_table.heading(col, text=col)
        supplier_table.column(col, width=100)
    supplier_table.grid(row=6, column=0, columnspan=3, padx=10, pady=20)

    def add_supplier():
        name = name_entry.get()
        supplier_id = supplier_entry.get()
        contact = contact_entry.get()

        if name == "" or contact =="":
            messagebox.showerror("error","fields cannot be empty!!")
            return
        
        if not contact.isdigit() or len(contact) !=10:
            messagebox.showerror("error","The number should be of 10 digits!!")
            return
        
        try:
            sql = "INSERT INTO suppliers (supplier_name, supplier_id, contact) VALUES (%s, %s, %s)"
            values = (name, supplier_id, contact)
            cursor.execute(sql, values)
            db.commit()
            messagebox.showinfo("Success", "Customer added successfully!")

            name_entry.delete(0, tk.END)
            supplier_entry.delete(0, tk.END)
            contact_entry.delete(0, tk.END)

        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    def view_supplier():
        for row in supplier_table.get_children():
            supplier_table.delete(row)
        cursor.execute("SELECT supplier_id, supplier_name, contact FROM suppliers")
        suppliers = cursor.fetchall()
        for supplier in suppliers:
            supplier_table.insert('', tk.END, values=supplier)

    # Delete Function
    def delete_supplier():
        selected_item = supplier_table.selection()
        if not selected_item:
            messagebox.showerror("Error", "No supplier selected")
            return
        supplier_id = supplier_table.item(selected_item[0])['values'][0]
        cursor.execute("DELETE FROM suppliers WHERE supplier_id=%s", (supplier_id,))
        db.commit()
        messagebox.showinfo("Success", "supplier deleted successfully")
        view_supplier()

    # Update  Function
    def update_supplier():
        selected_item = supplier_table.selection()
        if not selected_item:
            messagebox.showerror("Error", "No supplier selected")
            return
        supplier_id = supplier_table.item(selected_item[0])["values"][0]
        name = name_entry.get().strip()
        supplier_id = supplier_entry.get().strip()
        contact = contact_entry.get().strip()
        
       
        cursor.execute(
            "UPDATE customers SET supplier_name=%s, contact=%s WHERE supplier_id=%s",
            (name, supplier_id, contact)
        )
        db.commit()
        messagebox.showinfo("Success", "supplier updated successfully")
        clear_entries()
        view_supplier()

    # Clear entry boxes
    def clear_entries():
        name_entry.delete(0, tk.END)
        supplier_entry.delete(0, tk.END)
        contact_entry.delete(0, tk.END)           
    
    # On Treeview Row Select
    def on_tree_select(event):
        selected_item = supplier_table.selection()
        if not selected_item:
            return
        values = supplier_table.item(selected_item[0], 'values')
        supplier_entry.delete(0, tk.END)
        supplier_entry.insert(0, values[0])
        name_entry.delete(0, tk.END)
        name_entry.insert(0, values[1])
        contact_entry.delete(0, tk.END)
        contact_entry.insert(0, values[2])
       

    supplier_table.bind("<<TreeviewSelect>>", on_tree_select)

    # Buttons
    tk.Button(supplier_window, text="Add ", command=add_supplier).grid(row=5, column=0, padx=10, pady=5)
    tk.Button(supplier_window, text="View ", command=view_supplier).grid(row=5, column=1, padx=10, pady=5)
    tk.Button(supplier_window, text="Delete", command=delete_supplier).grid(row=5, column=2, padx=10, pady=5)
    tk.Button(supplier_window, text="Update", command=update_supplier).grid(row=5, column=3, padx=10, pady=5)

    
    view_supplier()

def open_sales_window():
    win = tk.Toplevel(window)
    win.title("Sales Transaction")
    win.geometry("800x600")

    tk.Label(win, text="select customer").grid(column=0, row=0, padx=10, pady=5)
    customer_combo = ttk.Combobox(win)
    customer_combo.grid(row=0, column=1, padx=1, pady=5)
    cursor.execute("select customer_id, customer_name from customers")
    customers = cursor.fetchall()
    customer_map = {f"{c[1]}(ID:{c[0]})": c[0] for c in customers}
    customer_combo['values'] = list(customer_map.keys())

    tk.Label(win, text="select product").grid(column=0, row=1, padx=10, pady=5)
    product_combo = ttk.Combobox(win)
    product_combo.grid(row=1, column=1, padx=1, pady=5)
    cursor.execute("select product_id, product_name, unit_price, quantity, description from items")
    product = cursor.fetchall()
    product_map = {f"{p[1]}(ID:{p[0]})": p for p in product}
    product_combo['values'] = list(product_map.keys())

    tk.Label(win, text="Quantity").grid(row=2, column=0, padx=10, pady=5)
    qty_entry = tk.Entry(win)
    qty_entry.grid(row=2, column=1, padx=10, pady=5)

    columns = ("Product", "Quantity", "Unit Price", "Total")
    sale_table = ttk.Treeview(win, columns=columns, show="headings")
    for col in columns:
        sale_table.heading(col, text=col)
        sale_table.column(col, width=120)
    sale_table.grid(row=4, column=0, columnspan=4, padx=10, pady=20)

    total_amount = tk.DoubleVar(value=0.0)
    tk.Label(win, text="Total Amount:").grid(row=5, column=2, padx=10, pady=5)
    total_label = tk.Label(win, textvariable=total_amount, font=("Arial", 12, "bold"), fg="green")
    total_label.grid(row=5, column=3, padx=10, pady=5)

    sale_items = []

    def update_total_amount():
        total = 0
        for child in sale_table.get_children():
            item_total = float(sale_table.item(child, 'values')[3])
            total += item_total
        total_amount.set(round(total, 2))

    def add_item():
        product_key = product_combo.get()
        if not product_key or product_key not in product_map:
            messagebox.showerror("Error", "Please select a valid product.")
            return

        try:
            quantity = int(qty_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Quantity must be a number.")
            return

        product = product_map[product_key]
        if quantity <= 0:
            messagebox.showerror("Error", "Quantity must be positive.")
            return
        if quantity > product[3]:
            messagebox.showerror("Error", f"Only {product[3]} units available in stock.")
            return

        total_price = round(quantity * product[2], 2)
        sale_items.append((product[0], product[1], quantity, product[2], total_price))
        sale_table.insert('', tk.END, values=(product[1], quantity, product[2], total_price))

        qty_entry.delete(0, tk.END)
        update_total_amount()

    def remove_item():
        selected_item = sale_table.selection()
        if not selected_item:
            messagebox.showerror("Error", "No item selected.")
            return

        for item in selected_item:
            sale_table.delete(item)

        update_total_amount()

    def confirm_sale():
        if not sale_table.get_children():
            messagebox.showerror("Error", "No items in the sale.")
            return

        customer_key = customer_combo.get()
        if not customer_key or customer_key not in customer_map:
            messagebox.showerror("Error", "Please select a valid customer.")
            return

        customer_id = customer_map[customer_key]
        sale_total = total_amount.get()

        try:
            # Insert sale header
            cursor.execute("INSERT INTO sales_transaction (date, customer_id, total_amount) VALUES (NOW(), %s, %s)", (customer_id, sale_total))
            db.commit()

            cursor.execute("SELECT LAST_INSERT_ID()")
            sale_id = cursor.fetchone()[0]

            for child in sale_table.get_children():
                values = sale_table.item(child, 'values')
                product_name, quantity, unit_price, _ = values
                # Get product_id using product name
                product_id = None
                for p in product:
                    if p[1] == product_name:
                        product_id = p[0]
                        break

                cursor.execute("INSERT INTO sale_details (sale_id, product_id, quantity, unit_price) VALUES (%s, %s, %s, %s)", (sale_id, product_id, quantity, unit_price))
                cursor.execute("UPDATE items SET quantity = quantity - %s WHERE product_id = %s", (quantity, product_id))

            db.commit()
            messagebox.showinfo("Success", f"Sale completed successfully with Sale ID: {sale_id}")

            # Clear UI
            sale_items.clear()
            sale_table.delete(*sale_table.get_children())
            total_amount.set(0.0)

        except Exception as e:
            db.rollback()
            messagebox.showerror("Database Error", str(e))

    tk.Button(win, text="Add Item", command=add_item).grid(row=3, column=0, padx=10, pady=5)
    tk.Button(win, text="Remove Selected Item", command=remove_item).grid(row=3, column=1, padx=10, pady=5)
    tk.Button(win, text="Confirm Sale", command=confirm_sale).grid(row=5, column=0, padx=10, pady=5)


def open_purchase_window():
    win = tk.Toplevel(window)
    win.title("Purchase Transaction")
    win.geometry("900x600")

    # Supplier selection
    tk.Label(win, text="Select Supplier").grid(row=0, column=0, padx=10, pady=5)
    supplier_combo = ttk.Combobox(win)
    supplier_combo.grid(row=0, column=1, padx=10, pady=5)
    cursor.execute("SELECT supplier_id, supplier_name FROM suppliers")
    suppliers = cursor.fetchall()
    supplier_map = {f"{s[1]}(ID:{s[0]})": s[0] for s in suppliers}
    supplier_combo['values'] = list(supplier_map.keys())

    # Product selection
    tk.Label(win, text="Select Product").grid(row=1, column=0, padx=10, pady=5)
    product_combo = ttk.Combobox(win)
    product_combo.grid(row=1, column=1, padx=10, pady=5)
    cursor.execute("SELECT product_id, product_name FROM items")
    products = cursor.fetchall()
    product_map = {f"{p[1]}(ID:{p[0]})": p[0] for p in products}
    product_combo['values'] = list(product_map.keys())

    # Quantity entry
    tk.Label(win, text="Quantity").grid(row=2, column=0, padx=10, pady=5)
    qty_entry = tk.Entry(win)
    qty_entry.grid(row=2, column=1, padx=10, pady=5)

    # Unit price entry (this was missing or misaligned)
    tk.Label(win, text="Unit Price").grid(row=3, column=0, padx=10, pady=5)
    price_entry = tk.Entry(win)
    price_entry.grid(row=3, column=1, padx=10, pady=5)

    # Purchase table
    columns = ("Product", "Quantity", "Unit Price", "Total")
    purchase_table = ttk.Treeview(win, columns=columns, show="headings")
    for col in columns:
        purchase_table.heading(col, text=col)
        purchase_table.column(col, width=120)
    purchase_table.grid(row=5, column=0, columnspan=5, padx=10, pady=20)

    # Total amount display
    total_amount = tk.DoubleVar(value=0.0)
    tk.Label(win, text="Total Amount:").grid(row=6, column=3, padx=10, pady=5)
    total_label = tk.Label(win, textvariable=total_amount, font=("Arial", 12, "bold"), fg="green")
    total_label.grid(row=6, column=4, padx=10, pady=5)

    def update_total_amount():
        total = 0
        for child in purchase_table.get_children():
            item_total = float(purchase_table.item(child, 'values')[3])
            total += item_total
        total_amount.set(round(total, 2))

    def add_item():
        product_key = product_combo.get()
        if not product_key or product_key not in product_map:
            messagebox.showerror("Error", "Select a valid product.")
            return

        try:
            quantity = int(qty_entry.get())
            unit_price = float(price_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Quantity and Unit Price must be numbers.")
            return

        if quantity <= 0 or unit_price <= 0:
            messagebox.showerror("Error", "Quantity and Unit Price must be positive.")
            return

        total_price = round(quantity * unit_price, 2)
        purchase_table.insert('', tk.END, values=(product_key.split("(ID:")[0], quantity, unit_price, total_price))

        qty_entry.delete(0, tk.END)
        price_entry.delete(0, tk.END)
        update_total_amount()

    def remove_item():
        selected_item = purchase_table.selection()
        if not selected_item:
            messagebox.showerror("Error", "No item selected.")
            return
        for item in selected_item:
            purchase_table.delete(item)
        update_total_amount()

    def confirm_purchase():
        if not purchase_table.get_children():
            messagebox.showerror("Error", "No items in the purchase.")
            return

        supplier_key = supplier_combo.get()
        if not supplier_key or supplier_key not in supplier_map:
            messagebox.showerror("Error", "Select a valid supplier.")
            return

        supplier_id = supplier_map[supplier_key]
        purchase_total = total_amount.get()

        try:
            cursor.execute("INSERT INTO purchase_transaction (date, supplier_id, total_amount) VALUES (NOW(), %s, %s)",
                           (supplier_id, purchase_total))
            db.commit()

            cursor.execute("SELECT LAST_INSERT_ID()")
            purchase_id = cursor.fetchone()[0]

            for child in purchase_table.get_children():
                values = purchase_table.item(child, 'values')
                product_name, quantity, unit_price, _ = values

                product_id = None
                for p in products:
                    if p[1] == product_name:
                        product_id = p[0]
                        break

                cursor.execute("INSERT INTO purchase_details (purchase_id, product_id, quantity, unit_price) VALUES (%s, %s, %s, %s)",
                               (purchase_id, product_id, quantity, unit_price))
                cursor.execute("UPDATE items SET quantity = quantity + %s WHERE product_id = %s", (quantity, product_id))

            db.commit()
            messagebox.showinfo("Success", f"Purchase completed successfully with Purchase ID: {purchase_id}")

            purchase_table.delete(*purchase_table.get_children())
            total_amount.set(0.0)

        except Exception as e:
            db.rollback()
            messagebox.showerror("Database Error", str(e))

    # Buttons
    tk.Button(win, text="Add Item", command=add_item).grid(row=4, column=0, padx=10, pady=5)
    tk.Button(win, text="Remove Selected Item", command=remove_item).grid(row=4, column=1, padx=10, pady=5)
    tk.Button(win, text="Confirm Purchase", command=confirm_purchase).grid(row=6, column=0, padx=10, pady=5)

def open_sale_details_window():
    win = tk.Toplevel(window)
    win.title("Sale Details")
    win.geometry("700x400")

    tk.Label(win, text="Enter Sale ID:").grid(row=0, column=0, padx=10, pady=10)
    sale_id_entry = tk.Entry(win)
    sale_id_entry.grid(row=0, column=1, padx=10, pady=10)

    columns = ("Product Name", "Quantity", "Unit Price", "Total")
    details_table = ttk.Treeview(win, columns=columns, show="headings")
    for col in columns:
        details_table.heading(col, text=col)
        details_table.column(col, width=120)
    details_table.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

    def fetch_details():
        sale_id = sale_id_entry.get()
        if not sale_id.isdigit():
            messagebox.showerror("Error", "Sale ID must be a number.")
            return

        details_table.delete(*details_table.get_children())

        try:
            cursor.execute("""
                SELECT i.product_name, sd.quantity, sd.unit_price,
                       (sd.quantity * sd.unit_price) AS total
                FROM sale_details sd
                JOIN items i ON sd.product_id = i.product_id
                WHERE sd.sale_id = %s
            """, (sale_id,))
            rows = cursor.fetchall()
            if not rows:
                messagebox.showinfo("Info", "No details found for this Sale ID.")
                return
            for row in rows:
                details_table.insert('', tk.END, values=row)
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    tk.Button(win, text="Fetch Details", command=fetch_details).grid(row=0, column=2, padx=10, pady=10)

def open_purchase_details_window():
    win = tk.Toplevel(window)
    win.title("Purchase Details")
    win.geometry("700x400")

    tk.Label(win, text="Enter Purchase ID:").grid(row=0, column=0, padx=10, pady=10)
    purchase_id_entry = tk.Entry(win)
    purchase_id_entry.grid(row=0, column=1, padx=10, pady=10)

    columns = ("Product Name", "Quantity", "Unit Price", "Total")
    details_table = ttk.Treeview(win, columns=columns, show="headings")
    for col in columns:
        details_table.heading(col, text=col)
        details_table.column(col, width=120)
    details_table.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

    def fetch_details():
        purchase_id = purchase_id_entry.get()
        if not purchase_id.isdigit():
            messagebox.showerror("Error", "Purchase ID must be a number.")
            return

        details_table.delete(*details_table.get_children())

        try:
            cursor.execute("""
                SELECT i.product_name, pd.quantity, pd.unit_price,
                       (pd.quantity * pd.unit_price) AS total
                FROM purchase_details pd
                JOIN items i ON pd.product_id = i.product_id
                WHERE pd.purchase_id = %s
            """, (purchase_id,))
            rows = cursor.fetchall()
            if not rows:
                messagebox.showinfo("Info", "No details found for this Purchase ID.")
                return
            for row in rows:
                details_table.insert('', tk.END, values=row)
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    tk.Button(win, text="Fetch Details", command=fetch_details).grid(row=0, column=2, padx=10, pady=10)


# Main window button
tk.Button(window, text="Manage Products", command=open_product_window).pack(pady=20)
tk.Button(window, text="Manage Customers", command=open_customer_window).pack(pady=20)
tk.Button(window, text="Manage Suppliers", command=open_supplier_window).pack(pady=20)
tk.Button(window, text="Sales Transaction", command=open_sales_window).pack(pady=20)
tk.Button(window, text="Purchase Transaction", command=open_purchase_window).pack(pady=20)
tk.Button(window, text="Sale Details", command=open_sale_details_window).pack(pady=20)
tk.Button(window, text="Purchase Details", command=open_purchase_details_window).pack(pady=20)
window.mainloop()