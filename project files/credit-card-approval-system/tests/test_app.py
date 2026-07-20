import tempfile
from app import create_app
from services.database import db, User

def test_registration():
    _, path=tempfile.mkstemp(suffix=".db")
    app=create_app()
    app.config.update(TESTING=True,SQLALCHEMY_DATABASE_URI=f"sqlite:///{path}")
    with app.app_context():
        db.drop_all(); db.create_all()
    client=app.test_client()
    response=client.post("/auth/register",data={"full_name":"Test User","email":"test@example.com","password":"Password1"},follow_redirects=True)
    assert response.status_code==200
    with app.app_context():
        assert User.query.filter_by(email="test@example.com").first() is not None
