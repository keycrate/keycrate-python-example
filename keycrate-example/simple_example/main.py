import keycrate


def main():

    client = keycrate.configurate(
        host="https://api.keycrate.dev", 
        app_id="YOUR_APP_ID"
        )
    

    action = input("Do you want to (1) Authenticate or (2) Register? [1/2]: ").strip()

    if action == "1":
        # AUTHENTICATE
        auth_type = input("Authenticate with (1) License or (2) Username/Password? [1/2]: ").strip()
        
        if auth_type == "1":
            # License-based authentication
            license_key = input("Enter license key: ").strip()
            resp = client.authenticate(license=license_key)
        else:
            # Username/password authentication
            username = input("Enter username: ").strip()
            password = input("Enter password: ").strip()
            resp = client.authenticate(username=username, password=password)

        
        if (not resp.get("success")): 
            print(f"\nAuthentication failed: {resp.get('message')}")
            quit()
        else :
            print("\nAuthentication successful!")


    elif action == "2":
        # REGISTER
        license_key = input("Enter license key to register a username and password to: ").strip()
        username = input("Enter desired username: ").strip()
        password = input("Enter password: ").strip()
        
        resp = client.register(license=license_key, username=username, password=password)
        


        if (not resp.get("success")): 
            print(f"\nRegistration failed: {resp.get('message')}")
            quit()
        else :
            print(f"\nRegistration successful! , {resp.get('message')}")


    else:
        print("Invalid option. Exiting.")


if __name__ == "__main__":
    main()