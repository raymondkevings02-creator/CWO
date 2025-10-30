from babel.messages.extract import extract
from babel.messages.pofile import write_po
from babel.messages.catalog import Catalog
import io

catalog = Catalog()
for filename in ['app.py']:
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    fileobj = io.BytesIO(content.encode('utf-8'))
    keywords = {'_': None}
    for lineno, funcname, messages, comments in extract('python', fileobj, keywords, [], {}, filename):
        if messages:
            message = messages[0] if isinstance(messages, list) else messages
            catalog.add(message, locations=[(filename, lineno)])

with open('messages.pot', 'wb') as f:
    write_po(f, catalog)
