from fastapi.testclient import TestClient
from fastapi import status
from main import app

client = TestClient(app=app)


def test_get_user_specific():
    response = client.get("/user/55")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "id": 55,
        "name": "string",
        "email": "string",
        "password": "string",
        "role": 0,
    }


def test_login_admin_fail():
    response = client.post(
        "/auth/login", json={"email": "admin", "password": "admin1"}
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_R_user():
    response = client.get("/user")
    assert response.status_code == status.HTTP_403_FORBIDDEN
    response_login = client.post(
        "/auth/login", json={"email": "admin", "password": "admin"}
    )
    token = response_login.json()["access_token"]
    response_get = client.get(
        "/user", headers={"Authorization": f"Bearer {token}"}
    )
    assert response_get.status_code == status.HTTP_200_OK


def test_U_user():
    response = client.patch("/user/53", json={"email": "email53@gmail.com"})
    assert response.status_code == status.HTTP_403_FORBIDDEN

    response_login = client.post(
        "/auth/login", json={"email": "ocd", "password": "string"}
    )
    token = response_login.json()["access_token"]
    response_patch = client.patch(
        "/user/53",
        json={"email": "email53@gmail.com"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response_patch.status_code == status.HTTP_403_FORBIDDEN

    response_login_admin = client.post(
        "/auth/login", json={"email": "admin", "password": "admin"}
    )
    token_admin = response_login_admin.json()["access_token"]
    print(token_admin)
    response_patch_admin = client.patch(
        "/user/53",
        headers={"Authorization": f"Bearer {token_admin}"},
        json={
            "email": "email53@gmail.com",
            "name": "caisedo",
            "password": "brighton",
        },
    )
    assert response_patch_admin.status_code == status.HTTP_200_OK


def test_D_user():
    response = client.delete("/user/53")
    assert response.status_code == status.HTTP_403_FORBIDDEN

    response_login = client.post(
        "/auth/login", json={"email": "ocd", "password": "string"}
    )
    token = response_login.json()["access_token"]
    response_delete = client.delete(
        "/user/53", headers={"Authorization": f"Bearer {token}"}
    )
    assert response_delete.status_code == status.HTTP_403_FORBIDDEN

    response_login_admin = client.post(
        "/auth/login", json={"email": "admin", "password": "admin"}
    )
    token_admin = response_login_admin.json()["access_token"]
    print(token_admin)
    response_delete_admin = client.delete(
        "/user/53", headers={"Authorization": f"Bearer {token_admin}"}
    )
    assert response_delete_admin.status_code == status.HTTP_200_OK
