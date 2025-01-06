import sqlite3

# Σύνδεση με τη βάση δεδομένων μας
conn = sqlite3.connect("airline_reservation.db")
cursor = conn.cursor()

# Insert ΧΡΗΣΤΗΣ
def insert_xrhsths():
    with open("XRHSTHS_100.txt", "r", encoding="utf-8") as file:
        lines = file.readlines()
    for line in lines:
        id, username, password, email = line.strip().split("\t")
        cursor.execute("INSERT INTO XRHSTHS (ID, Username, Password, Email) VALUES (?, ?, ?, ?)",
                       (id, username, password, email))
    conn.commit()

# Insert ΠΕΛΑΤΗΣ
def insert_pelaths():
    with open("PELATHS.txt", "r", encoding="utf-8") as file:
        lines = file.readlines()
    for line in lines:
        id_pelath, fname, lname, phone_number, ar_diavathriou, id_xrhsth = line.strip().split("\t")
        cursor.execute("INSERT INTO PELATHS (ID_Pelath, Fname, Lname, Phone_Number, Ar_Diavathriou, ID_Xrhsth) VALUES (?, ?, ?, ?, ?, ?)",
                       (id_pelath, fname, lname, phone_number, ar_diavathriou, id_xrhsth))
    conn.commit()

# Insert ΑΕΡΟΔΡΟΜΙΑ
def insert_aerodromia():
    with open("AERODROMIA.txt", "r", encoding="utf-8") as file:
        lines = file.readlines()
    for line in lines:
        airport_code, onoma, polh, xwra = line.strip().split("\t")
        cursor.execute("INSERT INTO AERODROMIA (Airport_Code, Onoma, Polh, Xwra) VALUES (?, ?, ?, ?)",
                       (airport_code, onoma, polh, xwra))
    conn.commit()

# Insert ΠΤΗΣΕΙΣ
def insert_ptiseis():
    with open("PTISEIS.txt", "r", encoding="utf-8") as file:
        lines = file.readlines()
    for line in lines:
        flight_id, airline, dep_airport, arr_airport, dep_time, arr_time, stops = line.strip().split("\t")
        cursor.execute("INSERT INTO PTISEIS (FlightID, Airline, Departure_Airport, Arrival_Airport, Departure_Time, Arrival_Time, Stops) VALUES (?, ?, ?, ?, ?, ?, ?)",
                       (flight_id, airline, dep_airport, arr_airport, dep_time, arr_time, stops))
    conn.commit()

# Insert ΚΡΑΤΗΣΕΙΣ
def insert_krathseis():
    with open("KRATHSEIS.txt", "r", encoding="utf-8") as file:
        lines = file.readlines()
    for line in lines:
        reservation_id, id_xrhsth, flight_id, seats, type, booking_date, status, price = line.strip().split("\t")
        # Εισαγωγή δεδομένων με τη σωστή σειρά πεδίων
        cursor.execute(
            "INSERT INTO KRATHSEIS (Reservation_ID, ID_Xrhsth, FlightID, Seats, Type, Booking_Date, Status, Price) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (reservation_id, id_xrhsth, flight_id, seats, type, booking_date, status, price)
        )
    conn.commit()

# Insert ΑΞΙΟΛΟΓΗΣΗ
def insert_axiologhsh():
    with open("AXIOLOGHSH.txt", "r", encoding="utf-8") as file:
        lines = file.readlines()
    for line in lines:
        id_axiologhshs, id_xrhsth, hmeromhnia, sxolia, vathmos, agaphmenos_proorismos = line.strip().split("\t")
        cursor.execute("INSERT INTO AXIOLOGHSH (ID_Axiologhshs, ID_Xrhsth, Hmeromhnia, Sxolia, Vathmos, Agaphmenos_Proorismos) VALUES (?, ?, ?, ?, ?, ?)",
                       (id_axiologhshs, id_xrhsth, hmeromhnia, sxolia, vathmos, agaphmenos_proorismos))
    conn.commit()

# Insert GRAFEI
def insert_grafei():
    with open("GRAFEI.txt", "r", encoding="utf-8") as file:
        lines = file.readlines()
    for line in lines:
        id_xrhsth, id_axiologhshs, date = line.strip().split("\t")
        cursor.execute("INSERT INTO GRAFEI (ID_Xrhsth, ID_Axiologhshs, Date) VALUES (?, ?, ?)",
                       (id_xrhsth, id_axiologhshs, date))
    conn.commit()

# Insert EPLEGEI
def insert_eplegei():
    with open("EPLEGEI.txt", "r", encoding="utf-8") as file:
        lines = file.readlines()
    for line in lines:
        id_xrhsth, flight_id, date = line.strip().split("\t")
        cursor.execute("INSERT INTO EPILEGEI (ID_Xrhsth, FlightID, Date) VALUES (?, ?, ?)",
                       (id_xrhsth, flight_id, date))
    conn.commit()

# Insert EGGRAFEI
def insert_eggrafei():
    with open("EGGRAFEI.txt", "r", encoding="utf-8") as file:
        lines = file.readlines()
    for line in lines:
        id_xrhsth, id_pelath = line.strip().split("\t")
        cursor.execute("INSERT INTO EGGRAFEI (ID_Xrhsth, ID_Pelath) VALUES (?, ?)",
                       (id_xrhsth, id_pelath))
    conn.commit()

# Insert KANEI
def insert_kanei():
    with open("KANEI.txt", "r", encoding="utf-8") as file:
        lines = file.readlines()
    for line in lines:
        id_xrhsth, reservation_id, date = line.strip().split("\t")
        cursor.execute("INSERT INTO KANEI (ID_Xrhsth, Reservation_ID, Date) VALUES (?, ?, ?)",
                       (id_xrhsth, reservation_id, date))
    conn.commit()

# Εκτέλεση των λειτουργιών εισαγωγής
insert_xrhsths()
insert_pelaths()
insert_aerodromia()
insert_ptiseis()
insert_axiologhsh()
insert_grafei()
insert_eggrafei()
insert_kanei()
insert_krathseis()
insert_eplegei()

# Κλείσιμο της σύνδεσης
conn.close()
