import discord
from discord.ext import commands
import asyncio
import os
import subprocess
from gtts import gTTS
from voice_generator import creat_MP3
import discord_send_error
import time

prefix = '?'#dev
#prefix = '.'#main

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

@client.command()
async def register(ctx, arg1, arg2):
    with open('./dic.txt', mode='a',encoding='shift-jis') as f:
        f.write('\n'+ arg1 + ',' + arg2)
        print('dic.txtに書き込み：''\n'+ arg1 + ',' + arg2)
    await ctx.send('`' + arg1+'` を `'+arg2+'` として登録しました！')

@client.event
async def on_voice_state_update(member, before, after):
    server_id_test = "サーバーID"
    text_id_test = "通知させたいテキストチャンネルID"


    if member.guild.id == server_id_test:   # サーバーid
        text_ch = client.get_channel(text_id_test)   # 通知させたいTEXTチャンネルid
        if before.channel is None:
            msg = f'【VC参加ログ】{member.name} が {after.channel.name} に参加しました。'
            await text_ch.send(msg)

@client.event
async def on_message(message):
    if message.author.bot:
        return
    with open('./text_channel.txt',mode='r',encoding='shift-jis') as f:
        text_channel = f.read()
    print(message.author.display_name)
    try:
        print('---on_message_start---')
        msgclient = message.guild.voice_client
        print(msgclient)
        print(discord.opus.is_loaded())
        print(message.channel)

        if message.content.startswith(prefix):
            pass
        else:
            if str(message.channel) == text_channel:
                if message.guild.voice_client:
                    creat_MP3(message.author.display_name,'output_name.mp3')
                    source = discord.FFmpegOpusAudio("./output_name.mp3")
                    message.guild.voice_client.play(source)
                    time.sleep(2)
                    print('#message.content:'+ message.content)
                    creat_MP3(message.content,'output_content.mp3')
                    source = discord.FFmpegOpusAudio("./output_content.mp3")
                    message.guild.voice_client.play(source)
                else:
                    pass

        await client.process_commands(message)
        print('---on_message_end---')
    except:
        import traceback
        discord_send_error.send_error_log(traceback.format_exc())

client.run("Nzk0OTQxMzU1MDc0NzgxMjU0.X_CI1A.4wTuK0UhfprkJKTJGNy_4Iuy4aY")#dev
#client.run("Nzk0NTY1MTE3OTc4NDc2NTU0.X-8qbg.hoWlswUZztYE0pYM5e9clscITtQ")#main
