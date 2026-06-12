import requests

movie_name = input("Enter a movie name: ").strip()

if not movie_name:
    print("Movie name cannot be empty.")
    exit()

api_key = "451f5044"

url = f"https://www.omdbapi.com/?t={movie_name}&apikey={api_key}"

response = requests.get(url)

try:
    response = requests.get(url, timeout=5)
    response.raise_for_status()

    data = response.json()
    if data["Response"] == "True":
        print(f"Title: {data['Title']}")
        print(f"Year: {data['Year']}")
        print(f"Genre: {data['Genre']}")
        print(f"IMDb Rating: {data['imdbRating']}")
        print(f"Director: {data['Director']}")
        print(f"Runtime: {data['Runtime']}")
        print(data.get("Plot", "N/A"))
    else:
        print("Movie not found.")

except requests.RequestException as e:
    print(f"Error: {e}")

   
        