import requests

# OAuth 2.0 parameters
client_id = "1052058814383-2s503ud9diredv3117t5m2foq9i0cift.apps.googleusercontent.com"
redirect_uri = "http://localhost:8080/oauth2callback"
scope = "https://www.googleapis.com/auth/contacts"
response_type = "code"

# Authorization endpoint URL
authorization_url = "https://accounts.google.com/o/oauth2/auth"

# Construct authorization URL
authorization_url_params = {
    "client_id": client_id,
    "redirect_uri": redirect_uri,
    "scope": scope,
    "response_type": response_type
}

authorization_redirect_url = authorization_url + "?" + "&".join(f"{key}={value}" for key, value in authorization_url_params.items())

# Redirect the user to the authorization URL
print("Please visit the following URL to authorize this application:")
print(authorization_redirect_url)

"http://localhost:8080/oauth2callback?code=4/0AeaYSHCApwsfJ8_PAGnZNtj_1x_jM_ErLon2HR8YsLkAd4v20HR8SqBbP7jn6u28M1D9pw&scope=https://www.googleapis.com/auth/contacts"
