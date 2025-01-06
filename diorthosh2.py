import sqlite3

# Σύνδεση με τη βάση δεδομένων
conn = sqlite3.connect("airline_reservation.db")
cursor = conn.cursor()

# Ενημέρωση των πεδίων Vathmos και Sxolia
update_query = """
UPDATE AXIOLOGHSH
SET Vathmos = (SELECT CAST(Sxolia AS INTEGER) FROM AXIOLOGHSH tmp WHERE tmp.ID_Axiologhshs = AXIOLOGHSH.ID_Axiologhshs),
    Sxolia = (SELECT CAST(Vathmos AS TEXT) FROM AXIOLOGHSH tmp WHERE tmp.ID_Axiologhshs = AXIOLOGHSH.ID_Axiologhshs)
WHERE Vathmos IS NOT NULL AND Sxolia IS NOT NULL;
"""

# Εκτέλεση του query
cursor.execute(update_query)

# Commit και κλείσιμο της σύνδεσης
conn.commit()
conn.close()

print("Η διόρθωση ολοκληρώθηκε!")
