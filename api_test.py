import requests


def get_pokemont_info(name):
    url = "https://pokeapi.co/api/v2/pokemon/" + name

    response = requests.get(url)


    if response.status_code == 200:
        data = response.json()
        print(f"name: {data["name"]}")
        print(f"ID: {data["id"]}")
    else:
        print("Pokemon not found")



get_pokemont_info("pikachu")