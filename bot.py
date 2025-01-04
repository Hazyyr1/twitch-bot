from flask import Flask
import threading
import requests
from twitchio.ext import commands

# Twój klucz API z OpenWeatherMap
WEATHER_API_KEY = "e0561e4677fbd9a616065f4043c59ef5"

app = Flask('')


@app.route('/')
def home():
    return "Bot działa!"


def run():
    app.run(host='0.0.0.0', port=8080)


def keep_alive():
    t = threading.Thread(target=run)
    t.start()


class Bot(commands.Bot):

    def __init__(self):
        super().__init__(
            token='oauth:fn7sxmte78wx4rbnxqu4diqfv9c26i',  # Token OAuth dla bota
            prefix='!',  # Prefix komend
            initial_channels=['Hazyyr_', 'fake_danon']
        )

    async def event_ready(self):
        print(f'Zalogowano jako {self.nick}')
        print(f'Połączono z kanałami: {self.connected_channels}')

    @commands.command(name='pogoda')
    async def weather_command(self, ctx):
        if len(ctx.message.content.split()) < 2:
            await ctx.send(f"{ctx.author.name}, podaj lokalizację, np. !pogoda Warszawa")
            return

        location = " ".join(ctx.message.content.split()[1:])
        try:
            response = requests.get(
                f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={WEATHER_API_KEY}&units=metric&lang=pl"
            )
            data = response.json()

            if response.status_code == 200:
                city = data['name']
                temp = round(data['main']['temp'])
                weather = data['weather'][0]['description']
                await ctx.send(f"Pogoda dla {city}: {temp}°C, {weather}.")
            else:
                await ctx.send(f"{ctx.author.name}, nie znaleziono lokalizacji: {location}.")
        except Exception as e:
            await ctx.send(f"{ctx.author.name}, wystąpił błąd podczas pobierania pogody.")


if __name__ == "__main__":
    keep_alive()
    bot = Bot()
    bot.run()