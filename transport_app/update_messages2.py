from babel.messages.pofile import write_po
from babel.messages.catalog import Catalog

# Create a new catalog
cat = Catalog()

# Add the new strings from app.py
cat.add('Code d\'accès incorrect.', locations=[('app.py', 1)])
cat.add('Vous avez été déconnecté.', locations=[('app.py', 2)])
cat.add('Conducteur ajouté avec succès.', locations=[('app.py', 3)])
cat.add('Conducteur supprimé avec succès.', locations=[('app.py', 4)])
cat.add('Investisseur ajouté avec succès.', locations=[('app.py', 5)])
cat.add('Investisseur supprimé avec succès.', locations=[('app.py', 6)])

# Write to messages.pot
with open('messages.pot', 'w', encoding='utf-8') as f:
    write_po(f, cat)

print('messages.pot updated with new strings')
