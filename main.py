import requests

def main():
    print("Welcome :)")
    print("What would you like to do?")
    choice = input("1.Remove all friends\n2.Remove all messages in a channel\n3.Leave all servers\n4.Everything\n5.Exit\n")
    token = input("Enter your token: ")
    session = requests.Session()
    session.headers.update({"authorization": token})
    session.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"})
    if choice == "1":
        print("Removing all friends...")
        remove_friends(session)
    elif choice == "2":
        channel_id = input("Enter the channel id: ")
        print("Removing all messages...")
        remove_messages(channel_id, session)
    elif choice == "3":
        print("Leaving all servers...")
        leave_servers(session)
    elif choice == "4":
        print("Removing all friends...")
        remove_friends(session)
        print("Removing all messages...")
        remove_messages(session)
        print("Leaving all servers...")
        leave_servers(session)
    else:
        print("Bye 👋")               
        exit()

def remove_friends(session):
    r = session.get("https://discord.com/api/v9/users/@me/relationships")
    open("friends.json", "w").write(r.text)
    print("Saved friends to friends.json")
    for i in r.json():
        r = session.delete(f"https://discord.com/api/v9/users/@me/relationships/{i['id']}")
        if r.status_code == 204:
            print(f"Removed {i['id']}")
        else:
            print(f"Failed to remove {i['id']}")    
    print("Finished.")

def remove_messages(channel_id, session):
    r = session.get(f"https://discord.com/api/v9/channels/{channel_id}/messages?limit=100")
    open("messages.json", "w").write(r.text)
    print("Saved messages to messages.json")
    userID = session.get("https://discord.com/api/v9/users/@me").json()["id"]
    for i in r.json():
        if i["author"]["id"] == userID:
            r = session.delete(f"https://discord.com/api/v9/channels/{channel_id}/messages/{i['id']}")
            if r.status_code == 204:
                print(f"Removed {i['id']}")
            else:
                print(f"Failed to remove {i['id']}")
    print("Finished.")

def leave_servers(session):
    r = session.get("https://discord.com/api/v9/users/@me/guilds")
    open("servers.json", "w").write(r.text)
    print("Saved servers to servers.json")
    for i in r.json():
        r = session.delete(f"https://discord.com/api/v9/users/@me/guilds/{i['id']}")
        if r.status_code == 204:
            print(f"Left {i['id']}")
        else:
            print(f"Failed to leave {i['id']}")
            print(r.status_code)
    print("Finished.")   

if __name__ == "__main__":
    main()      