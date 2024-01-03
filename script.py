from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import pandas as pd
import datetime

token_bot = "MTE5MjAzNDQ1MzIyMTAyMzgxNA.GlWvIS.c2UoH_3ed0CRZHUR-_wBSdVwCidoMOuR1-EWW4"

import nest_asyncio
nest_asyncio.apply()

import discord
from discord.ext import commands

# Función para enviar un mensaje
async def enviar_mensaje(channel_id, mensaje, token_bot=token_bot):
    # Configurar intents
    intents = discord.Intents.default()
    intents.messages = True  # Puedes ajustar estos según tus necesidades

    # Configurar el bot con intents
    bot = commands.Bot(command_prefix='!', intents=intents)

    # Evento cuando el bot está listo
    @bot.event
    async def on_ready():
        print(f'Bot conectado como {bot.user.name}')

        # Obtén el canal por ID
        channel = bot.get_channel(channel_id)

        # Verifica que el canal existe y no es None
        if channel:
            # Envía un mensaje al canal
            await channel.send(mensaje)
            # Cerrar el bot después de enviar el mensaje
            await bot.close()

        else:
            print(f"No se pudo encontrar el canal con ID {channel_id}")

    # Ejecutar el bot con el token
    bot.run(token_bot)

# Función para sacar info del LSE
def get_news_lse(ticker):
    url = f"https://www.lse.co.uk/rns/{ticker}/"

    # Entrar en la web
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req)
    soup = BeautifulSoup(webpage, 'html.parser')

    # Parte de la web en la que hay la tabla
    rns_table = soup.find_all('table')
  
    # Con esto encontramos los links y los encabezados de la noticia
    tag = rns_table[0].find_all('a')

    # Falta encontrar las fechas de la noticia
    date = rns_table[0].find_all('td')

    date_n = []
    href_n = []
    title_n = []

    count = 0
    for i in range(len(tag)):
      date_n.append(date[count].text)
      href_n.append(tag[i].attrs['href'])
      title_n.append(tag[i].text)

      count += 4


    df = pd.DataFrame({'Date': date_n, 'Title': title_n, 'Link': href_n})
    df.Date = pd.to_datetime(df.Date)

    if df.Date[0].date() == datetime.date.today():
        row = df.iloc[0]
        print('En la fecha de hoy {} hay una noticia de {} en {}'.format(row.Date.strftime("%Y/%m/%d"), row.Title, row.Link)) 
    else:
        print('No hay noticia de hoy')

    return df

# Tickers que buscamos
tickers = tickers = ['KIST', 'AET', 'KSPI']

# Bucle para buscar info en los tickers
for tck in tickers:
    print(tck)
    df_news = get_news_lse(tck)

    if df_news.Date[0].date() == datetime.date.today():
        row = df_news.iloc[0]
        mensaje = f'En la fecha de hoy {row.Date.strftime("%Y/%m/%d")} hay una noticia de {row.Title} en {row.Link}'
        await enviar_mensaje(1192039992097247252, mensaje) 
    else:
        pass
