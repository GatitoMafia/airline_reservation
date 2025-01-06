import sqlite3

# Σύνδεση με τη βάση δεδομένων
conn = sqlite3.connect("airline_reservation.db")
cursor = conn.cursor()

# Διόρθωση των πεδίων Price και Type
update_query = """
UPDATE KRATHSEIS
SET Price = CAST(Type AS REAL), -- Μεταφέρει την τιμή από το Type στο Price
    Type = CASE
        WHEN CAST(Type AS REAL) < 200 THEN 'Economy' -- Αν η τιμή είναι μικρότερη από 200, Economy
        WHEN CAST(Type AS REAL) >= 200 AND CAST(Type AS REAL) < 400 THEN 'Business' -- Αν είναι μεταξύ 200-400, Business
        ELSE 'First' -- Αν είναι 400 ή παραπάνω, First
    END
WHERE CAST(Type AS REAL) > 0; -- Επιλέγουμε μόνο εγγραφές όπου το Type έχει αριθμητική τιμή
"""

# Εκτέλεση του query
cursor.execute(update_query)

# Commit και κλείσιμο της σύνδεσης
conn.commit()
conn.close()

print("Η διόρθωση ολοκληρώθηκε!")
