# Name: Theresa Quach
# Course: CS361
# Project: Sprint#1 -   User Interface (UI) for the Retail Calculator program. Currently allows the user to create an account and login.

import time
from functools import *
from tkinter import *
import tkinter as tk
from subprocess import *
from tkinter.messagebox import *
import sys
import json
import webbrowser

current_user = ""                                                                                                       # global variable to hold username of current user
user_products=[]

def createacct(username, password):
    global current_user


    # Opens acctnotif.txt and writes command to create an account. Creates the document if it doesn't exist.
    fd = open("acctnotif.txt", "w+")
    fd.write("create account")
    fd.truncate(len("create account"))
    fd.write("\n"+username.get()+":"+password.get())
    fd.close()

    time.sleep(1)

    # Returns to beginning of acctnotif.txt for update
    fd = open("acctnotif.txt", "r+")
    result=fd.readline()
    result=result.strip('\n')
    if (result == "user created"):
        # Current user's username saved to global for project management
        result = fd.readline()
        result = result.strip('\n')
        current_user = result
        # Clear error messages
        user_msg.config(text="")
        # Change UI to program's main page
        app.deiconify()
        start.withdraw()
    elif (result == "user exists"):
        user_msg.config(text="Username already exists. Please select another.")
    else:
        user_msg.config(text="Error: Account Services")

    # Clear entry boxes
    username_box.delete(0, END)
    password_box.delete(0, END)

    fd.close()

    ret_main()


def login(username, password):
    global current_user

    # Opens acctnotif.txt and writes command to log into an account. Creates the document if it doesn't exist.
    fd = open("acctnotif.txt", "w+")
    fd.write("login")
    fd.truncate(len("login"))
    fd.write("\n"+username.get()+":"+password.get())
    fd.close() 

    # Sleeps for 10 seconds to allow other service to finish searching for and/or creating the user account
    time.sleep(2)

    # Returns to beginning of acctnotif.txt for update
    fd = open("acctnotif.txt", "r+")
    result=fd.readline()
    result=result.strip('\n')
    if (result == "user found"):
        # Current user's username saved to global for project management
        result = fd.readline()
        result = result.strip('\n')
        current_user = result
        # Clear error messages
        user_msg.config(text="")
        # Change UI to program's main page
        app.deiconify()
        start.withdraw()
    elif (result == "bad password"):
        user_msg.config(text="Incorrect password. Please try again.")
    elif (result == "user not found"):
        user_msg.config(text="Account not found. Please try again.")
    else:
        user_msg.config(text="Error: Account Services")

    # Clear entry boxes
    username_box.delete(0, END)
    password_box.delete(0, END)

    fd.close()

    ret_main()


def ret_main():
    """
    Function that returns the user to the main of the window and removes widget frames (if appicable)
    """
    share_msg.grid_forget()
    add_frame.grid_forget()
    rmcalc_frame.grid_forget()

    main_frame.grid(row=10, column=50, rowspan=60)

    return

def show_add():
    """
    Function that moves the user to the Add Product screen by hiding other main window widgets and replacing them with the Add Product widgets
    """
    main_frame.grid_forget()
    share_msg.grid_forget()
    rmcalc_frame.grid_forget()

    add_frame.grid(row=2, column = 40, rowspan=90, pady=5)


def add_prod():
    """
    Event handler function that, after user confirms input, takes user inputted product (materials, costs, labor, etc.) and puts it into the user's file 
    on a new line in dictionary object format.
    Window widgets change to allow user to input product information, including product name, material names and costs (up to 3), labor costs, and percent
    markup.
    """
    confirm = askyesno(title="Confirm Add Product", message="Are you sure you want to add the product with these details?")

    # If user confirms adding product
    if confirm:

        product_name = prod_name.get(1.0, "end-1c")
        material1_name = mat1_name.get(1.0, "end-1c")
        if (material1_name == "Material Name"):
            material1_name = "None"
        material1_cost = mat1_cost.get(1.0, "end-1c")
        if (material1_cost == "Cost"):
            material1_cost = "0"
        material2_name = mat2_name.get(1.0, "end-1c")
        if (material2_name == "Material Name"):
            material2_name = "None"
        material2_cost = mat2_cost.get(1.0, "end-1c")
        if (material2_cost == "Cost"):
            material2_cost = "0"
        labor_time = hours.get(1.0, "end-1c")
        if (labor_time == "Hours worked"):
            labor_time = "0"
        labor_cost = hour_cost.get(1.0, "end-1c")
        if (labor_cost == "Cost per hour"):
            labor_cost = "0"
        percent = markup.get(1.0, "end-1c")
        if ("Enter" in percent):
            percent = "0"

        userfile = open(current_user+".txt", "a+")
        string_to_store = '{"'+product_name+'":[{"materials":{"'+material1_name+'":"'+material1_cost+'","'+material2_name+'":"'+material2_cost+'"}},{"labor":{"'+labor_time+'":"'+labor_cost+'"}},{"percent_markup":"'+percent+'"}]}\n'
        userfile.write(string_to_store)
        userfile.close
        completed = showinfo("Confirmation", "Product Added.")


def show_rmcalc():
    """
    Function that moves the user to the shared Edit, Remove, Calculate Product screen by hiding other main window widgets and replacing them with Product widgets
    to edit, remove, or calculate the cost of products.
    """
    global user_products

    # Hide other widgets and replace with Edit/Remove/Calculate Product page widgets
    main_frame.grid_forget()
    share_msg.grid_forget()
    add_frame.grid_forget()

    rmcalc_frame.grid(row=2, column = 40, rowspan=90, pady=5)
    
    # Populate user's products list
    user_file = open(current_user+".txt", "r+")
    for line in user_file:
        line=line.strip('\n')
        if line not in user_products:
            user_products.append(line)
    user_file.close()

    # Populate dropdown menu with user's products if there are products in the file
    if len(user_products) > 0:
        # Remove default list options
        product.set('')
        prod_list['menu'].delete(0, 'end')
        # Add user products to menu  
        for prod in user_products:
            prod_list['menu'].add_command(label=prod, command=tk._setit(product, prod))
    else:
        product.set('')


def calculate():
    """
    Function that signals to another microservice to calculate the suggested retail price of a product through acctnotif.txt with the
    command 'calculate' and the information (in json-format) of the product to be calculated.
    """

    main_frame.grid_forget()

    # Write 'calculate' and user's selected product
    fd = open("acctnotif.txt", "w+")
    fd.write("calculate")
    fd.truncate(len("calculate"))
    fd.write("\n"+product.get())
    fd.close() 

    time.sleep(2)

    # Read returned price and present in notification to user
    fd = open("acctnotif.txt", "r+")
    price=fd.readline()
    price=price.strip('\n')
    completed = showinfo("Confirmation", "Suggest retail price: "+ price)



def remove_prod():
    """
    Function that allows user delete selected product from their file.
    """
    global user_products

    main_frame.grid_forget()

    prod_tormv = product.get()
    confirm = askyesno(title="Confirm Remove Product", message="Are you sure you want to delete the selected product")

    # If user confirms removing product, remove data from user's file and present confirmation message
    if confirm:
        fd = open(current_user+".txt", "r+")
        products_text = fd.readlines()
        fd.close()
        fd = open(current_user+".txt", "w+")
        for prod in products_text:
            print(prod)
            if prod.strip("\n") != prod_tormv:
                fd.write(prod)
        for prod in user_products:
            if prod_tormv == prod:
                user_products.remove(prod_tormv)
        fd.close()
        completed = showinfo("Confirmation", "Product removed.")


def product_list():
    """
    Function that allows the user to view a list of all of their entered products (by name) in a pop-up window
    """

    # Populate user's products list
    user_file = open(current_user+".txt", "r+")
    for line in user_file:
        line=line.strip('\n')
        if line not in user_products:
            user_products.append(line)
    user_file.close()

    prod_names = []

    for prod in user_products:
        json_prod = json.loads(prod)
        prod_keys = json_prod.keys()
        for key in prod_keys:
            print(key)
            prod_names.append(key+"\n")

    completed = showinfo("Product List", prod_names)


def tutorial():
    webbrowser.open_new('Getting Started.pdf')
    return


def logout():
    # Clear current username from global
    current_user = ""
    
    # Return main page widgets to normal and return to login screen
    main_frame.grid(row=20, column=50, rowspan=20)
    app.withdraw()
    start.deiconify()


def exit():
    fd = open("acctnotif.txt", "w+")
    fd.write("terminate")
    fd.truncate(len("terminate"))
    fd.close() 

    start.destroy()
    app.destroy()
    sys.exit()




if __name__ == '__main__':
    print("Retail Calculator UI program running\n")


    # First UI on startup is different from logged-in UI
    # Creating windows GUI for retail product calculator
    app = Tk()                                                                                                          # Main window
    app.title("Retail Product Calculator - Theresa Quach - CS361")
    app.geometry("1000x800")
    
    start = Toplevel()                                                                                                  # Login window
    start.geometry("800x600")
    

    # Configure main window for rows/columns placement
    for i in range(101):
        app.columnconfigure(i, weight=1)
    for i in range(101):
        app.rowconfigure(i, weight=1)
    
    # Configure login window for rows/columns placement
    for i in range(101):
        start.columnconfigure(i, weight=1)
    for i in range(101):
        start.rowconfigure(i, weight=1)

    # Starting window widgets
    # Menu bar for login window
    login_menu = Menu(start)
    filemenu1 = Menu(login_menu, tearoff=0)
    filemenu1.add_command(label="Exit Program" , command = exit)
    login_menu.add_cascade(label="File", menu = filemenu1)

    # Menu bar for main window
    main_menu = Menu(app)
    filemenu2 = Menu(main_menu, tearoff=0)
    filemenu2.add_command(label="Main Page", command = ret_main)
    filemenu2.add_command(label="Logout", command = logout)
    filemenu2.add_separator()
    filemenu2.add_command(label="Exit Program" , command = exit)
    main_menu.add_cascade(label="File", menu=filemenu2)

    prod_menu = Menu(main_menu, tearoff=0)
    prod_menu.add_command(label="Add Product", command = show_add)
    prod_menu.add_command(label="Remove Product", command = show_rmcalc)
    prod_menu.add_command(label="Calculate Product Cost", command = show_rmcalc)
    prod_menu.add_separator()
    adv_prod = Menu(prod_menu, tearoff=0)
    adv_prod.add_command(label="List Products", command = product_list)
    prod_menu.add_cascade(label="Advanced Options", menu = adv_prod)
    main_menu.add_cascade(label="Product", menu = prod_menu)

    help_menu = Menu(main_menu, tearoff=0)
    help_menu.add_command(label="Get Started", command = tutorial)
    main_menu.add_cascade(label="Help", menu = help_menu)

    # Write introduction to user
    intro = Label(start, text="Welcome to the Retail Product Calculator, a program designed for small business owners to calculate suggested retail prices for their products and crafts, and to store product info into an electronic database. Please create an account or login to begin.\n", font=("Helvetica", 14), wraplength=700).grid(row=2, column=49, sticky = 'n', columnspan=2)
    login_instruct = Label(start, text="Usernames are not case-sensitive; Passwords are case-sensitive.\n", font=("Helvetica", 11), wraplength=700).grid(row=3, column=49, sticky = 'n', columnspan=2)

    # Username and password textboxes
    username_label = Label(start, text="User Name:", font=("Helvetica", 12)).grid(row=20, column=49)
    username = StringVar()
    username_box = Entry(start, textvariable=username, width=50)
    username_box.grid(row=20, column=50)

    password_label = Label(start, text="Password:", font=("Helvetica", 12)).grid(row=25, column=49)
    password = StringVar()
    password_box = Entry(start, textvariable=password, width = 50, show='*')
    password_box.grid(row=25, column=50)

    # Create button for user to press and register program function to button
    createacct = partial(createacct, username, password)
    login = partial(login, username, password)
    user_button1 = Button(start, text="Create New Account", width=20, height=1, bg='#CBCBCB',  font=("Helvetica", 12), command=createacct).grid(row=35, column=49, columnspan=2)
    user_button2 = Button(start, text="Login", width=20, height=1, bg='#CBCBCB',  font=("Helvetica", 12), command=login).grid(row=38, column=49, columnspan=2)
    user_button3 = Button(start, text="Exit", width=20, height=1, bg='#CBCBCB',  font=("Helvetica", 12), command=exit).grid(row=41, column=49, columnspan=2)
    
    # User notification messages label
    user_msg = Label(start, font=("Helvetica", 13), fg = 'red')
    user_msg.grid(row=10, column=49, columnspan=2)                     


    # Frame for main page widgets
    main_frame = Frame(app)
    main_frame.grid(row=10, column=50, rowspan=60)
    welcome = Label(main_frame, text="Welcome to the Retail Product Calculator. To begin, please select an action from the left.\n New Users should begin by clicking 'Add Product'. \n\nFor more information, click the Help menu at the top of the window. ", font=("Helvetica", 15), wraplength=300)
    welcome.grid(row=20, column=50, rowspan=20)
    

    # Left-side Navigation button widgets
    main_button = Button(app, text="Main", width=14, height=1, bg='#CBCBCB',  font=("Helvetica", 12), command=ret_main).grid(row=5, column=2, sticky = 'w')
    addprod_button = Button(app, text="Add Product", width=14, height=1, bg='#CBCBCB',  font=("Helvetica", 12), command=show_add).grid(row=7, column=2, sticky = 'w')
    removeprod_button = Button(app, text="Remove Product", width=14, height=1, bg='#CBCBCB',  font=("Helvetica", 12), command=show_rmcalc).grid(row=9, column=2, sticky = 'w')
    calcost_button = Button(app, text="Calculate Cost", width=14, height=1, bg='#CBCBCB',  font=("Helvetica", 12), command=show_rmcalc).grid(row=11, column=2, sticky = 'w')       
    logout_button = Button(app, text="Logout", width=14, height=1, bg='#CBCBCB',  font=("Helvetica", 12), command=logout).grid(row=13, column=2, sticky = 'w')
    exit_button = Button(app, text="Exit", width=14, height=1, bg='#CBCBCB',  font=("Helvetica", 12), command=exit).grid(row=15, column=2, sticky = 'w')
    

    # Share widgets
    share_msg = Label(app, font=("Helvetica", 13))


    # Add Product Frame and widgets
    add_frame = Frame(app, width = 60, height = 100)
    add_frame.grid(row=2, column = 40, rowspan=90, pady=5)
    add_name = Label(add_frame, text = "Here you can create and add individual products and their associated materials, costs, and labor.\n You can use the keyboard shortcuts 'Ctrl-Z' to undo typing errors and 'Ctrl-Y' to redo text deletions in these fields.\n\n To begin, type in the product's name.", font = ("Helvetica", 12), wraplength = 500)
    add_name.grid(row=2, column = 40, rowspan=10, pady=5)
    prod_name = Text(add_frame, width=30, height=1, undo=True)
    prod_name.grid(row=15, column = 20, columnspan=25, pady=10)
    prod_name.insert(END, "Product Name")

    add_mats = Label(add_frame, text = "Next, add materials used to make the product and their costs. If the product was bought wholesale, please RETYPE THE NAME OF THE PRODUCT and put in the total cost of the product (i.e. 'Necklace, 15'.", font = ("Helvetica", 12), wraplength = 500)
    add_mats.grid(row=25, column = 40, rowspan=10)
    mat1_name = Text(add_frame, width = 30, height = 1, undo=True)
    mat1_name.grid(row=35, column=30, rowspan=10, columnspan=20, pady=5)
    mat1_name.insert(END, "Material Name")
    mat1_cost = Text(add_frame, width = 10, height = 1, undo=True)
    mat1_cost.grid(row=35, column =60, rowspan=10, columnspan=20, pady=5)
    mat1_cost.insert(END, "Cost",)
    mat2_name = Text(add_frame, width = 30, height = 1, undo=True)
    mat2_name.grid(row=45, column=30, rowspan=10, columnspan=20, pady=5)
    mat2_name.insert(END, "Material Name")
    mat2_cost = Text(add_frame, width = 10, height = 1, undo=True)
    mat2_cost.grid(row=45, column =60, rowspan=10, columnspan=20, pady=5)
    mat2_cost.insert(END, "Cost")

    add_work = Label(add_frame, text = "Then, add the amount of labor (in hours) and cost of labor (price per hour) used to produce this product. If not applicable, enter '0' for both fields.", font = ("Helvetica", 12), wraplength = 500)
    add_work.grid(row=55, column=20, rowspan=10, columnspan=25, pady=5)
    hours = Text( add_frame, width = 15, height = 1, undo=True)
    hours.grid(row=65, column=25, rowspan=10, columnspan=20, pady=5)
    hours.insert(END,"Hours worked")
    hour_cost = Text(add_frame, width = 15, height = 1, undo=True)
    hour_cost.grid(row=65, column=45, rowspan=10, columnspan=25, pady=5)
    hour_cost.insert(END,"Cost per hour")

    add_markup = Label(add_frame, text = "Lastly, add the percent markup you'd like to use for your suggested retail price (i.e. Enter '100' for 100%, '50' for 50%, etc.)", font = ("Helvetica", 12), wraplength = 500)
    add_markup.grid(row=75, column=33, columnspan=25, pady=5)
    markup = Text(add_frame, width = 35, height = 1, undo=True)
    markup.grid(row=80, column=40, rowspan=10, columnspan=25, pady=5)
    markup.insert(END,"i.e. Enter '150' for 150%")

    add_confirm = Label(add_frame, text = "Press Add to confirm your product.", font = ("Helvetica", 12), wraplength = 500)
    add_confirm.grid(row=90, column=40, columnspan=25, pady=5)
    add_button = Button(add_frame, text="Add", width=14, height=1, bg='#CBCBCB',  font=("Helvetica", 12), command=add_prod)
    add_button.grid(row=95, column=40, pady=5)


    # Edit/Remove/Calculate Widgets
    default_prod=["No products found"]
    rmcalc_frame = Frame(app)
    rmcalc_frame.grid(row=2, column = 40, rowspan=100, columnspan=3, pady=5)
    prodlist_instructions = Label(rmcalc_frame, text = "To edit, remove, or calculate the cost of a product. Please select a product from your account below and select the desired action. To see an updated list, return to Main Page and navigate back here.", font = ("Helvetica", 13), wraplength=600)
    prodlist_instructions.grid(row=5, column=37, columnspan=5, pady=5)
    product = StringVar(rmcalc_frame)
    product.set("Choose a product")
    prod_list = OptionMenu(rmcalc_frame, product, default_prod)
    prod_list.config(width=50)
    prod_list.grid(row=20, column=39, rowspan=25)
    remove_button = Button(rmcalc_frame, text="Remove", width=14, height=1, bg='#CBCBCB',  font=("Helvetica", 12), command=remove_prod)
    remove_button.grid(row=52, column=37, pady=20)
    calc_button = Button(rmcalc_frame, text="Calculate Price", width=14, height=1, bg='#CBCBCB',  font=("Helvetica", 12), command=calculate)
    calc_button.grid(row=52, column=40, pady=20)




    start.config(menu=login_menu)
    app.config(menu=main_menu)
    
    add_frame.grid_forget()
    rmcalc_frame.grid_forget()

    app.withdraw()         
    app.mainloop()






