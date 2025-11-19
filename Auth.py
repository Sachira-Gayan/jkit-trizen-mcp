from msal import ConfidentialClientApplication


TENANT_ID = "704e1a5a-f6a7-4fae-be42-e1a81a3412e7"
CLIENT_ID = "f659c2ba-4303-48be-bc57-8a6427b6f237"
REDIRECT_URI = "http://localhost:8000/mcp"


CLIENT_ID = "029a88ac-a2a7-48dc-999a-e48cee57866d"
CLIENT_SS= "zNp8Q~dMQ5cvIFdiMLHn2ojDZAJaTLPt1~qqwaf2"
TENANT_ID = "f6bf0d68-8c3c-4a25-a5d8-661cec987ce2"
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPE = ["https://graph.microsoft.com/.default"]  # or your API scope

result = None 

def get_accessToken():


    app = ConfidentialClientApplication(
    client_id=CLIENT_ID,
    client_credential=CLIENT_SS,
    authority=AUTHORITY
    )

# Acquire token
    result = app.acquire_token_for_client(scopes=SCOPE)

    if "access_token" in result:
        access_token = result["access_token"]
        return access_token # print partial for debug

    
    
    else:
        return("Error acquiring token:", result.get("error_description"))
