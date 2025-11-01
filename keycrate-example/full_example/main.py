import keycrate
import hwid
from datetime import datetime, timezone

# One-time client setup
client = keycrate.configurate(
    host="https://api.keycrate.dev", 
    app_id="YOUR_APP_ID"
)


def print_error(msg, data=None):
    print(f"\nAuthentication failed: {msg}")

    if msg == "LICENSE_NOT_FOUND":
        print("License key not found. Check your key.")
    elif msg == "INVALID_USERNAME_OR_PASSWORD":
        print("Wrong username or password.")
    elif msg == "LICENSE_NOT_ACTIVE":
        print("License not active. Contact support.")
    elif msg == "DEVICE_ALREADY_REGISTERED_WITH_OTHER_LICENSE":
        print("This device is already linked to another license.")
    elif msg == "LICENSE_EXPIRED":
        expires = data.get("expires_at")
        if expires:
            exp_dt = datetime.fromisoformat(expires.replace("Z", "+00:00"))
            print(f"License expired on: {exp_dt.strftime('%Y-%m-%d %H:%M:%S UTC')}")
        else:
            print("License has expired.")
    elif msg == "HWID_MISMATCH":
        print("HWID doesn't match.")
        if data and data.get("hwid_reset_allowed"):
            last = data.get("last_hwid_reset_at")
            cd = data.get("hwid_reset_cooldown")
            if last and cd:
                last_dt = datetime.fromisoformat(last.replace("Z", "+00:00"))
                now_dt = datetime.now(timezone.utc)
                elapsed = (now_dt - last_dt).total_seconds()
                left = int(cd) - elapsed
                if left > 0:
                    print(f"Reset available in {int(left)} seconds.")
                else:
                    print("You can reset HWID now.")
            else:
                print("Try resetting HWID.")
        else:
            print("HWID reset not allowed.")
    else:
        print(f"Error: {msg}. Contact support.")


def login():
    hwid_val = hwid.get_hwid()
    print("\n=== Keycrate Login ===")
    key = input("License key (or press ENTER for username): ").strip()

    try:
        if key:
            resp = client.authenticate(license=key, hwid=hwid_val)
        else:
            user = input("Username: ").strip()
            pwd = input("Password: ").strip()
            if not user or not pwd:
                print("Both required.")
                return False, None
            resp = client.authenticate(username=user, password=pwd, hwid=hwid_val)

        if not resp.get("success"):
            print_error(resp.get("message"), resp.get("data"))
            return False, None

        print("\nLogin successful!")
        return True, resp.get("data", {}).get("key")

    except Exception as e:
        print(f"Connection error: {e}")
        return False, None


def register(license_key):
    print("\n=== Set Up Username & Password ===")
    user = input("Username: ").strip()
    pwd = input("Password: ").strip()
    if not user or not pwd:
        print("Can't be empty.")
        return

    try:
        resp = client.register(license=license_key, username=user, password=pwd)
        if resp.get("success"):
            print(f"\nSuccess! {resp.get('message')}")
        else:
            print(f"\nFailed: {resp.get('message')}")
    except Exception as e:
        print(f"Failed to register: {e}")


def main():
    ok, key = login()
    if not ok:
        print("\nAccess denied. Bye.")
        return

    print("\nWelcome! You have access.\n")

    while True:
        cmd = input("Type 'register' or 'exit': ").strip().lower()
        if cmd == "exit":
            print("Goodbye!")
            break
        if cmd == "register":
            register(key)
            break
        print("Invalid. Try 'register' or 'exit'.")


if __name__ == "__main__":
    main()