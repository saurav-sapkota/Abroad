import datetime
import os


def initialize_files():
    # Data for each file
    files = {
        "vehicles.txt": """BKV-943,Ford Fiesta,35,Manual Transmission
JMB-535,Ford Fiesta,48,Air Conditioning,Manual Transmission
SKF-124,Ford Focus,52,Air Conditioning,Manual Transmission
MSQ-731,Ford Focus Wagon,52,Air Conditioning,Manual Transmission
AMG-111,Toyota Yaris,65,Air Conditioning,Hybrid,Automatic Transmission
MER-611,Kia Rio,52,Air Conditioning,Manual Transmission
ZEQ-851,Toyota Corolla Touring Sports,63,Air Conditioning,Hybrid,Automatic Transmission
CHF-337,Volkswagen Up,58,Air Conditioning,Manual Transmission
BMC-69,Nissan Micra,42,Manual Transmission
TTC-513,Volkswagen Golf,51,Air Conditioning,Manual Transmission
VIG-326,Nissan Micra,43,Manual Transmission
DKG-477,Toyota Corolla,52,Air Conditioning,Manual Transmission
HYA-544,Toyota Yaris,66,Hybrid,Automatic Transmission
XJY-604,Volkswagen Polo,62,Air Conditioning,Automatic Transmission
AJB-123,SEAT Ibiza,65,Air Conditioning,Automatic Transmission
MDZ-471,Skoda Kodiaq,71,Air Conditioning,Automatic Transmission
TUS-674,Volkswagen T-Cross,72,Air Conditioning,Manual Transmission
WYN-482,Mercedes A-Class,90,Air Conditioning,Manual Transmission
KOL-99,Audi Q5,110,Air Conditioning,Automatic Transmission
""",
        "ongoing.txt": """AJB-123,07/07/1977,21/10/2024 10:31
TTC-513,28/01/2002,23/10/2024 14:32
MER-611,14/07/2000,24/10/2024 10:46
ZEQ-851,16/10/2001,24/10/2024 15:45
CHF-337,22/02/1961,25/10/2024 12:33
MSQ-731,05/05/1995,28/10/2024 13:29
""",
        "customers.txt": """12/12/1985,Alice,Wonder,Alice.Wonder@outlook.com
23/03/1990,Mark,Smith,Mark.Smith@hotmail.com
05/05/1995,Emma,Stone,Emma.Stone@live.com
11/11/1988,David,Lee,David.Lee@aol.com
30/06/1992,Sarah,Connor,Sarah.Connor@gmail.com
22/02/1961,James,Bond,James.Bond@mi6.co.uk
07/07/1977,John,Lucky,John.Lucky@email.com
09/09/1999,Tom,Shark,Tom.Shark@gmail.com
28/01/2002,Laura,Driver,Laura.Driver@garage.fi
17/04/1997,Jia,Mei,Jia.Mei@163.com
17/08/1978,Jack,Mobile,Jack.Mobile@yahoo.com
16/10/2001,Tom,Johanson,Tom.Johanson@gmail.com
14/07/2000,Matti,Virtanen,Matti.Virtanen@lut.fi
""",
        "transactions.txt": """XJY-604,23/03/1990,01/10/2024 11:15,05/10/2024 20:10,5,310.00
MER-611,05/05/1995,10/10/2024 08:00,15/10/2024 16:30,6,312.00
BMC-69,17/04/1997,15/10/2024 14:01,19/10/2024 22:20,5,210.00
VIG-326,17/08/1978,13/10/2024 12:23,20/10/2024 14:03,8,344.00
KOL-99,11/11/1988,15/10/2024 14:45,22/10/2024 19:20,8,880.00
AJB-123,12/12/1985,20/10/2024 09:30,25/10/2024 18:45,6,390.00
TTC-513,30/06/1992,25/10/2024 10:05,28/10/2024 21:50,4,204.00
"""
    }

    for filename, data in files.items():
        if not os.path.exists(filename):
            with open(filename, 'w') as file:
                file.write(data)
            print(f"Created {filename}.")


def show_menu():
    print("\nCar Rental Management System")
    print("1. List available cars")
    print("2. Rent a car")
    print("3. Return a car")
    print("4. Count the money")
    print("5. Exit")
    return input("Enter your choice: ")


def list_available_cars():
    try:
        with open('vehicles.txt', 'r') as vehicles, open('ongoing.txt', 'r') as ongoing:
            ongoing_cars = {line.split(',')[0] for line in ongoing.readlines()}
            print("\nAvailable Cars:")
            print("-----------------------------------------------------")
            for line in vehicles:
                car = line.strip().split(',')
                if car[0] not in ongoing_cars:
                    print(", ".join(car))
            print("-----------------------------------------------------")
    except FileNotFoundError:
        print("Error: vehicles.txt or ongoing.txt not found.")


def rent_a_car():
    try:
        reg_plate = input("\nEnter the registration plate of the car: ").strip()
        with open('vehicles.txt', 'r') as vehicles:
            car_found = False
            for line in vehicles:
                car = line.strip().split(',')
                if car[0] == reg_plate:
                    car_found = True
                    break
            if not car_found:
                print("Car not found in the system!")
                return

        birthdate = input("Enter your birthdate (DD/MM/YYYY): ").strip()
        customer_found = False

        with open('customers.txt', 'r') as customers:
            for line in customers:
                if line.strip().split(',')[0] == birthdate:
                    customer_found = True
                    print("Welcome back, returning customer!")
                    break

        if not customer_found:
            name = input("Enter your full name: ").strip()
            with open('customers.txt', 'a') as customers:
                customers.write(f"{birthdate},{name}\n")

        start_time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
        with open('ongoing.txt', 'a') as ongoing:
            ongoing.write(f"{reg_plate},{birthdate},{start_time}\n")
        print("Car rental logged successfully.")

    except FileNotFoundError:
        print("Error: Required files are missing!")


def return_a_car():
    try:
        reg_plate = input("\nEnter the registration plate of the car being returned: ").strip()
        end_time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")

        found = False
        updated_ongoing = []
        rental_info = None

        with open('ongoing.txt', 'r') as ongoing:
            for line in ongoing:
                data = line.strip().split(',')
                if data[0] == reg_plate:
                    found = True
                    rental_info = data
                else:
                    updated_ongoing.append(line.strip())

        if not found:
            print("Rental not found!")
            return

        with open('ongoing.txt', 'w') as ongoing:
            ongoing.write("\n".join(updated_ongoing) + "\n")

        start_time = datetime.datetime.strptime(rental_info[2], "%d/%m/%Y %H:%M")
        end_time_dt = datetime.datetime.strptime(end_time, "%d/%m/%Y %H:%M")
        duration_days = (end_time_dt - start_time).days + 1

        with open('vehicles.txt', 'r') as vehicles:
            for line in vehicles:
                car = line.strip().split(',')
                if car[0] == reg_plate:
                    daily_rate = float(car[2])
                    break

        total_price = duration_days * daily_rate

        with open('transactions.txt', 'a') as transactions:
            transactions.write(f"{reg_plate},{rental_info[1]},{rental_info[2]},{end_time},{duration_days},{total_price:.2f}\n")

        print(f"Car returned successfully. Total price: {total_price:.2f}")

    except FileNotFoundError:
        print("Error: Required files are missing!")


def count_money():
    try:
        total = 0.0
        with open('transactions.txt', 'r') as transactions:
            for line in transactions:
                total += float(line.strip().split(',')[-1])
        print(f"\nTotal money earned: {total:.2f}")
    except FileNotFoundError:
        print("Error: transactions.txt not found.")


def main():
    # Ensure the necessary files are initialized
    initialize_files()
    
    while True:
        choice = show_menu()
        if choice == '1':
            list_available_cars()
        elif choice == '2':
            rent_a_car()
        elif choice == '3':
            return_a_car()
        elif choice == '4':
            count_money()
        elif choice == '5':
            print("Exiting system...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()