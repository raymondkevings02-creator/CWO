import sys
import os
sys.path.append(os.path.dirname(__file__))

from app import app, db, Conducteur, Investisseur
from forms import ConducteurForm, InvestisseurForm
from config import Config

def test_imports():
    print("Testing imports...")
    assert app is not None
    assert db is not None
    assert Conducteur is not None
    assert Investisseur is not None
    assert ConducteurForm is not None
    assert InvestisseurForm is not None
    assert Config is not None
    print("All imports successful!")

def test_config():
    print("Testing config...")
    config = Config()
    assert hasattr(config, 'SECRET_KEY')
    assert hasattr(config, 'SQLALCHEMY_DATABASE_URI')
    print("Config test passed!")

def test_models():
    print("Testing models...")
    with app.app_context():
        db.create_all()
        # Test Conducteur
        c = Conducteur(nom="Test Driver", gain=100.0, miles=50, itineraire="Route A", date="2023-01-01")
        db.session.add(c)
        db.session.commit()
        assert c.id is not None
        # Test Investisseur
        i = Investisseur(nom="Test Investor", montant=500.0)
        db.session.add(i)
        db.session.commit()
        assert i.id is not None
        print("Models test passed!")

def test_forms():
    print("Testing forms...")
    with app.test_request_context():
        form = ConducteurForm()
        assert hasattr(form, 'nom')
        assert hasattr(form, 'gain')
        assert hasattr(form, 'miles')
        assert hasattr(form, 'itineraire')
        assert hasattr(form, 'date')
        form2 = InvestisseurForm()
        assert hasattr(form2, 'nom')
        assert hasattr(form2, 'montant')
        print("Forms test passed!")

def test_routes():
    print("Testing routes...")
    with app.test_client() as client:
        # Test home page
        response = client.get('/')
        assert response.status_code == 200
        print("Home page: OK")

        # Test conducteurs page
        response = client.get('/conducteurs')
        assert response.status_code == 200
        print("Conducteurs page: OK")

        # Test investisseurs page
        response = client.get('/investisseurs')
        assert response.status_code == 200
        print("Investisseurs page: OK")

        # Test liaison page (requires access code, so expect redirect)
        response = client.get('/liaison')
        assert response.status_code == 302  # Redirect to access_code
        print("Liaison page: OK (redirects as expected)")

        # Test 404
        response = client.get('/nonexistent')
        assert response.status_code == 404
        print("404 page: OK")

if __name__ == "__main__":
    test_imports()
    test_config()
    test_models()
    test_forms()
    test_routes()
    print("All tests passed!")
