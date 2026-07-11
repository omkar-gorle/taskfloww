def test_unauthorized_redirect(client):
    r=client.get("/tasks/"); assert r.status_code==302 and "/login" in r.location
def test_create_route(auth_client):
    r=auth_client.post("/tasks/create",data={"title":"Route task","description":"","category":"Work","priority":"High","status":"Pending","due_date":""},follow_redirects=True); assert b"Route task" in r.data
def test_edit_own(auth_client,sample_task):
    r=auth_client.post(f"/tasks/{sample_task.id}/edit",data={"title":"Edited","description":"","category":"Study","priority":"Low","status":"Pending","due_date":""},follow_redirects=True); assert b"Edited" in r.data
def test_delete_own(auth_client,sample_task):
    r=auth_client.post(f"/tasks/{sample_task.id}/delete",follow_redirects=True); assert b"Task deleted" in r.data
def test_toggle_own(auth_client,sample_task):
    r=auth_client.post(f"/tasks/{sample_task.id}/toggle",follow_redirects=True); assert b"Task status updated" in r.data
def test_cannot_edit_other(client,second_user,sample_task):
    client.post("/login",data={"email":"other@example.com","password":"password123"}); assert client.get(f"/tasks/{sample_task.id}/edit").status_code==404
def test_cannot_delete_other(client,second_user,sample_task):
    client.post("/login",data={"email":"other@example.com","password":"password123"}); assert client.post(f"/tasks/{sample_task.id}/delete").status_code==404
def test_search_route(auth_client,sample_task):
    r=auth_client.get("/tasks/?search=pytest"); assert b"Study pytest" in r.data
def test_filter_route(auth_client,sample_task):
    assert b"Study pytest" in auth_client.get("/tasks/?priority=High").data
    assert b"Study pytest" not in auth_client.get("/tasks/?priority=Low").data
def test_export_csv(auth_client,sample_task):
    r=auth_client.get("/reports/export.csv"); assert r.status_code==200 and b"Study pytest" in r.data
def test_dashboard(auth_client):
    assert b"Weekly productivity" in auth_client.get("/dashboard/").data
def test_reports(auth_client):
    assert b"Productivity reports" in auth_client.get("/reports/").data
