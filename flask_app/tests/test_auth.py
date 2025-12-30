# tests/test_auth.py
def test_signup_and_login(client):
    res = client.post("/auth/signup", data={"email": "a@b.com", "password": "pass"})
    assert res.status_code == 302

    res = client.post("/auth/api/login", json={"email": "a@b.com", "password": "pass"})
    assert res.status_code == 200
    token = res.get_json()["access_token"]
    assert token
