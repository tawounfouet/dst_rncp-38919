import os

print(os.getenv("APP_ENV", "development"))
print(int(os.getenv("API_PORT", "8000")))
