import subprocess
from gtts import gTTS
import re

# ************************************************
# remove_custom_emoji
# 絵文字IDは読み上げない
# ************************************************
def remove_custom_emoji(text):
    
    #pattern = r'<:[a-zA-Z0-9_]+:[0-9]+>'    # カスタム絵文字のパターン
    pattern = r'<:'    # カスタム絵文字のパターン
    text = re.sub(pattern,'',text)   # 置換処理
    pattern = r':[0-9]+>'    # カスタム絵文字のパターン
    return re.sub(pattern,'',text)   # 置換処理

# ************************************************
# url_shouryaku
# URLなら省略
# ************************************************
def url_shouryaku(text):
    pattern = "https?://[\w/:%#\$&\?\(\)~\.=\+\-]+"
    return re.sub(pattern,'URLは省略するのデス！',text)   # 置換処理

# ************************************************
# remove_picture
# 画像ファイルなら読み上げない
# ************************************************
def remove_picture(text):
    pattern = r'.*(\.jpg|\.jpeg|\.gif|\.png|\.bmp)'
    return re.sub(pattern,'',text)   # 置換処理

# ************************************************
# remove_command
# コマンドは読み上げない
# ************************************************
def remove_command(text):
    pattern = r'^\!.*'
    return re.sub(pattern,'',text)   # 置換処理

# ************************************************
# remove_log
# 参加ログは読み上げない
# ************************************************
def remove_log(text):
    pattern = r'(\【VC参加ログ\】.*)'
    return re.sub(pattern,'',text)   # 置換処理

# ************************************************
# user_custam
# ユーザ登録した文字を読み替える
# ************************************************

def user_custam(text):

    #f = open('C:/open_jtalk/bin/dic.txt', 'r')
    f = open('./dic.txt', 'r')
    line = f.readline()

    while line:
        pattern = line.strip().split(',')
        if pattern[0] in text:
            text = text.replace(pattern[0], pattern[1])
            print('置換後のtext:'+text)
            break
        else:
            line = f.readline()
    f.close()

    return text



# ************************************************
# creat_WAV
# message.contentをテキストファイルと音声ファイルに書き込む
# 引数：inputText
# 書き込みファイル：input.txt、output.wav
# ************************************************
def creat_WAV(inputText):
        # message.contentをテキストファイルに書き込み

    inputText = remove_custom_emoji(inputText)   # 絵文字IDは読み上げない
    inputText = remove_command(inputText)   # コマンドは読み上げない
    inputText = url_shouryaku(inputText)   # URLなら省略
    inputText = remove_picture(inputText)   # 画像なら読み上げない
    inputText = remove_log(inputText)   # 参加ログなら読み上げない
    inputText = user_custam(inputText)   # ユーザ登録した文字を読み替える
    input_file = 'input.txt'

    with open(input_file,'w',encoding='shift_jis') as file:
        file.write(inputText)

    tts = gTTS(text=inputText, lang='ja')
    tts.save('./output.mp3')

    return True

if __name__ == '__main__':
    creat_WAV('テスト')
