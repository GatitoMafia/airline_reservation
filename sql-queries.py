import sqlite3

# Function to execute a query and display the result
def execute_query_and_print(query, query_description):
    conn = sqlite3.connect('airline_reservation.db')  # Adjust to your database name if necessary
    cursor = conn.cursor()
    try:
        cursor.execute(query)
        results = cursor.fetchall()
        print(f"{query_description}\n")
        for row in results:
            print(row)
        print("\n" + "-"*80 + "\n")
    except sqlite3.Error as e:
        print(f"An error occurred while executing {query_description}: {e}")
    conn.close()

# List of queries and their descriptions (in order from the txt file)
queries = [
    ("Αναζήτηση πτήσεων με συγκεκριμένο εύρος τιμών",
     """
     SELECT KRATHSEIS.FlightID, KRATHSEIS.Price
     FROM KRATHSEIS
     WHERE KRATHSEIS.Price BETWEEN 300 AND 400;
     """),
    ("Αναζήτηση πτήσεων με συγκεκριμένη ημερομηνία",
     """
     SELECT PTISEIS.FlightID, PTISEIS.Airline, PTISEIS.Departure_Airport, PTISEIS.Arrival_Airport, 
            PTISEIS.Departure_Time, PTISEIS.Arrival_Time
     FROM PTISEIS
     WHERE DATE(PTISEIS.Departure_Time) = '2025-01-15'; 
     """),
    ("Εμφάνιση πτήσεων που αναχωρούν από συγκεκριμένο αεροδρόμιο",
     """
     SELECT PTISEIS.FlightID, PTISEIS.Airline, AERODROMIA.Onoma AS Departure_Airport, 
            PTISEIS.Arrival_Airport, PTISEIS.Departure_Time, PTISEIS.Arrival_Time
     FROM PTISEIS
     JOIN AERODROMIA ON PTISEIS.Departure_Airport = AERODROMIA.Airport_Code
     WHERE AERODROMIA.Airport_Code = 'AP003'; 
     """),
    ("Εμφάνιση των κρατήσεων 2 θέσεων που τα status είναι confirmed",
     """
     SELECT KRATHSEIS.Reservation_ID, KRATHSEIS.Seats, KRATHSEIS.Status
     FROM KRATHSEIS
     WHERE KRATHSEIS.Seats = 2 AND KRATHSEIS.Status = 'confirmed';
     """),
    ("Για τις επιβεβαιωμένες κρατήσεις άνω των 300 ευρώ να βρείτε το αεροδρόμιο και τη χώρα επιβίβασης καθώς και το email του χρήστη που έκανε την κράτηση",
     """
     SELECT KRATHSEIS.Reservation_ID, KRATHSEIS.Seats, KRATHSEIS.Price, KRATHSEIS.Status,
            AERODROMIA.Onoma AS Departure_Airport, AERODROMIA.Xwra AS Departure_Country,
            XRHSTHS.Email
     FROM KRATHSEIS
     JOIN PTISEIS ON KRATHSEIS.FlightID = PTISEIS.FlightID
     JOIN AERODROMIA ON PTISEIS.Departure_Airport = AERODROMIA.Airport_Code
     JOIN XRHSTHS ON KRATHSEIS.ID_Xrhsth = XRHSTHS.ID
     WHERE KRATHSEIS.Status = 'confirmed' AND KRATHSEIS.Price > 300;
     """),
    ("Για τις επιβεβαιωμένες κρατήσεις που έγιναν στην εταιρία 'Aegean Airlines' να βρείτε το αεροδρόμιο και τη χώρα αποβίβασης καθώς και το email του χρήστη που έκανε την κράτηση",
     """
     SELECT KRATHSEIS.Reservation_ID, KRATHSEIS.Status,
            PTISEIS.Airline,
            AERODROMIA.Onoma AS Arrival_Airport, AERODROMIA.Xwra AS Arrival_Country,
            XRHSTHS.Email
     FROM KRATHSEIS
     JOIN PTISEIS ON KRATHSEIS.FlightID = PTISEIS.FlightID
     JOIN AERODROMIA ON PTISEIS.Arrival_Airport = AERODROMIA.Airport_Code
     JOIN XRHSTHS ON KRATHSEIS.ID_Xrhsth = XRHSTHS.ID
     WHERE KRATHSEIS.Status = 'confirmed' AND PTISEIS.Airline = 'Aegean Airlines';
     """),
    ("Eμφάνισε τους 10 πιο δημοφιλείς προορισμούς",
     """
     SELECT AERODROMIA.Onoma AS Destination_Airport, AERODROMIA.Polh AS Destination_City,
            AERODROMIA.Xwra AS Destination_Country, COUNT(KRATHSEIS.Reservation_ID) AS Total_Bookings
     FROM KRATHSEIS
     JOIN PTISEIS ON KRATHSEIS.FlightID = PTISEIS.FlightID
     JOIN AERODROMIA ON PTISEIS.Arrival_Airport = AERODROMIA.Airport_Code
     GROUP BY AERODROMIA.Onoma, AERODROMIA.Polh, AERODROMIA.Xwra
     ORDER BY Total_Bookings DESC
     LIMIT 10; 
     """),
    ("Εμφάνιση πτήσεων με ενδιάμεση στάση και πού γίνεται αυτή",
     """
     SELECT PTISEIS.FlightID, PTISEIS.Airline, AERODROMIA.Onoma AS Stop_Airport, AERODROMIA.Xwra AS Stop_Country
     FROM PTISEIS
     JOIN AERODROMIA ON PTISEIS.Stops = AERODROMIA.Airport_Code
     WHERE PTISEIS.Stops IS NOT NULL;
     """),
    ("Εμφάνιση του συνολικού εισοδήματος κάθε αεροπορικής εταιρίας από τις πτήσεις της",
     """
     SELECT PTISEIS.Airline, SUM(KRATHSEIS.Price) AS Total_Revenue
     FROM KRATHSEIS
     JOIN PTISEIS ON KRATHSEIS.FlightID = PTISEIS.FlightID
     WHERE KRATHSEIS.Status = 'confirmed'
     GROUP BY PTISEIS.Airline
     ORDER BY Total_Revenue DESC;
     """),
     ("Εμφάνισε τον συνολικό μέσο όρο αξιολόγησης των πελατών",
      """
      SELECT AVG(AXIOLOGHSH.Vathmos) AS Overall_Avg_Rating
      FROM AXIOLOGHSH;
      """),
      ("Εμφάνισε τις πτήσεις μαζί με το σύνολo κρατήσεων για κάθε πτήση",
       """
        SELECT 
        PTISEIS.FlightID,
        PTISEIS.Airline,
        PTISEIS.Departure_Time,
        PTISEIS.Arrival_Time,
        COUNT(KRATHSEIS.Reservation_ID) AS Total_Bookings
        FROM 
        PTISEIS
        JOIN 
        KRATHSEIS ON PTISEIS.FlightID = KRATHSEIS.FlightID
        GROUP BY 
        PTISEIS.FlightID, PTISEIS.Airline, PTISEIS.Departure_Time, PTISEIS.Arrival_Time
        ORDER BY 
        Total_Bookings DESC;
        """),
        ("Εμφάνισε τις πτήσεις με το συνολικό αριθμό επιβατών που έχουν κάνει κράτηση για κάθε πτήση",
         """
        SELECT 
        PTISEIS.FlightID,
        PTISEIS.Airline,
        PTISEIS.Departure_Time,
        PTISEIS.Arrival_Time,
        SUM(KRATHSEIS.Seats) AS Total_Passengers
        FROM 
        PTISEIS
        JOIN 
        KRATHSEIS ON PTISEIS.FlightID = KRATHSEIS.FlightID
        WHERE 
        KRATHSEIS.Status = 'confirmed' 
        GROUP BY PTISEIS.FlightID, PTISEIS.Airline, PTISEIS.Departure_Time, PTISEIS.Arrival_Time
        ORDER BY Total_Passengers DESC;
        """),
        ("Βρες τις πτήσεις που έχουν επιβεβαιωμένες κρατήσεις σε ένα συγκεκριμένο χρονικό διάστημα",
         """
        SELECT 
        PTISEIS.FlightID,
        PTISEIS.Airline,
        PTISEIS.Departure_Time,
        PTISEIS.Arrival_Time,
        SUM(KRATHSEIS.Seats) AS Total_Passengers
        FROM 
        PTISEIS
        JOIN 
        KRATHSEIS ON PTISEIS.FlightID = KRATHSEIS.FlightID
        WHERE KRATHSEIS.Status = 'confirmed' 
        AND PTISEIS.Departure_Time BETWEEN '2025-01-01' AND '2025-01-31' -- Χρονικό φίλτρο
        GROUP BY PTISEIS.FlightID, PTISEIS.Airline, PTISEIS.Departure_Time, PTISEIS.Arrival_Time
        ORDER BY PTISEIS.Departure_Time ASC;
        """),
        ("Για κάθε αεροδρόμιο, εμφάνισε τον αριθμό των πτήσεων που αναχωρούν από εκεί.",
         """
        SELECT 
        AERODROMIA.Airport_Code,
        AERODROMIA.Onoma AS Airport_Name,
        AERODROMIA.Polh AS City,
        AERODROMIA.Xwra AS Country,
        COUNT(PTISEIS.FlightID) AS Total_Departures
        FROM AERODROMIA
        JOIN 
        PTISEIS ON AERODROMIA.Airport_Code = PTISEIS.Departure_Airport
        GROUP BY AERODROMIA.Airport_Code, AERODROMIA.Onoma, AERODROMIA.Polh, AERODROMIA.Xwra
        ORDER BY Total_Departures DESC;
        """),
        ("Για κάθε αεροδρόμιο, εμφάνισε τον αριθμό των πτήσεων που φτάνουν σε αυτό.",
         """
        SELECT 
        AERODROMIA.Airport_Code,
        AERODROMIA.Onoma AS Airport_Name,
        AERODROMIA.Polh AS City,
        AERODROMIA.Xwra AS Country,
        COUNT(PTISEIS.FlightID) AS Total_Arrivals
        FROM AERODROMIA
        JOIN 
        PTISEIS ON AERODROMIA.Airport_Code = PTISEIS.Arrival_Airport
        GROUP BY AERODROMIA.Airport_Code, AERODROMIA.Onoma, AERODROMIA.Polh, AERODROMIA.Xwra
        ORDER BY Total_Arrivals DESC;
        """),
        ("Βρες τα αεροδρόμια που είναι τόσο αναχωρητήρια όσο και προορισμοί",
         """
        SELECT 
        AERODROMIA.Airport_Code,
        AERODROMIA.Onoma AS Airport_Name,
        AERODROMIA.Polh AS City,
        AERODROMIA.Xwra AS Country,
        COUNT(DISTINCT PTISEIS1.FlightID) AS Total_Departures,
        COUNT(DISTINCT PTISEIS2.FlightID) AS Total_Arrivals
        FROM AERODROMIA
        JOIN 
        PTISEIS AS PTISEIS1 ON AERODROMIA.Airport_Code = PTISEIS1.Departure_Airport
        JOIN 
        PTISEIS AS PTISEIS2 ON AERODROMIA.Airport_Code = PTISEIS2.Arrival_Airport
        WHERE PTISEIS1.FlightID IS NOT NULL AND PTISEIS2.FlightID IS NOT NULL
        GROUP BY AERODROMIA.Airport_Code, AERODROMIA.Onoma, AERODROMIA.Polh, AERODROMIA.Xwra
        ORDER BY Total_Departures DESC, Total_Arrivals DESC;
        """),
        ("Βρες τους χρήστες που έχουν δώσει βαθμολογία μεγαλύτερη από 8",
         """
        SELECT 
        XRHSTHS.Username,
        XRHSTHS.Email,
        AXIOLOGHSH.Vathmos,
        AXIOLOGHSH.Sxolia,
        AXIOLOGHSH.Hmeromhnia
        FROM AXIOLOGHSH
        JOIN 
        XRHSTHS ON AXIOLOGHSH.ID_Xrhsth = XRHSTHS.ID
        WHERE AXIOLOGHSH.Vathmos > 8
        ORDER BY AXIOLOGHSH.Vathmos DESC;
        """),
        ("Βρες τους πιο δημοφιλείς προορισμούς με βάση τις αξιολογήσεις που έχουν δοθεί.",
         """
        SELECT 
        AXIOLOGHSH.Agaphmenos_Proorismos AS Popular_Destination,
        COUNT(AXIOLOGHSH.Agaphmenos_Proorismos) AS Total_Ratings
        FROM AXIOLOGHSH
        WHERE AXIOLOGHSH.Agaphmenos_Proorismos IS NOT NULL
        GROUP BY AXIOLOGHSH.Agaphmenos_Proorismos
        ORDER BY Total_Ratings DESC, Popular_Destination ASC;
        """)
    # Add more queries here
]

# Execute all queries
for i, (description, query) in enumerate(queries, 1):
    execute_query_and_print(query, f"Query {i}: {description}")
