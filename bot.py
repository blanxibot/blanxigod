#bot.py
import os
import yt_dlp
import asyncio
import subprocess

import discord
from discord.ext import commands
#from dotenv import load_dotenv

#load_dotenv()
TOKEN = "x"

client = commands.Bot(command_prefix='!', intents=discord.Intents.all())

# Comando !helloworld
@client.command()
async def ayuda(ctx):
    await ctx.send('⚪️!play + url música \➡️ El bot se unirá al canal de voz y reproducirá la música seleccionada. ▶️\n⚪️!stop \➡️ La música que se está reproduciendo en el momento se parará y el bot abandonará el canal de voz. ⏹️\n⚪️!pause \➡️ La música que se está reproduciendo en el momento se parará. ⏸️\n⚪️!resume \➡️ La música que se está reproduciendo en el momento se reanudará. ⏯️')

@client.command()
async def play(ctx, url):
    song = os.path.isfile("song.mp3")

    # Mira si la canción está en reproducción y sino borra el fichero song.mp3
    try:
        if song:
            os.remove("song.mp3")
    except PermissionError:
        await ctx.send("Error: La música ya está en reproducción.")
        return
    
    await ctx.send('🎶 Descargando canción... 🎶 🎶', delete_after=5)
    process = subprocess.Popen("yt-dlp -f 'ba' -x --audio-format mp3 " +  url + " -o song.mp3 ", shell=True, stdout=subprocess.PIPE)
    process.wait() 
    await asyncio.sleep(1)
    await ctx.send('🕺 A bailar!!! 🕺'delete_after=5)
    

    # Descomentar para descargar canción
    #loop = asyncio.get_event_loop()
    #await loop.run_in_executor(None, download_to_mp3, url)

    voiceChannel = discord.utils.get(ctx.guild.voice_channels, name=ctx.author.voice.channel.name)
    await voiceChannel.connect()
    guild = ctx.guild
    voice_client = guild.voice_client

    voice_client.play(discord.FFmpegPCMAudio("song.mp3"))
        
    
@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.command()
async def stop(ctx):
    voice_client = ctx.message.guild.voice_client
    await voice_client.disconnect()
    voice_client.disconnect()
    await ctx.send('👋🏻 Blanxi dice adioos 👋🏻', delete_after=5)

@client.command()
async def pause(ctx):
    voice_client = ctx.message.guild.voice_client
    if not voice_client.is_paused():
        voice_client.pause()
        await ctx.send("La música se ha pausado ⏸️", delete_after=5)
    else:
        await ctx.send("⚠️Error: La música ya está en pausa. ⏸️", delete_after=5)
        
@client.command()
async def resume(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_paused():
        voice_client.resume()
        await ctx.send("🔊 La música se ha vuelto a reproducir 🔊", delete_after=5)
    else:
        await ctx.send("⚠️Error: La música no está en pausa 🔊", delete_after=5)
client.run(TOKEN)