import requests

# OAuth 2.0 parameters
client_id = "1052058814383-2s503ud9diredv3117t5m2foq9i0cift.apps.googleusercontent.com"
client_secret = "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"
authorization_code = "4/0AeaYSHCApwsfJ8_PAGnZNtj_1x_jM_ErLon2HR8YsLkAd4v20HR8SqBbP7jn6u28M1D9pw"
redirect_uri = "http://localhost:8080/oauth2callback"

# Token endpoint URL
token_url = "https://oauth2.googleapis.com/token"

# Token request parameters
token_request_data = {
    "client_id": client_id,
    "client_secret": client_secret,
    "code": authorization_code,
    "redirect_uri": redirect_uri,
    "grant_type": "authorization_code"
}

try:
    # Make POST request to exchange authorization code for tokens
    response = requests.post(token_url, data=token_request_data)

    # Check if request was successful
    response.raise_for_status()

    # Parse response
    token_data = response.json()

    # Extract refresh token
    refresh_token = token_data.get("refresh_token")

    if refresh_token is None:
        raise ValueError("Refresh token not found in token response")

    # Store refresh token securely
    with open("refresh_token.txt", "w") as file:
        file.write(refresh_token)

    print("Refresh token obtained and stored successfully.")

except requests.RequestException as e:
    print("Error occurred during token exchange:", e)

except ValueError as e:
    print("Error:", e)
