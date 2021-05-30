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

client = commands.Bot(command_prefix=prefix)

ctx_join = None


# ログイン処理
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


# 入室
@client.command()
async def join(ctx):
    global ctx_join
    global guild
    guild = ctx.guild
    print('#join')
    print(type(ctx_join))
    vc = ctx.author.voice.channel
    await vc.connect()
    await ctx.channel.send('接続されたよ！')
    ctx_join = ctx


# 退室
@client.command()
async def bye(ctx):
    print('#bye')
    await ctx.channel.send('またね！')
    await ctx.voice_client.disconnect()


# 辞書登録
@client.command()
async def register(ctx, arg1, arg2):
    with open('./dic.txt', mode='r', encoding='shift-jis') as f:
        r = f.read()
    with open('./dic.txt', mode='w', encoding='shift-jis') as f:
        f.write(arg1 + ',' + arg2 + '\n' + r)
        print('dic.txtに書き込み：''\n' + arg1 + ',' + arg2)
    await ctx.send('`' + arg1+'` を `'+arg2+'` として登録しました！')


# 辞書登録
@client.command()
async def register_export(ctx):
    await ctx.channel.send(file=discord.File("dic.txt"))


# 自動退出
@client.event
async def on_voice_state_update(member, before, after):
    if ctx_join is None:
        return
    if member.bot:
        return
    member_count = len([i.name for i in ctx_join.voice_client.channel.members])
    if after.channel != ctx_join.voice_client.channel:
        if before.channel == ctx_join.voice_client.channel:
            if member_count == 1:
                await ctx_join.channel.send('人がいなくなっちゃったから、ばいばい！')
                await ctx_join.voice_client.disconnect()


# 発声
@client.event
async def on_message(message):
    try:
        if message.author.bot:
            return
        print('---on_message_start---')
        if message.content.startswith(prefix):
            pass
        elif ctx_join is None:
            pass
        elif message.channel == ctx_join.channel:
            if message.guild.voice_client:
                print("channel:" + str(message.channel))
                print("speaker:" + str(message.author.display_name))
                play_MP3(message, message.author.display_name,
                         "output_name.mp3")
                print('content:' + str(message.content))
                play_MP3(message, message.content, "output_content.mp3")
        await client.process_commands(message)
        print('---on_message_end---')
    except:
        discord_send_error.send_error_log(traceback.format_exc())


# 発声モジュール
def play_MP3(message, inputText, file_name):
    creat_MP3(inputText, file_name)
    source = discord.FFmpegOpusAudio(file_name)
    message.guild.voice_client.play(source)
    time.sleep(MP3(file_name).info.length+0.5)


# アモアス
@client.command()
async def a(ctx, arg="", *member_count):
    bot_vc = ctx_join.guild.me.voice.channel  # botのいるボイスチャンネルを取得

    if arg == "start":
        global member_list
        global death_list
        member_list = bot_vc.members
        n = 0
        bot_message = ""
        for member in bot_vc.members:
            bot_message += str(member)+"  :"+str(n)+"\n"
            n += 1
        death_list=[]
        death_list_num=[False]*n
        embed = discord.Embed(title="ゲームスタート", description=bot_message)
        await ctx.channel.send(embed=embed)



    elif arg == "m" or arg == "mute":
        # ミュート処理(オフからオン)
        for member in bot_vc.members:
            await member.edit(mute=True)
            await member.edit(deafen=True)
        for member in death_list:
            await member.edit(mute=False)
            await member.edit(deafen=False)

        bot_message = "ミュートをオンにしました。"
        embed = discord.Embed(title="ミュート", description=bot_message)
        await ctx.channel.send(embed=embed)



    elif arg == "d" or arg == "die" or arg == "unmute" or arg == "u":
        for member in member_count:
            death_list+=member
            death_list_num+=int(member)

        # ミュート処理(オンからオフ)
        for member in bot_vc.members:
            await member.edit(mute=False)
            await member.edit(deafen=False)
        for member in death_list:
            await member.edit(mute=True)

        bot_message = "ミュートをオフにしました。"
        embed = discord.Embed(title="ミュート", description=bot_message)
        await ctx.channel.send(embed=embed)

        #生き残り
        n = 0
        bot_message = ""
        for member in member_list:
            if death_list_num[n] == False:
                bot_message += str(member)+"  :"+str(n)+"\n"
            n += 1
        embed = discord.Embed(title="生き残り", description=bot_message)
        await ctx.channel.send(embed=embed)        
        


    elif arg == "ban":
        for member in member_count:
            death_list+=member
            death_list_num+=int(member)
        
        #生き残り
        n = 0
        bot_message = ""
        for member in member_list:
            if death_list_num[n] == False:
                bot_message += str(member)+"  :"+str(n)+"\n"
            n += 1
        embed = discord.Embed(title="生き残り", description=bot_message)
        await ctx.channel.send(embed=embed)

        # ミュート処理(オフからオン)
        for member in bot_vc.members:
            await member.edit(mute=True)
            await member.edit(deafen=True)
        for member in death_list:
            await member.edit(mute=False)
            await member.edit(deafen=False)

        bot_message = "ミュートをオンにしました。"
        embed = discord.Embed(title="ミュート", description=bot_message)
        await ctx.channel.send(embed=embed)
        


    elif arg == "end":
        # ミュート処理
        for member in bot_vc.members:
            await member.edit(mute=False)
            await member.edit(deafen=False)

        bot_message = "ミュートをオフにしました。"
        embed = discord.Embed(title="ミュート", description=bot_message)
        await ctx.channel.send(embed=embed)



    else:
        bot_message = "Among Usモードへようこそ！\n`"\
            + prefix+"a`でいつでも操作方法を見ることができます。\n`"\
            + prefix+"a start`でゲームを開始します。\n`"\
            + prefix+"a m`または`"+prefix+"a mute`で全員をサーバーミュートにします。\n`"\
            + prefix+"a d 人 人...`または`"+prefix+"a die 人 人...`で死んだ人をミュートし、他の人のミュートを解除します。但し、人は番号で指定してください。\n`"\
            + prefix+"a end`でゲームを終了し、全員をメインチャンネルに戻します。\n"
        embed = discord.Embed(title="各種コマンド説明", description=bot_message)
        await ctx.channel.send(embed=embed)

'''
async def mute(ctx,bot_vc,arg=False):
    for member in bot_vc.members:
        await member.edit(mute=arg)
    if arg:
        bot_message="ミュートをオンにしました。"
    else:
        bot_message="ミュートをオフにしました。"
    embed = discord.Embed(title="ミュート",description=bot_message)
    await ctx.channel.send(embed=embed)
'''

client.run(os.environ["client"])