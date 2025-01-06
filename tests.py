import sqlite3

def connect_to_database():
    conn = sqlite3.connect("airline_reservation.db")
    return conn

def register_user():
    conn = connect_to_database()
    cursor = conn.cursor()
    print("\n--- Εγγραφή Νέου Χρήστη ---")
    username = input("Όνομα χρήστη: ")
    email = input("Email: ")
    password = input("Κωδικός: ")

    try:
        cursor.execute("INSERT INTO XRHSTHS (Username, Email, Password) VALUES (?, ?, ?)", (username, email, password))
        conn.commit()
        print("Επιτυχής εγγραφή!")
        conn.close()
        return username  # Αυτόματα κάνει log in
    except sqlite3.IntegrityError:
        print("Σφάλμα: Το όνομα χρήστη ή το email χρησιμοποιούνται ήδη.")
        conn.close()
        return None

def login_user():
    conn = connect_to_database()
    cursor = conn.cursor()
    print("\n--- Σύνδεση ---")
    username = input("Όνομα χρήστη: ")
    password = input("Κωδικός: ")

    cursor.execute("SELECT * FROM XRHSTHS WHERE Username = ? AND Password = ?", (username, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        print("Σύνδεση επιτυχής!")
        return user[0]  # Επιστρέφει το ID του χρήστη
    else:
        print("Λάθος όνομα χρήστη ή κωδικός.")
        return None

def view_flights():
    conn = connect_to_database()
    cursor = conn.cursor()
    print("\n--- Διαθέσιμες Πτήσεις ---")

    query = """
    SELECT PTISEIS.FlightID, PTISEIS.Airline, 
           (SELECT AERODROMIA.Onoma FROM AERODROMIA WHERE AERODROMIA.Airport_Code = PTISEIS.Departure_Airport) AS Departure_Airport,
           (SELECT AERODROMIA.Onoma FROM AERODROMIA WHERE AERODROMIA.Airport_Code = PTISEIS.Arrival_Airport) AS Arrival_Airport,
           PTISEIS.Departure_Time, PTISEIS.Arrival_Time
    FROM PTISEIS
    """
    cursor.execute(query)
    flights = cursor.fetchall()

    for flight in flights:
        print(f"FlightID: {flight[0]}, Airline: {flight[1]}, Από: {flight[2]}, Προς: {flight[3]}, Αναχώρηση: {flight[4]}, Άφιξη: {flight[5]}")

    conn.close()

def select_flight(user_id):
    conn = connect_to_database()
    cursor = conn.cursor()
    print("\n--- Επιλογή Πτήσης ---")

    # Επιλογή πόλης αναχώρησης
    departure_city = input("Γράψτε την πόλη αναχώρησης: ")

    # Επιλογή πόλης προορισμού
    arrival_city = input("Γράψτε την πόλη προορισμού: ")

    # Αναζήτηση πτήσεων για τις δύο πόλεις
    query = """
    SELECT PTISEIS.FlightID, PTISEIS.Airline, 
           (SELECT AERODROMIA.Onoma FROM AERODROMIA WHERE AERODROMIA.Airport_Code = PTISEIS.Departure_Airport) AS Departure_Airport,
           (SELECT AERODROMIA.Onoma FROM AERODROMIA WHERE AERODROMIA.Airport_Code = PTISEIS.Arrival_Airport) AS Arrival_Airport,
           PTISEIS.Departure_Time, PTISEIS.Arrival_Time
    FROM PTISEIS
    WHERE Departure_Airport IN (SELECT Airport_Code FROM AERODROMIA WHERE Polh = ?)
      AND Arrival_Airport IN (SELECT Airport_Code FROM AERODROMIA WHERE Polh = ?)
    """
    cursor.execute(query, (departure_city, arrival_city))
    flights = cursor.fetchall()

    if not flights:
        print("Δεν βρέθηκαν διαθέσιμες πτήσεις για αυτήν τη διαδρομή.")
        conn.close()
        return

    # Εμφάνιση διαθέσιμων πτήσεων
    print("\n--- Διαθέσιμες Πτήσεις ---")
    for flight in flights:
        print(f"FlightID: {flight[0]}, Airline: {flight[1]}, Από: {flight[2]}, Προς: {flight[3]}, Αναχώρηση: {flight[4]}, Άφιξη: {flight[5]}")

    # Επιλογή πτήσης
    flight_id = input("Επιλέξτε το FlightID της πτήσης που θέλετε: ")

    # Ενημέρωση πίνακα "ΕΠΙΛΕΓΕΙ"
    try:
        query = """
        INSERT INTO EPILEGEI (ID_Xrhsth, FlightID, Date)
        VALUES (?, ?, datetime('now'))
        """
        cursor.execute(query, (user_id, flight_id))
        conn.commit()
    except Exception as e:
        print(f"Σφάλμα κατά την καταχώρηση στον πίνακα 'ΕΠΙΛΕΓΕΙ': {e}")
    finally:
        conn.close()

    # Δημιουργία Κράτησης
    create_reservation(user_id, flight_id)

def create_reservation(user_id, flight_id):
    conn = connect_to_database()
    cursor = conn.cursor()
    print("\n--- Δημιουργία Κράτησης ---")
    try:
        seats = int(input("Αριθμός θέσεων: "))

        # Επαναλαμβανόμενη ερώτηση για τον τύπο εισιτηρίου μέχρι να δοθεί έγκυρη απάντηση
        ticket_type = ""
        while ticket_type.lower() not in ["economy", "business", "first"]:
            ticket_type = input("Τύπος εισιτηρίου (Economy/Business/First): ")
            if ticket_type.lower() not in ["economy", "business", "first"]:
                print("Μη έγκυρος τύπος εισιτηρίου. Παρακαλώ επιλέξτε μεταξύ Economy, Business, ή First.")

        # Υπολογισμός τιμής
        ticket_price = 0
        if ticket_type.lower() == "economy":
            ticket_price = 70
        elif ticket_type.lower() == "business":
            ticket_price = 110
        elif ticket_type.lower() == "first":
            ticket_price = 170

        total_price = ticket_price * seats
        print(f"Συνολικό Κόστος: {total_price}€")

        # Εισαγωγή της κράτησης
        query = """
        INSERT INTO KRATHSEIS (ID_Xrhsth, FlightID, Seats, Type, Price)
        VALUES (?, ?, ?, ?, ?)
        """
        cursor.execute(query, (user_id, flight_id, seats, ticket_type, total_price))
        reservation_id = cursor.lastrowid  # Παίρνουμε το ID της κράτησης

        # Ενημέρωση πίνακα "Κάνει"
        kanei_query = """
        INSERT INTO KANEI (ID_Xrhsth, Reservation_ID, Date)
        VALUES (?, ?, datetime('now'))
        """
        cursor.execute(kanei_query, (user_id, reservation_id))

        conn.commit()

        # Εισαγωγή των πελατών
        for _ in range(seats):
            print("\n--- Στοιχεία Πελάτη ---")
            fname = input("Όνομα: ")
            lname = input("Επώνυμο: ")
            phone_number = input("Αριθμός Τηλεφώνου: ")
            passport_number = input("Αριθμός Διαβατηρίου: ")

            customer_query = """
            INSERT INTO PELATHS (Fname, Lname, Phone_Number, Ar_Diavathriou, ID_Xrhsth)
            VALUES (?, ?, ?, ?, ?)
            """
            cursor.execute(customer_query, (fname, lname, phone_number, passport_number, user_id))

            # Ενημέρωση πίνακα "Εγγράφει"
            customer_id = cursor.lastrowid
            eggrafei_query = """
            INSERT INTO EGGRAFEI (ID_Xrhsth, ID_Pelath)
            VALUES (?, ?)
            """
            cursor.execute(eggrafei_query, (user_id, customer_id))

        conn.commit()
        print("Η κράτηση ολοκληρώθηκε επιτυχώς!")
    except Exception as e:
        print(f"Σφάλμα κατά την κράτηση: {e}")
    finally:
        conn.close()

def review_flight(user_id):
    conn = connect_to_database()
    cursor = conn.cursor()
    print("\n--- Αξιολόγηση Πτήσης ---")

    try:
        # Εύρεση πτήσεων του χρήστη
        query = """
        SELECT KRATHSEIS.Reservation_ID, 
               PTISEIS.FlightID, 
               PTISEIS.Airline, 
               (SELECT AERODROMIA.Onoma FROM AERODROMIA WHERE AERODROMIA.Airport_Code = PTISEIS.Departure_Airport) AS Departure_Airport,
               (SELECT AERODROMIA.Onoma FROM AERODROMIA WHERE AERODROMIA.Airport_Code = PTISEIS.Arrival_Airport) AS Arrival_Airport,
               PTISEIS.Departure_Time, 
               PTISEIS.Arrival_Time
        FROM KRATHSEIS
        JOIN PTISEIS ON KRATHSEIS.FlightID = PTISEIS.FlightID
        WHERE KRATHSEIS.ID_Xrhsth = ?
        """
        cursor.execute(query, (user_id,))
        flights = cursor.fetchall()

        if not flights:
            print("Δεν υπάρχουν πτήσεις καταχωρημένες για αυτόν τον χρήστη.")
            return

        print("\n--- Οι Πτήσεις σας ---")
        for flight in flights:
            print(f"Reservation ID: {flight[0]}, FlightID: {flight[1]}, Airline: {flight[2]}, Από: {flight[3]}, Προς: {flight[4]}, Αναχώρηση: {flight[5]}, Άφιξη: {flight[6]}")

        if len(flights) > 1:
            reservation_id = input("Γράψτε το Reservation ID της πτήσης που θέλετε να αξιολογήσετε: ")
        else:
            reservation_id = flights[0][0]

        rating = int(input("Βαθμολογία (1-10): "))
        comment = input("Σχόλια: ")
        favorite_destination = input("Αγαπημένος προορισμός (προαιρετικά, πατήστε Enter για να παραλείψετε): ")
        if not favorite_destination:
            favorite_destination = None

        query = """
        INSERT INTO AXIOLOGHSH (ID_Xrhsth, Vathmos, Sxolia, Agaphmenos_Proorismos)
        VALUES (?, ?, ?, ?)
        """
        cursor.execute(query, (user_id, rating, comment, favorite_destination))
        review_id = cursor.lastrowid

        # Ενημέρωση πίνακα "Γράφει"
        grafei_query = """
        INSERT INTO GRAFEI (ID_Xrhsth, ID_Axiologhshs, Date)
        VALUES (?, ?, datetime('now'))
        """
        cursor.execute(grafei_query, (user_id, review_id))

        conn.commit()
        print("Η αξιολόγηση καταχωρήθηκε επιτυχώς!")
    except Exception as e:
        print(f"Σφάλμα κατά την αξιολόγηση: {e}")
    finally:
        conn.close()

def main():
    print("Καλώς ήρθατε στο Σύστημα Κρατήσεων!")
    user_id = None

    while not user_id:
        print("\n1. Εγγραφή\n2. Σύνδεση")
        choice = input("Επιλέξτε: ")

        if choice == "1":
            user_id = register_user()
        elif choice == "2":
            user_id = login_user()
        else:
            print("Μη έγκυρη επιλογή. Δοκιμάστε ξανά.")

    while True:
        print("\n--- Κύριο Μενού ---")
        print("1. Εμφάνιση Πτήσεων")
        print("2. Επιλογή Πτήσης και Δημιουργία Κράτησης")
        print("3. Αξιολόγηση Πτήσης")
        print("4. Έξοδος")
        choice = input("Επιλέξτε: ")

        if choice == "1":
            view_flights()
        elif choice == "2":
            select_flight(user_id)
        elif choice == "3":
            review_flight(user_id)
        elif choice == "4":
            print("Ευχαριστούμε που χρησιμοποιήσατε την εφαρμογή μας!")
            break
        else:
            print("Μη έγκυρη επιλογή. Δοκιμάστε ξανά.")

if __name__ == "__main__":
    main()
