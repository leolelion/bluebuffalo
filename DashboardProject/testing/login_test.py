from DashboardProject.models import User
from DashboardProject import db

def test_login(client):
    """"""
    new_user = User(userId="1",firstName="putri",lastName="leksono",email="putri", password="putri")
    db.session.add(new_user)
    db.session.commit()

    response = client.post("/login", data={"email": "putri",\
                                           "password": "putri"})

    with app.app_context():
        assert User.query.count() == 1