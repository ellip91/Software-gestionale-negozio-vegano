import csv

class VeganShop:
    # Initialize empty lists for products and sales
    def __init__(self):          
        self.product_list = []    
        self.sell_list = []

    def add_product(self, name, quantity): 
        # Add a new product
        #if product already exists, update only quantity 
        for product in self.product_list:
            if product["name"] == name:
                product["quantity"] += quantity
                print(f"AGGIUNTO: {quantity}x{name}")
                return
        # If the product doesn't exist, get purchase and sell cost from input and add it to the list    
        #verify purchase_cost
        while True:
            try:
                purchase_cost = float(input("Inserisci il prezzo di acquisto: "))
                if purchase_cost <= 0:
                    raise ValueError("I prezzi devono essere numeri float positivi.")
                break
            except ValueError:
                print("Inserisci un valore valido per il prezzo di acquisto.")

    # Verify sell cost
        while True:
            try:
                sell_cost = float(input("Inserisci il prezzo di vendita: "))
                if sell_cost <= 0:
                    raise ValueError("I prezzi devono essere numeri float positivi.")
                break
            except ValueError:
                print("Inserisci un valore valido per il prezzo di vendita.")
        new_product = {'name': name, 'quantity': quantity, 'purchase_cost': purchase_cost, 'sell_cost': sell_cost}
        self.product_list.append(new_product)
        print(f"AGGIUNTO: {quantity} x {name}")

    def product_sale (self, product_name, sell_quantity):
        # methof for recording a sale, updating quantities, and calculating total price
        partial_sell_list=[] # List to store partial sales for later display
        while True:
            for product in self.product_list:    #verify that product is in the product_list.
                if product["name"] == product_name:
                    if product["quantity"] >= sell_quantity:
                        product["quantity"] -= sell_quantity #update quantity in the list
                        sell_cost=product["sell_cost"]
                        total_price = sell_quantity * product["sell_cost"] 
                        #add info in both sell and partial sell list. the first one will be used
                        #for profits calculation
                        partial_sell_list.append({'name': product_name, 'quantity': sell_quantity, "sell_cost": sell_cost, 'total_price':total_price})
                        self.sell_list.append({'name': product_name, 'quantity': sell_quantity, "sell_cost": sell_cost, 'total_price':total_price})
                    else:
                        print("Quantità insufficiente in magazzino.")
                    break  # Esci dal ciclo for
            else:        
                print("Prodotto non trovato in magazzino.")

            # Ask the user if He want to add another product
            answer = input("Vuoi aggiungere un altro prodotto? (si/no): ")
            if answer == 'si':
                product_name = input("Inserisci il nome del nuovo prodotto: ")
                while True:
                    try:
                        sell_quantity = int(input("Inserisci la quantità venduta del nuovo prodotto: ")) 
                        if sell_quantity<= 0:
                            raise ValueError ("La quantità deve essere un numero intero positivo")
                        break
                    except ValueError:
                        print ("Inserisci un valore valido per la quantità.")
            else: #if answer is no print the sell details
                partial_price=0
                for sell in partial_sell_list:
                    partial_price+=sell["total_price"] #calculates the total price based on the products sold per user
                    print(f"Vendita registrata: {sell['quantity']}X{sell['name']} {sell['sell_cost']} €")
                print(f"Totale: {partial_price:.2f} €")    
                break  # exit from while cycle

    def show_product(self):
        # Display the products in the inventory
        print("PRODOTTO QUANTITA PREZZO:")
        for product in self.product_list:
            print(f"{product['name']}, {product['quantity']}, {product['sell_cost']} €")


    def profits(self):
        #calculate profits
        gross_profit = sum(sell["total_price"]for sell in self.sell_list) #considering all products sold
        net_profit = gross_profit - sum(product["quantity"] * product["purchase_cost"]for product in self.product_list) 
        print(f"Profitti lordi: {gross_profit:.2f} €")
        print(f"Profitti netti: {net_profit:.2f} €")


    def help_menu (self):
         # Display available commands
        print("I comandi disponibili sono i seguenti:\n"+
                 "-aggiungi: aggiungi un prodotto al magazzino\n"+
                 "-elenca: elenca i prodotto in magazzino \n"+
                 "-vendita: registra una vendita effettuata \n"+
                 "-profitti: mostra i profitti totali \n"+
                 "-aiuto: mostra i possibili comandi \n" +
                 "-esci: esci dal programma \n")

    def save_file(self):
         # Save product information to a CSV file
        with open("inventory.csv", mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Name", "Quantity", "Purchase_cost", "Sell_cost"])
            for product in self.product_list:
                writer.writerow([product["name"], product["quantity"], product["purchase_cost"], product["sell_cost"]])

    def load_file(self):
         # Load in the lists product information from a CSV file
        try: #verify that the file exists
            with open("inventory.csv", mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    self.product_list.append({"name": row["Name"], "quantity": int(row["Quantity"]),
                                              "purchase_cost": float(row["Purchase_cost"]),
                                              "sell_cost": float(row["Sell_cost"])})
        except FileNotFoundError:
            print("Il file specificato non esiste. Caricamento iniziale del magazzino.")
            
# main function from which the various methods are called
def run_method():
    
    #creating an instance of the VeganShop class
    shop = VeganShop() 
    #calling the method of the VeganShop class
    shop.load_file() 
    shop.help_menu()

    while True:
        #try:
            
            cmd = (input("Inserisci un comando: "))

            if cmd == "aggiungi":
                product_name = input("Inserisci il nome del prodotto da aggiungere: ")
                while True:
                    try:
                        quantity = int(input("Inserisci la quantità: "))
                        #verify that quantity is a positive number
                        if quantity<=0:
                            raise ValueError("La quantità deve essere un numero intero positivo")
                        break 
                    except ValueError:
                        print ("inserisci un numero intero positivo")
                shop.add_product(product_name, quantity)

            elif cmd == "vendita":
                product_name = input("Inserisci il nome del prodotto da vendere: ")
                while True:
                    try:
                        sell_quantity = int(input("Inserisci la quantità da vendere: "))
                        if sell_quantity<=0:
                            raise ValueError("La quantità deve essere un numero intero positivo")
                        break 
                    except ValueError:
                        print ("inserisci un numero intero positivo")
                shop.product_sale(product_name, sell_quantity)

            elif cmd == "elenca":
                shop.show_product()

            elif cmd == "profitti":
                shop.profits()

            elif cmd == "aiuto":
                shop.help_manu()

            elif cmd == "esci":
                shop.save_file()
                break

            else:
                print("Scelta non valida. Riprova.")

        #except ValueError:
            #print("Inserisci un valore valido.")

run_method()

