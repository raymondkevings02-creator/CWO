from babel.messages.pofile import read_po
from babel.messages.mofile import write_mo
import os

def compile_po_to_mo(po_file, mo_file):
    with open(po_file, 'r', encoding='utf-8') as f:
        catalog = read_po(f)
    with open(mo_file, 'wb') as f:
        write_mo(f, catalog)

# Compile for English
compile_po_to_mo('translations/en/LC_MESSAGES/messages.po', 'translations/en/LC_MESSAGES/messages.mo')

# Compile for French
compile_po_to_mo('translations/fr/LC_MESSAGES/messages.po', 'translations/fr/LC_MESSAGES/messages.mo')

print('Compiled .mo files for both languages')
