from msal import ConfidentialClientApplication



CLIENT_ID = "f659c2ba-4303-48be-bc57-8a6427b6f237"
CLIENT_SECRET = "7Vi8Q~x.z7GBT.Yt5rGQS4LyfqJPaHV6ZyFVTazN"
TENANT_ID = "704e1a5a-f6a7-4fae-be42-e1a81a3412e7"
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPE = ["https://graph.microsoft.com/.default"]  # or your API scope

result = None 

def get_accessToken():


    app = ConfidentialClientApplication(
    client_id=CLIENT_ID,
    client_credential=CLIENT_SECRET,
    authority=AUTHORITY
    )

# Acquire token
    result = app.acquire_token_for_client(scopes=SCOPE)

    if "access_token" in result:
        access_token = result["access_token"]
        return access_token # print partial for debug

    
    
    else:
        return("Error acquiring token:", result.get("error_description"))
    
    
