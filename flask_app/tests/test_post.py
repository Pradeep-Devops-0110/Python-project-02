# tests/test_posts.py
def auth_header(client, email="c@d.com", password="pass"):
    client.post("/auth/signup", data={"email": email, "password": password})
    res = client.post("/auth/api/login", json={"email": email, "password": password})
    token = res.get_json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def test_create_list_update_delete_post(client):
    h = auth_header(client)
    res = client.post("/posts/api", json={"title": "t1", "body": "b1"}, headers=h)
    assert res.status_code == 201
    pid = res.get_json()["id"]

    res = client.get("/posts/api", headers=h)
    assert len(res.get_json()) == 1

    res = client.put(f"/posts/api/{pid}", json={"title": "t2"}, headers=h)
    assert res.status_code == 200
    assert res.get_json()["title"] == "t2"

    res = client.delete(f"/posts/api/{pid}", headers=h)
    assert res.status_code == 200

    res = client.get("/posts/api", headers=h)
    assert res.get_json() == []
