import discord
from discord.ext import commands
import libs.gpt3 as gpt3
import libs.ImageGrid as ImageGrid
import requests
from discord.ui import Button,View

api_token="YOUR_TOKEN"

intents = discord.Intents.default()
intents.message_content = True
prefix='!'
bot = commands.Bot(command_prefix=prefix, intents=intents)
channelToSend=''

@bot.event
async def on_ready():
    print('Bot Started!')

@bot.event
async def on_message(message):
    #Check if prefix is used
    if (message.content[0] == prefix):
        if (message.author == bot.user):
            return
        userCommand=str(message.content[1:]).split(' ')

        # Process Commands From User
        match userCommand[0]:
            case 'gpt3':
                await send(message, 'Processing...', 'norm')
                msgContent = (str(message.content).replace(prefix,'').replace(userCommand[0],'').strip())
                generatedText = gpt3.textPrompt(msgContent)
                await send(message, generatedText, 'norm')
            case 'image':
                await send(message, 'Processing...', 'norm')
                try:
                    msgContent = (str(message.content).replace(prefix,'').replace(userCommand[0],'').strip())
                    generatedImgUrls = gpt3.imgPrompt(msgContent)
                    imgGridPath = ImageGrid.create_image_grid(generatedImgUrls)        
                    await send(message, imgGridPath, 'imgGen', generatedImgUrls)
                except requests.exceptions.MissingSchema:
                    await send(ctx=message, msg='Trial Ended, Make New Token!', request='norm')
            case 'test':
                await send(message, '', 'button')
            case other:
                await send(message, 'Not A Command!', 'norm')

class AllMightyButton(str):
    def __init__(self, url):
        self.url = url
        super().__init__()

    def create(self, label, style, row, function):
        button = Button(label=label, style=style, row=row)
        button.callback = eval('self.'+function)
        return button
    async def pickImage(self, interaction: discord.Interaction):
        await interaction.response.send_message(self.url)
    async def variationImage(self, interaction: discord.Interaction):
        mention=interaction.user.mention
        await interaction.response.send_message(f"{mention} Processing...")
        imgUrls = gpt3.imgVariation(imgUrl=self.url)
        imgGridPath = ImageGrid.create_image_grid(imgUrls)
        await interaction.channel.send(f"{mention}", file=discord.File(imgGridPath), view=await loadButtons(imgUrls))

async def loadButtons(urlList):
    u1 = AllMightyButton(urlList[0]).create(label='U1', style=discord.ButtonStyle.gray, row=1, function='pickImage')
    u2 = AllMightyButton(urlList[1]).create(label='U2', style=discord.ButtonStyle.gray, row=1, function='pickImage')
    u3 = AllMightyButton(urlList[2]).create(label='U3', style=discord.ButtonStyle.gray, row=1, function='pickImage')
    u4 = AllMightyButton(urlList[3]).create(label='U4', style=discord.ButtonStyle.gray, row=1, function='pickImage')

    v1 = AllMightyButton(urlList[0]).create(label='V1', style=discord.ButtonStyle.gray, row=2, function='variationImage')
    v2 = AllMightyButton(urlList[1]).create(label='V2', style=discord.ButtonStyle.gray, row=2, function='variationImage')
    v3 = AllMightyButton(urlList[2]).create(label='V3', style=discord.ButtonStyle.gray, row=2, function='variationImage')
    v4 = AllMightyButton(urlList[3]).create(label='V4', style=discord.ButtonStyle.gray, row=2, function='variationImage')

    view=View()

    view.add_item(u1)
    view.add_item(u2)
    view.add_item(u3)
    view.add_item(u4)
    view.add_item(v1)
    view.add_item(v2)
    view.add_item(v3)
    view.add_item(v4)
    return view

async def send(ctx, msg, request, other=None):
    mention = ctx.author.mention
    match request:
        case 'imgGen':
            if msg == 'pornblocker':
                await ctx.reply('STOP TRYING TO MAKE PORN!', mention_author=True)
            elif msg == 'trialEnd':
                await ctx.reply('No More Credits!', mention_author=True)
            else:
                await ctx.channel.send(f"{mention}", file=discord.File(msg), view=await loadButtons(urlList=other))
        case 'norm':
            if (msg == 'badprompt'):
                await ctx.channel.send(f'{mention}, Reduce Your Prompt!')
            elif msg == 'trialEnd':
                await ctx.reply('No More Credits!', mention_author=True)
            else:
                await ctx.channel.send(f'{mention}, {msg}')

def run():
    bot.run(api_token)