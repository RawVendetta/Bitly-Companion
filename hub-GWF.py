import requests

# Function to shorten a link using the Bitly API
def shorten_link(access_token, long_url):
    base_url = "https://api-ssl.bitly.com/v4/bitlinks"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    try:
        data = {
            "long_url": long_url
        }
        response = requests.post(base_url, headers=headers, json=data)
        response.raise_for_status()
        short_link = response.json()["id"]
        print(f"Shortened Link: {short_link}")

        # Append to links.txt
        with open('links.txt', 'a') as file:
            file.write(f"{short_link}={long_url}\n")
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"Request exception occurred: {req_err}")
    except Exception as err:
        print(f"Error occurred: {err}")

# Function to remove a shortened link and update links.txt
def remove_shortened_link(access_token, short_link_to_remove, file_path):
    base_url = f"https://api-ssl.bitly.com/v4/bitlinks/{short_link_to_remove}"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    try:
        # Remove the shortened link from your Bitly account using the API
        response = requests.delete(base_url, headers=headers)
        response.raise_for_status()
        print(f"Shortened link '{short_link_to_remove}' removed from your Bitly account.")

        # Update links.txt by removing the line
        lines = []
        with open(file_path, 'r') as file:
            for line in file:
                if not line.startswith(f"{short_link_to_remove}="):
                    lines.append(line)

        with open(file_path, 'w') as file:
            file.writelines(lines)

        print(f"Shortened link '{short_link_to_remove}' removed from 'links.txt'.")
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"Request exception occurred: {req_err}")
    except Exception as err:
        print(f"Error occurred: {err}")
        
def display_bitlinks_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            for line in file:
                bitlink, long_url = line.strip().split('=')
                print(f"{bitlink} ----> {long_url}")
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
    except ValueError:
        print(f"Invalid line format in '{file_path}'. Each line should contain a bitlink and a long URL separated by '='.")

        
def main():
    # Replace 'YOUR_ACCESS_TOKEN' with your actual Bitly access token
    access_token = ""

    # Replace 'links.txt' with the actual file path of your text file
    file_path = 'links.txt'

    while True:
        display_bitlinks_from_file(file_path)
        print("\nOptions:")
        print("1. Shorten a link")
        print("2. Remove shortened link")
        print("3. Exit")

        choice = input("Enter your choice (1/2/3): ")

        if choice == '1':
            long_url = input("Enter the URL to shorten: ")
            shorten_link(access_token, long_url)

        elif choice == '2':
            short_link_to_remove = input("Enter the shortened link to remove: ")
            remove_shortened_link(access_token, short_link_to_remove, file_path)

        elif choice == '3':
            print("Exiting the program.")
            break

        else:
            print("Invalid choice. Please choose a valid option.")

if __name__ == "__main__":
    main()
