import discord
from discord.ext import commands
import asyncio
import os
import subprocess
from gtts import gTTS
from voice_generator import creat_MP3
import discord_send_error
import time
from mutagen.mp3 import MP3

prefix = os.environ["prefix"]


client = commands.Bot(command_prefix = prefix)

voice_client = None

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


@client.command()
async def join(ctx):
    print('#join')
    print('#voicechannelを取得')
    vc = ctx.author.voice.channel
    print('#voicechannelに接続')
    await vc.connect()
    await ctx.channel.send('接続されたよ！')
    with open('./text_channel.txt',mode='w',encoding="shift-jis") as f:
        f.write(str(ctx.channel))

@client.command()
async def bye(ctx):
    print('#bye')
    print('#切断')
    await ctx.channel.send('またね！')
    await ctx.voice_client.disconnect()
    print(ctx.channel)

@client.command()
async def register(ctx, arg1, arg2):
    with open('./dic.txt', mode='a',encoding='shift-jis') as f:
        f.write('\n'+ arg1 + ',' + arg2)
        print('dic.txtに書き込み：''\n'+ arg1 + ',' + arg2)
    await ctx.send('`' + arg1+'` を `'+arg2+'` として登録しました！')

@client.event
async def on_voice_state_update(member, before, after):
    if after.channel is None:
        print("taisyutu")
        print(member.channel)
        #await member.channel.send('またね！')
        #await member.voice_client.disconnect()
"""
    server_id_test = "サーバーID"
    text_id_test = "通知させたいテキストチャンネルID"

    if member.guild.id == server_id_test:   # サーバーid
        text_ch = client.get_channel(text_id_test)   # 通知させたいTEXTチャンネルid
        if before.channel is None:
            msg = f'【VC参加ログ】{member.name} が {after.channel.name} に参加しました。'
            await text_ch.send(msg)
"""
    

@client.event
async def on_message(message):
    if message.author.bot:
        return
    with open('./text_channel.txt',mode='r',encoding='shift-jis') as f:
        text_channel = f.read()
    try:
        print('---on_message_start---')
        if message.content.startswith(prefix):
            pass
        else:
            if str(message.channel) == text_channel:
                if message.guild.voice_client:
                    print("channel:" + str(message.channel))
                    print("speaker:" + str(message.author.display_name))
                    play_MP3(message,message.author.display_name,"output_name.mp3")
                    print('content:' + str(message.content))
                    play_MP3(message,message.content,"output_content.mp3")
                else:
                    pass

        await client.process_commands(message)
        print('---on_message_end---')
    except:
        import traceback
        discord_send_error.send_error_log(traceback.format_exc())

def play_MP3(message,inputText,file_name):
    creat_MP3(inputText,file_name)
    source = discord.FFmpegOpusAudio(file_name)
    message.guild.voice_client.play(source)
    time.sleep(MP3(file_name).info.length+0.5)

client.run(os.environ["client"])
