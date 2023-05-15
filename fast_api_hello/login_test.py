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


def test_login_admin_success():
    response = client.post(
        "/auth/login", json={"email": "admin@gmail.com",
                             "password": "123456"}
    )
    assert response.status_code == status.HTTP_200_OK


def test_login_admin_fail():
    response = client.post(
        "/auth/login", json={"email": "admin@gmail.com",
                             "password": "1234567"}
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_read_user():
    # user without token
    # expected unauthenticated fail
    response = client.get("/user")
    assert response.status_code == status.HTTP_403_FORBIDDEN

    # re-login with proper admin user
    # get JWT to attach to request header
    response_login = client.post(
        "/auth/login", json={"email": "admin",
                             "password": "admin"}
    )

    token = response_login.json()["access_token"]
    response_get = client.get(
        "/user", headers={"Authorization": f"Bearer {token}"}
    )
    assert response_get.status_code == status.HTTP_200_OK


def test_update_user():
    # three scenarios
    # no JWT
    # unauthorized JWT
    # proper JWT

    # 1. No JWT - expected unauthenticated
    response = client.patch("/user/53", json={"email": "email53@gmail.com"})
    assert response.status_code == status.HTTP_403_FORBIDDEN

    # 2. Unauthorized JWT, login as an unauthorized user with role 0 instead of 1 as admin
    # Expected 403
    response_login = client.post(
        "/auth/login",
        json={"email": "ocd",
              "password": "string"}
    )
    token = response_login.json()["access_token"]
    response_patch = client.patch(
        "/user/53",
        json={"email": "email53@gmail.com"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response_patch.status_code == status.HTTP_403_FORBIDDEN

    # 3. Login with proper user, attach JWT to header
    # Update
    # Expected 200
    response_login_admin = client.post(
        "/auth/login",
        json={"email": "admin",
              "password": "admin"}
    )
    token_admin = response_login_admin.json()["access_token"]
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


def test_delete_user():
    """
    Test delete user in three scenario
    Scenario one: No JWT - unauthenticated user
    Scenario two: Unauthorized user with improper JWT
    Scenario three: Proper user with admin right to execute the method
    """

    # Scenario 1: Non-login user - expected 403
    response = client.delete("/user/53")
    assert response.status_code == status.HTTP_403_FORBIDDEN

    # Scenario 2: Improper user, normal user executing forbidden action
    # Get JWT then attach to the header
    # Return 403
    response_login = client.post(
        "/auth/login", json={"email": "ocd",
                             "password": "string"}
    )
    token = response_login.json()["access_token"]
    response_delete = client.delete(
        "/user/53",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response_delete.status_code == status.HTTP_403_FORBIDDEN


    # proper admin user
    # delete user
    # expecct 200
    response_login_admin = client.post(
        "/auth/login",
        json={"email": "admin",
             "password": "admin"}
    )
    token_admin = response_login_admin.json()["access_token"]
    print(token_admin)
    response_delete_admin = client.delete(
        "/user/53", headers={"Authorization": f"Bearer {token_admin}"}
    )
    assert response_delete_admin.status_code == status.HTTP_200_OK
