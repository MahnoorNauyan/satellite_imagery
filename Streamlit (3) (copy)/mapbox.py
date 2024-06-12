import requests
from PIL import Image
from io import BytesIO
from tqdm import tqdm
import random


def save_map_image(url, save_path):
    try:
        # Make a GET request to the Mapbox API
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Open the image using PIL
            image = Image.open(BytesIO(response.content))

            # Save the image to the specified path
            image.save(save_path)

            # print(f"Image saved successfully at {save_path}")

        else:
            print(
                f"Error: Unable to fetch image. Status Code: {response.status_code}"
            )

    except Exception as e:
        print(f"Error: {e}")


def generate_random_lat_lng():
    # min_lat, min_lng = min(polygon, key=lambda x: x[0])
    # max_lat, max_lng = max(polygon, key=lambda x: x[0])

    random_lat = random.uniform(33.45, 33.75)
    random_lng = random.uniform(72.8, 73.4)

    return random_lat, random_lng


def point_in_polygon(lat, lng, polygon):
    # Check if a point is inside a polygon using Ray Casting algorithm
    # Arguments:
    #   lat: Latitude of the point
    #   lng: Longitude of the point
    #   polygon: List of tuples representing the vertices of the polygon

    num_vertices = len(polygon)
    is_inside = False

    j = num_vertices - 1
    for i in range(num_vertices):
        if ((polygon[i][1] > lng) != (polygon[j][1] > lng)) and (
                lat < (polygon[j][0] - polygon[i][0]) * (lng - polygon[i][1]) /
            (polygon[j][1] - polygon[i][1]) + polygon[i][0]):
            is_inside = not is_inside
        j = i
    print(is_inside)
    return is_inside


if __name__ == "__main__":

    city_lat_lngs = [(33.66630, 72.98918),
                    (33.66746, 72.98830),
                    (33.66798, 72.98950),
                    (33.66691, 72.99034)]

    zoom = 17
    height, width = 1280, 1280
    access_token = "pk.eyJ1IjoibWFobm9vcnN5ZWRhIiwiYSI6ImNsd295a2VicDJhY3kya3BmNzB4a3JoZTUifQ.Ro8HUA5tcEBXHstv5EN8FQ"

    points = []
    for _ in tqdm(range(1000), total=1000):
        random_point = generate_random_lat_lng()
        print(random_point)
        if point_in_polygon(random_point[0], random_point[1], city_lat_lngs):
            points.append(random_point)

            latitude, longitude = random_point[0], random_point[1]
            print(latitude,longitude,"*****")

            mapbox_url = f"https://api.mapbox.com/styles/v1/mapbox/satellite-v9/static/{longitude},{latitude},{zoom},0/{height}x{width}?access_token={access_token}"

            # Path to save the image
            save_path = f"dataset/islamabad/lat_{latitude}_lng_{longitude}_zoom_{zoom}.png"

            # Call the function to save the map image
            save_map_image(mapbox_url, save_path)

        print("Total Generated Points",len(points))