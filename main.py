# Importación de librerías necesarias
import discord  # Librería principal para interactuar con la API de Discord
from discord.ext import commands  # Extensiones de comandos para crear bots
from model import get_class  # Función personalizada para clasificar imágenes
import os, random  # Módulos estándar para manejo del sistema y generación aleatoria
import requests  # Librería para realizar solicitudes HTTP

# Configuración de los "intents" para permitir que el bot lea el contenido de los mensajes
intents = discord.Intents.default()
intents.message_content = True

# Creación de una instancia del bot con prefijo de comando '$' y los intents definidos
bot = commands.Bot(command_prefix='$', intents=intents)

# Evento que se ejecuta cuando el bot ha iniciado correctamente
@bot.event
async def on_ready():
    print(f'Hemos iniciado sesión como {bot.user}')  # Mensaje en consola al iniciar el bot

# Función que obtiene una URL aleatoria de imagen de pato desde una API pública
def get_duck_image_url():
    url = 'https://random-d.uk/api/random'  # URL de la API
    res = requests.get(url)  # Realiza una solicitud HTTP GET
    data = res.json()  # Convierte la respuesta en un diccionario Python
    return data['url']  # Retorna solo la URL de la imagen

# Comando del bot que envía una imagen aleatoria de pato al canal donde se invocó
@bot.command('duck')
async def duck(ctx):
    '''El comando "duck" devuelve la foto del pato'''
    print('hello')  # Mensaje de depuración en consola
    image_url = get_duck_image_url()  # Obtiene la URL de la imagen
    await ctx.send(image_url)  # Envía la imagen al canal

# Comando del bot que permite analizar una imagen enviada por el usuario
@bot.command()
async def check(ctx):
    # Verifica si el mensaje contiene archivos adjuntos (imágenes)
    if ctx.message.attachments:
        for attachment in ctx.message.attachments:
            file_name = attachment.filename  # Nombre del archivo
            file_url = attachment.url  # URL del archivo
            # Guarda la imagen en el directorio actual
            await attachment.save(f"./{attachment.filename}")
            # Llama a la función de clasificación de imagen y envía el resultado al canal
            await ctx.send(get_class(
                model_path="./keras_model.h5",  # Ruta del modelo de clasificación
                labels_path="labels.txt",  # Ruta del archivo de etiquetas
                image_path=f"./{attachment.filename}"  # Ruta de la imagen guardada
            ))
    else:
        # Mensaje de error si el usuario no adjunta una imagen
        await ctx.send("Olvidaste subir la imagen :(")

# Ejecuta el bot con el token de autenticación
bot.run('TOKEN')  # Reemplaza 'TOKEN' con tu token real del bot de Discord