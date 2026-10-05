import os

# TODO: afficher APP_ENV et API_PORT avec valeurs par défaut.

app_env = os.getenv("APP_ENV", "APP_ENV_NOT_DEFINED")
api_port = os.getenv("API_PORT", "API_PORT_NOT_DEFINED")

print(app_env)
print(api_port)  

print("\n")
print(f"The app is running in {app_env} and the api will run on port {api_port}")