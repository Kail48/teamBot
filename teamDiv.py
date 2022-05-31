
import discord
import random
TOKEN=""             #Your Token for the bot set at developers's portal
help_message="To create a team You need following things:\n-Three servers with name that has no space between them.\n-The first server is where all the members are.\n-The two destinations servers where the members must be equally and randomly divided.\n-Enter command like this: ($team source team1 team2) replace the source,team1 and team 2 with the channels in your server you would like as explained above"
help_message2="\nIf it doesnt work:\n-Check your spellings and upper-lower cases.\n-Try disconnecting from the channel and reconnect again.\n                                                           -Created by Condorrianno"
#-------------------This section deals with granting your bot different discord permissions----------
intents = discord.Intents.default()
permissions=discord.Permissions()
permissions.move_members=True
intents.members=True
intents.messages=True
#-----------------------------------------------
client = discord.Client()

def teamCreate(list_of_members):           #returns two lists by selecting random half number of members from the list provided
    if len(list_of_members)%2!=0:          # the given list contains id of all the members in the main channel 
        print("Uneven members")
        return
    ls1=[]
    ls2=[]
    while list_of_members:
        randomItem=random.choice(range(len(list_of_members)))   #Randomly chose members from the list and put them to a team 
        item1=list_of_members.pop(randomItem)
        ls1.append(item1)
        randomItem=random.choice(range(len(list_of_members)))
        item2=list_of_members.pop(randomItem)
        ls2.append(item2)
    return {'team 1':ls1,'team 2':ls2}

async def move(sourceId,dest1Id,dest2Id):               #This contains api code to move the members to different channel
    global client
    source_channel=await client.fetch_channel(sourceId)
    guild=source_channel.guild
    dest_channel_1=await client.fetch_channel(dest1Id)
    print(f"chaneel 1: {dest_channel_1}")
    dest_channel_2=await client.fetch_channel(dest2Id)
    print(f"chaneel 2: {dest_channel_2}")
    member_list=[]
    for member in source_channel.members:
        member_list.append(member.id)
    print(f"found {len(member_list)} members")
    print(member_list)
    divided_list=teamCreate(member_list)
    print(divided_list)
    if divided_list==None:
        return
    t1=divided_list['team 1']
    t2=divided_list['team 2']
    
    while t1:
        memid=t1.pop()
        mem=await guild.fetch_member(memid)
        print(f"Got member: {mem}")
        await mem.move_to(dest_channel_1)
    while t2:
        memid=t2.pop()
        mem=await guild.fetch_member(memid)
        print(f"Got member: {mem}")
        await mem.move_to(dest_channel_2)
    
gd={}
g=None
client = discord.Client()
chid={}
memb={}
def getMembers(ch):
    m={}
    l=[]
    for y in ch.members:
        l.append([y.name,y.id])
    for i in l:
        m[l[0]]=l[1]
    return m
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    guilds = await client.fetch_guilds(limit=150).flatten()
    for i in guilds:
        gd[i.name]=i.id
    chs=[y for y in client.get_all_channels()]
    y=[]
    for ch in chs:
        y.append([ch.name,ch.id])
    for i in y:
        chid[i[0]]=i[1]
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('$help'):
        await message.channel.send(help_message+'\n'+help_message2)
    if message.content.startswith('$channel'):
        await message.channel.send(chid)
    if message.content.startswith('$getId'):
        cmdList=message.content.split(" ")
        id=chid[cmdList[1]]
        await message.channel.send(id)
    if message.content.startswith('$team'):
        cmdList=message.content.split(" ")
        source=chid[cmdList[1]]
        dest1=chid[cmdList[2]]
        dest2=chid[cmdList[3]]
        await move(source,dest1,dest2)
    if message.content.startswith('$gd'):
        await message.channel.send(gd) 

          

client.run(TOKEN)