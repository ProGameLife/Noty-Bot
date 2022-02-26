import os
from dotenv import load_dotenv
import discord
import requests
import asyncio
from json import loads

client = discord.Client()
load_dotenv(verbose=True)

twitch_Client_ID = os.getenv('TWITCH_CLIENT_ID')
twitch_Client_secret = os.getenv('TWITCH_CLIENT_SECRET')
discord_Token = os.getenv('DISCORD_TOKEN')
discord_channelID = os.getenv('DISCORD_CHANNELID')
discord_bot_state = '방송 모니터링'
ment = '방송 켰다 드가자~'

ralro = '<@&945893180656734239>'
kimdo = '<@&945902518704156702>'
salgu = '<@&945916718226747413>'
twitchID = ['viichan6', 'cotton__123', 'jingburger', 'vo_ine', 'lilpaaaaaa', 'gosegugosegu', 'kimdoe', 'sal_gu', 'aba4647']
check = [False, False, False, False, False, False, False, False, False]
lastgameid = ['', '', '', '', '', '', '', '', '']
newgameid = ['', '', '', '', '', '', '', '', '']


@client.event
async def on_ready():
    print("ready")

    # 디스코드 봇 상태 설정
    game = discord.Game(discord_bot_state)
    await client.change_presence(status=discord.Status.online, activity=game)

    # 채팅 채널 설정
    channel = client.get_channel(944168212436746292)

    # 트위치 api 2차인증
    oauth_key = requests.post(
        "https://id.twitch.tv/oauth2/token?client_id="
        + twitch_Client_ID
        + "&client_secret="
        + twitch_Client_secret
        + "&grant_type=client_credentials")
    access_token = loads(oauth_key.text)["access_token"]
    token_type = 'Bearer '
    authorization = token_type + access_token

    while True:
        print("ready on Notification")
        print(check)
        # 트위치 api에게 방송 정보 요청
        headers = {'client-id': twitch_Client_ID, 'Authorization': authorization}

        for i, x in enumerate(twitchID):
            response_channel = requests.get('https://api.twitch.tv/helix/streams?user_login=' + x, headers=headers)
            print(response_channel.text)
            # 라이브 상태 체크
            try:
                # game_id
                # 탈콥 = 491931, 롤 = 21779, 저챗 = 509658
                twitch_channel_response = loads(response_channel.text)['data'][0]
                category = twitch_channel_response['game_name']
                title = twitch_channel_response['title']
                link = ment + '\nhttps://www.twitch.tv/' + x
                newgameid[i] = twitch_channel_response['game_id']

                if not (lastgameid[i] == newgameid[i] and twitch_channel_response['user_login'] != 'kimdoe'):
                    lastgameid[i] = newgameid[i]
                    check[i] = False

                if not (twitch_channel_response['type'] == 'live' and check[i] is False):
                    continue

                if twitch_channel_response['user_login'] == 'kimdoe':
                    await channel.send(kimdo + title + '\n' + category + ' ' + link)
                elif (twitch_channel_response['game_id'] == '21779'
                        or twitch_channel_response['game_id'] == '509658') and \
                        twitch_channel_response['user_login'] == 'aba4647':
                    await channel.send(ralro + title + '\n' + category + ' ' + link)
                elif twitch_channel_response['game_id'] == '491931' and \
                        twitch_channel_response['user_login'] == 'sal_gu':
                    await channel.send(salgu + title + '\n' + category + ' ' + link)
                else:
                    await channel.send(title + '\n' + category + ' ' + link)
                    print("Online")
                check[i] = True
                print(x)
            except:
                print("Offline")
                check[i] = False

            await asyncio.sleep(10)
        await asyncio.sleep(100)


client.run(discord_Token)
