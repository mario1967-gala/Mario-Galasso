#!/usr/bin/env python3
"""
Script di test per la funzionalità di import studenti
Dimostra come funziona l'estrazione dati da testo
"""

from app.utils import StudentExtractor

# Test 1: Formato base
print("=" * 60)
print("TEST 1: Formato Base (Cognome Nome, Data)")
print("=" * 60)

test_text_1 = """
Rossi Mario, 15/03/2007
Bianchi Laura, 22/05/2007
Verdi Giuseppe, 08/01/2007
Neri Anna, 30/09/2007
Ferrari Luca, 12/06/2007
"""

students_1 = StudentExtractor.extract_from_structured_text(test_text_1)
print(f"\nTesto di input:\n{test_text_1}")
print(f"\nStudenti estratti: {len(students_1)}")
for i, student in enumerate(students_1, 1):
    print(f"{i}. {student['cognome']} {student['nome']} - {student['data_nascita']}")

# Test 2: Formato completo con email
print("\n" + "=" * 60)
print("TEST 2: Formato Completo (con Email)")
print("=" * 60)

test_text_2 = """
Alberti Marco, 15/03/2007, marco.alberti@example.com
Bernardi Giulia, 22/05/2007, giulia.bernardi@example.com
Conti Luca, 08/01/2007, luca.conti@example.com
"""

students_2 = StudentExtractor.extract_from_structured_text(test_text_2)
print(f"\nTesto di input:\n{test_text_2}")
print(f"\nStudenti estratti: {len(students_2)}")
for i, student in enumerate(students_2, 1):
    print(f"{i}. {student['cognome']} {student['nome']} - {student['data_nascita']} - {student['email']}")

# Test 3: Formato completo con email e telefono
print("\n" + "=" * 60)
print("TEST 3: Formato Completo (con Email e Telefono)")
print("=" * 60)

test_text_3 = """
De Luca Sara, 30/09/2007, sara.deluca@example.com, 3331234567
Ferrari Alessandro, 12/07/2007, alessandro.ferrari@example.com, 3339876543
Gallo Martina, 25/04/2007, martina.gallo@example.com, 3335555555
"""

students_3 = StudentExtractor.extract_from_structured_text(test_text_3)
print(f"\nTesto di input:\n{test_text_3}")
print(f"\nStudenti estratti: {len(students_3)}")
for i, student in enumerate(students_3, 1):
    print(f"{i}. {student['cognome']} {student['nome']} - {student['data_nascita']} - {student['email']} - {student['telefono']}")

# Test 4: Formati misti
print("\n" + "=" * 60)
print("TEST 4: Formati Misti")
print("=" * 60)

test_text_4 = """
Marino Davide, 03/11/2007
Ricci Chiara, 18/06/2007, chiara.ricci@example.com
Romano Matteo, 09/02/2007, matteo.romano@example.com, 3337777777
Santoro Sofia, 14/08/2007
"""

students_4 = StudentExtractor.extract_from_structured_text(test_text_4)
print(f"\nTesto di input:\n{test_text_4}")
print(f"\nStudenti estratti: {len(students_4)}")
for i, student in enumerate(students_4, 1):
    email = student.get('email', '-')
    telefono = student.get('telefono', '-')
    print(f"{i}. {student['cognome']} {student['nome']} - {student['data_nascita']} - {email} - {telefono}")

print("\n" + "=" * 60)
print("RIEPILOGO")
print("=" * 60)
print(f"\nTotale studenti estratti: {len(students_1) + len(students_2) + len(students_3) + len(students_4)}")
print("\n✓ Tutti i test completati con successo!")
print("\nPuoi usare questi formati nella pagina di import dell'applicazione.")
