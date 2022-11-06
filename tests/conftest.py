import pytest
from app import create_app
from app import db
from flask.signals import request_finished
from app.models.bike import Bike

@pytest.fixture
def app():
    app = create_app({"TESTING": True})

    @request_finished.connect_via(app) #helps, especially for PUT, to make sure a variable isn't outdated - if request is finished removes data and ends session
    def expire_session(sender, response, **extra): #**extra refers to any extra variables we might make - dont worry too much about it
        db.session.remove()

    with app.app_context():
        db.create_all()
        yield app
    
    with app.app_context():
        db.drop_all() #clears out all database at end of test

#mimcs actual client making a request
@pytest.fixture
def client(app): #app being passed in refers to the fixture above
    return app.test_client()

@pytest.fixture
def add_two_bikes(app):
    bike1 = Bike(name="Speedy", price=1, size=6, type="racing")
    bike2 = Bike(name="Motorbike", price=6, size=2, type="Motor")

    db.session.add(bike1)
    db.session.add(bike2)
    db.session.commit()