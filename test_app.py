from app import app, usuarios_db

def setup_function():
    app.testing = True

def test_ct01_login_sucesso():
    client = app.test_client()
    resp = client.post(
        "/login",
        data={"usuario": "admin", "senha": "123456"},
        follow_redirects=True,
    )

    result = "Acesso Permitido "
    bytes_result = result.encode("utf-8")
    assert bytes_result in resp.data

def test_ct02_login_inválido():
    client = app.test_client()
    resp = client.post(
        "/login",
        data={"usuario": "geovanna", "senha": "1234567"},
        follow_redirects=True,
    )

    result = "Usuário ou senha incorretos."
    bytes_result = result.encode("utf-8")
    assert bytes_result in resp.data

def test_ct03_login_inexistente():
    client = app.test_client()
    resp = client.post(
        "/login",
        data={"usuario": "", "senha": ""},
        follow_redirects=True,
    )

    result = "Por favor preencha os campos antes de continuar"
    bytes_result = result.encode("utf-8")
    assert bytes_result in resp.data
