import discord
from discord.ext import commands
import asyncio
import os
from gtts import gTTS
from voice_generator import creat_MP3
import discord_send_error
import time
from mutagen.mp3 import MP3
import traceback

prefix = os.environ["prefix"]

client = commands.Bot(command_prefix = prefix)

#ログイン処理
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

#入室
@client.command()
async def join(ctx):
    join_raw(ctx)

@client.command()
async def j(ctx):
    join_raw(ctx)

def join_raw(ctx):
    global ctx_join
    print('#join')
    vc = ctx.author.voice.channel
    await vc.connect()
    await ctx.channel.send('接続されたよ！')
    ctx_join = ctx

#退室
@client.command()
async def bye(ctx):
    bye_raw(ctx)

@client.command()
async def b(ctx):
    bye_raw(ctx)

def bye_raw(ctx):
    print('#bye')
    await ctx.channel.send('またね！')
    await ctx.voice_client.disconnect()

#辞書登録
@client.command()
async def register(ctx, arg1, arg2):
    register_raw(ctx,arg1,arg2)

@client.command()
async def r(ctx, arg1, arg2):
    register_raw(ctx,arg1,arg2)

def register_raw(ctx, arg1, arg2):
    with open('./dic.txt', mode='a',encoding='shift-jis') as f:
        f.write('\n'+ arg1 + ',' + arg2)
        print('dic.txtに書き込み：''\n'+ arg1 + ',' + arg2)
    await ctx.send('`' + arg1+'` を `'+arg2+'` として登録しました！')

#辞書登録
@client.command()
async def register_export(ctx):
    await ctx.channel.send(file=discord.File("dic.txt"))

#自動退出
@client.event
async def on_voice_state_update(member, before, after):
    if member.bot:
        return
    member_count = len([i.name for i in ctx_join.voice_client.channel.members])
    if after.channel != ctx_join.voice_client.channel:
        if before.channel == ctx_join.voice_client.channel:
            if member_count == 1:
                await ctx_join.channel.send('人がいなくなっちゃったから、ばいばい！')
                await ctx_join.voice_client.disconnect()

#発声
@client.event
async def on_message(message):
    try:
        if message.author.bot:
            return
        print('---on_message_start---')
        if message.content.startswith(prefix):
            pass
        elif message.channel == ctx_join.channel:
            if message.guild.voice_client:
                print("channel:" + str(message.channel))
                print("speaker:" + str(message.author.display_name))
                play_MP3(message,message.author.display_name,"output_name.mp3")
                print('content:' + str(message.content))
                play_MP3(message,message.content,"output_content.mp3")
        await client.process_commands(message)
        print('---on_message_end---')
    except:
        discord_send_error.send_error_log(traceback.format_exc())

#発声モジュール
def play_MP3(message,inputText,file_name):
    creat_MP3(inputText,file_name)
    source = discord.FFmpegOpusAudio(file_name)
    message.guild.voice_client.play(source)
    time.sleep(MP3(file_name).info.length+0.5)

client.run(os.environ["client"])
