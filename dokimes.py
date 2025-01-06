import sqlite3

# Σύνδεση με τη Βάση Δεδομένων
conn = sqlite3.connect('airline_reservation.db')  # Δημιουργεί/Συνδέεται με τη βάση
cursor = conn.cursor()

# Δημιουργία της βάσης δεδομένων
create_complete_database_query = """
-- Πίνακας ΧΡΗΣΤΗΣ
CREATE TABLE IF NOT EXISTS "XRHSTHS" (
    "ID" INTEGER PRIMARY KEY AUTOINCREMENT,
    "Username" VARCHAR(50) NOT NULL UNIQUE,
    "Password" VARCHAR(50) NOT NULL,
    "Email" VARCHAR(100) NOT NULL UNIQUE
);

-- Πίνακας ΠΕΛΑΤΗΣ
CREATE TABLE IF NOT EXISTS "PELATHS" (
    "ID_Pelath" INTEGER PRIMARY KEY AUTOINCREMENT,
    "Fname" VARCHAR(50) NOT NULL,
    "Lname" VARCHAR(50) NOT NULL,
    "Phone_Number" VARCHAR(15),
    "Ar_Diavathriou" VARCHAR(20) UNIQUE,
    "ID_Xrhsth" INTEGER NOT NULL,
    FOREIGN KEY ("ID_Xrhsth") REFERENCES "XRHSTHS" ("ID")
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

-- Πίνακας ΠΤΗΣΕΙΣ
CREATE TABLE IF NOT EXISTS "PTISEIS" (
    "FlightID" INTEGER PRIMARY KEY AUTOINCREMENT,
    "Airline" VARCHAR(50) NOT NULL,
    "Departure_Airport" VARCHAR(10) NOT NULL,
    "Arrival_Airport" VARCHAR(10) NOT NULL,
    "Departure_Time" DATETIME NOT NULL,
    "Arrival_Time" DATETIME NOT NULL,
    "Stops" VARCHAR(10),
    FOREIGN KEY ("Departure_Airport") REFERENCES "AERODROMIA" ("Airport_Code"),
    FOREIGN KEY ("Arrival_Airport") REFERENCES "AERODROMIA" ("Airport_Code"),
    FOREIGN KEY ("Stops") REFERENCES "AERODROMIA" ("Airport_Code")
);

-- Πίνακας ΑΕΡΟΔΡΟΜΙΑ
CREATE TABLE IF NOT EXISTS "AERODROMIA" (
    "Airport_Code" VARCHAR(10) PRIMARY KEY,
    "Onoma" VARCHAR(100) NOT NULL,
    "Polh" VARCHAR(50) NOT NULL,
    "Xwra" VARCHAR(50) NOT NULL
);

-- Πίνακας ΚΡΑΤΗΣΕΙΣ
CREATE TABLE IF NOT EXISTS "KRATHSEIS" (
    "Reservation_ID" INTEGER PRIMARY KEY AUTOINCREMENT,
    "ID_Xrhsth" INTEGER NOT NULL,
    "FlightID" INTEGER NOT NULL,
    "Seats" INTEGER NOT NULL,
    "Booking_Date" DATETIME DEFAULT CURRENT_TIMESTAMP,
    "Status" VARCHAR(20) DEFAULT 'confirmed',
    "Price" REAL NOT NULL,
    "Type" VARCHAR(20) NOT NULL,
    FOREIGN KEY ("ID_Xrhsth") REFERENCES "XRHSTHS" ("ID")
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    FOREIGN KEY ("FlightID") REFERENCES "PTISEIS" ("FlightID")
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

-- Πίνακας ΑΞΙΟΛΟΓΗΣΗ
CREATE TABLE IF NOT EXISTS "AXIOLOGHSH" (
    "ID_Axiologhshs" INTEGER PRIMARY KEY AUTOINCREMENT,
    "ID_Xrhsth" INTEGER NOT NULL,
    "Hmeromhnia" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "Sxolia" TEXT,
    "Vathmos" INTEGER NOT NULL,
    "Agaphmenos_Proorismos" VARCHAR(50),
    FOREIGN KEY ("ID_Xrhsth") REFERENCES "XRHSTHS" ("ID")
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

-- Πίνακας GRAFEI (ΧΡΗΣΤΗΣ -> ΑΞΙΟΛΟΓΗΣΗ)
CREATE TABLE IF NOT EXISTS "GRAFEI" (
    "ID_Xrhsth" INTEGER NOT NULL,
    "ID_Axiologhshs" INTEGER NOT NULL,
    "Date" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY ("ID_Xrhsth", "ID_Axiologhshs"),
    FOREIGN KEY ("ID_Xrhsth") REFERENCES "XRHSTHS" ("ID")
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    FOREIGN KEY ("ID_Axiologhshs") REFERENCES "AXIOLOGHSH" ("ID_Axiologhshs")
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

-- Πίνακας EPILEGEI (ΧΡΗΣΤΗΣ -> ΠΤΗΣΗ)
CREATE TABLE IF NOT EXISTS "EPILEGEI" (
    "ID_Xrhsth" INTEGER NOT NULL,
    "FlightID" INTEGER NOT NULL,
    "Date" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY ("ID_Xrhsth", "FlightID"),
    FOREIGN KEY ("ID_Xrhsth") REFERENCES "XRHSTHS" ("ID")
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    FOREIGN KEY ("FlightID") REFERENCES "PTISEIS" ("FlightID")
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

-- Πίνακας EGGRAFEI (ΧΡΗΣΤΗΣ -> ΠΕΛΑΤΗΣ)
CREATE TABLE IF NOT EXISTS "EGGRAFEI" (
    "ID_Xrhsth" INTEGER NOT NULL,
    "ID_Pelath" INTEGER NOT NULL,
    PRIMARY KEY ("ID_Xrhsth", "ID_Pelath"),
    FOREIGN KEY ("ID_Xrhsth") REFERENCES "XRHSTHS" ("ID")
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    FOREIGN KEY ("ID_Pelath") REFERENCES "PELATHS" ("ID_Pelath")
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

-- Πίνακας KANEI (ΧΡΗΣΤΗΣ -> ΚΡΑΤΗΣΗ)
CREATE TABLE IF NOT EXISTS "KANEI" (
    "ID_Xrhsth" INTEGER NOT NULL,
    "Reservation_ID" INTEGER NOT NULL,
    "Date" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY ("ID_Xrhsth", "Reservation_ID"),
    FOREIGN KEY ("ID_Xrhsth") REFERENCES "XRHSTHS" ("ID")
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    FOREIGN KEY ("Reservation_ID") REFERENCES "KRATHSEIS" ("Reservation_ID")
        ON UPDATE CASCADE
        ON DELETE CASCADE
);
"""

# Εκτέλεση του SQL κώδικα
cursor.executescript(create_complete_database_query)

# Αποθήκευση και κλείσιμο
conn.commit()
conn.close()

