import pygame
import os
import requests
from datetime import datetime, timezone

class WeatherApp:
    def __init__(self, api_key, city):
        self.api_key = api_key
        self.city = city
        self.forecast = None

    def run(self):
        self.get_weather_data()
        if self.forecast:
            self.display_forecast()

    def get_weather_data(self):
        base_url = "http://api.openweathermap.org/data/2.5/forecast"
        params = {
            "q": self.city,
            "appid": self.api_key,
            "units": "metric",
            "cnt": 40,  
        }

        response = requests.get(base_url, params=params)

        if response.status_code == 200:
            self.forecast = response.json()
        else:
            print(f"Error {response.status_code}: {response.text}")

    def is_daytime(self, hour):
        return 6 <= hour < 21

    def display_forecast(self):
        pygame.init()
        screen = pygame.display.set_mode((400, 600))  
        pygame.display.set_caption("Weather Animation")

        clock = pygame.time.Clock()
        fps = 30  

        image_folder = os.path.join(os.path.dirname(__file__), "images")
        day_images, night_images = self.load_images(image_folder)

        for hour in self.forecast["list"]:
            self.display_hourly_weather(hour, day_images, night_images, screen, fps)

        pygame.quit()

    def display_hourly_weather(self, hour, day_images, night_images, screen, fps):
        timestamp = hour["dt"]
        date_time = datetime.fromtimestamp(timestamp, timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
        weather_description = hour["weather"][0]["main"]
        hour_of_day = int(datetime.fromtimestamp(timestamp, timezone.utc).strftime('%H'))

        alpha_value = 0  

        while alpha_value <= 255:
            background_color = (255, 255, 255, alpha_value)  

            screen.fill(background_color)

            if self.is_daytime(hour_of_day):
                self.display_fading_image(day_images, weather_description, screen)
            else:
                self.display_fading_image(night_images, weather_description, screen)

            pygame.display.flip()
            pygame.time.Clock().tick(fps)

            alpha_value += 5 

        print(f"At {date_time}, the weather is: {weather_description}")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

    def display_fading_image(self, images, weather_description, screen):
        if weather_description in images and images[weather_description] is not None:
           
            scaled_image = pygame.transform.scale(images[weather_description], (400, 600))
            screen.blit(scaled_image, (0, 0))

    def load_images(self, image_folder):
        day_images = {
            "Clear": pygame.image.load(os.path.join(image_folder, "day_clear_sky.png")),
            "Clouds": pygame.image.load(os.path.join(image_folder, "day_clouds.png")),
            "Drizzle": pygame.image.load(os.path.join(image_folder, "day_drizzle.png")),
            "Rain": pygame.image.load(os.path.join(image_folder, "day_rain.png")),
            "Thunderstorm": pygame.image.load(os.path.join(image_folder, "day_thunderstorm.png")),
            "Snow": pygame.image.load(os.path.join(image_folder, "day_snow.png")),
        }

        night_images = {
            "Clear": pygame.image.load(os.path.join(image_folder, "night_clear_sky.png")),
            "Clouds": pygame.image.load(os.path.join(image_folder, "night_clouds.png")),
            "Drizzle": pygame.image.load(os.path.join(image_folder, "night_drizzle.png")),
            "Rain": pygame.image.load(os.path.join(image_folder, "night_rain.png")),
            "Thunderstorm": pygame.image.load(os.path.join(image_folder, "night_thunderstorm.png")),
            "Snow": pygame.image.load(os.path.join(image_folder, "night_snow.png")),
        }

        return day_images, night_images

if __name__ == "__main__":
    api_key = "aaf9e3fd4728eb781f2b48fd3267b258"
    city = "Ultimo, Sydney"

    weather_app = WeatherApp(api_key, city)
weather_app.run()