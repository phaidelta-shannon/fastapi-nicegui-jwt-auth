from nicegui import ui
import requests

BASE_URL = "http://127.0.0.1:8000"

def register():
    username = username_input.value
    password = password_input.value
    response = requests.post(f"{BASE_URL}/register", params={"username": username, "password": password})
    result_label.set_text(response.json().get("message", "Error"))

def login():
    global token
    username = username_input.value
    password = password_input.value
    response = requests.post(f"{BASE_URL}/login", params={"username": username, "password": password})
    token = response.json().get("access_token")
    if token:
        result_label.set_text("Login Successful")
    else:
        result_label.set_text("Login Failed")

def check_protected_route():
    global token
    if not token:
        result_label.set_text("Please log in first!")
        return
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/protected-route", headers=headers)
    result_label.set_text(response.json().get("message", "Error"))

ui.label("Secure user authentication & authorization in a FastAPI backend with a NiceGUI frontend using JWT")
username_input = ui.input("Username")
password_input = ui.input("Password", password=True)
ui.button("Register", on_click=register)
ui.button("Login", on_click=login)
ui.button("Check Protected Route", on_click=check_protected_route)
result_label = ui.label("")
ui.run()
