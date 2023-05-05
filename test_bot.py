import os
import yt_dlp
import asyncio
import subprocess

import discord
from discord.ext import commands

TOKEN = "MTA5NTM2MTUxNjAyNDM4MTQ2MA.GGu8pX.kRE-BoCym-HR4-hY1RZ8phnJAkvFQ_56i-yqQM"

client = commands.Bot(command_prefix='!', intents=discord.Intents.all())

# Crear la lista de reproducción
queue = []

# Añadir una canción a la cola
@client.command()
async def add(ctx, url):
    queue.append(url)
    await ctx.send(f'🎵 ha sido añadido a la cola de reproducción 🎵')

# Reproducir la próxima canción en la cola
@client.command()
async def play_queue(ctx):
    while queue:
        url = queue[0]
        song = os.path.isfile("song.mp3")

        # Mira si la canción está en reproducción y sino borra el fichero song.mp3
        try:
            if song:
                os.remove("song.mp3")
        except PermissionError:
            await ctx.send("Error: La música ya está en reproducción.")
            return
        await ctx.send(f'🎶 Descargando canción... 🎶 🎶')
        process = subprocess.Popen("yt-dlp -f 'ba' -x --audio-format mp3 " +  url + " -o song.mp3 ", shell=True, stdout=subprocess.PIPE)
        process.wait()  
        await asyncio.sleep(1)
        await ctx.send('🕺 A bailar!! 🕺')
        
        voiceChannel = discord.utils.get(ctx.guild.voice_channels, name=ctx.author.voice.channel.name)
        await voiceChannel.connect()
        guild = ctx.guild
        voice_client = guild.voice_client
        voice_client.play(discord.FFmpegPCMAudio("song.mp3"))

        # Espera hasta que se complete la reproducción
        while voice_client.is_playing():
            await asyncio.sleep(1)

        # Elimina la canción de la cola
        queue.pop(0)

    # Sale del canal de voz al finalizar la cola
    await voice_client.disconnect()

@client.command()
async def play(ctx):
    if not queue:
        await ctx.send('❌ La cola de reproducción está vacía ❌')
        return

    if not ctx.voice_client:
        voiceChannel = discord.utils.get(ctx.guild.voice_channels, name=ctx.author.voice.channel.name)
        await voiceChannel.connect()

@client.command()
async def stop(ctx):
    voice_client = ctx.message.guild.voice_client
    await voice_client.disconnect()
    await ctx.send('👋🏻 Blanxi dice adioos 👋🏻')

@client.command()
async def pause(ctx):
    voice_client = ctx.message.guild.voice_client
    
    if not voice_client.is_paused():
        voice_client.pause()
        await ctx.send("La música se ha pausado ⏸️")
    else:
        await ctx.send("⚠️ Error: La música ya está en pausa. ⏸️")

@client.command()
async def resume(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_paused():
        voice_client.resume()
        await ctx.send("🔊 La música se ha vuelto a reproducir 🔊")
        await asyncio.sleep(3)
        await ctx.message.delete()

# Reproducir la próxima canción en la cola
@client.command()
async def next(ctx):
    if queue:
        await play_queue(ctx, queue[0])
        queue.pop(0)
    else:
        await ctx.send('❌No hay más canciones en la cola❌')

client.run(TOKEN)
