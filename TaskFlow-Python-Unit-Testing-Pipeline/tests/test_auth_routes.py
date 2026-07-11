def test_register_success(client):
    r=client.post("/register",data={"full_name":"Jane","email":"jane@example.com","password":"password123","confirm_password":"password123"},follow_redirects=True); assert r.status_code==200 and b"Registration successful" in r.data
def test_password_mismatch(client):
    r=client.post("/register",data={"full_name":"Jane","email":"jane@example.com","password":"password123","confirm_password":"different"}); assert r.status_code==400
def test_login_success(client,user):
    r=client.post("/login",data={"email":"test@example.com","password":"password123"},follow_redirects=True); assert b"Good to see you" in r.data
def test_login_failure(client,user):
    assert client.post("/login",data={"email":"test@example.com","password":"bad"}).status_code==401
def test_logout(auth_client):
    r=auth_client.get("/logout",follow_redirects=True); assert b"Plan smarter" in r.data
