#importing required modules
import os
import discord
import requests
import json
import random
from dotenv import load_dotenv
from discord.ext import commands
import mysql.connector

load_dotenv()

intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix='$', intents=intents)

@bot.command()
async def greaseTest(ctx, arg):
    await ctx.send(arg)

@bot.command()
async def bal(ctx, arg):
    if getUserBalance(arg[2:-1]) == -1:
        await ctx.send(embed=createUserRetrivalError(arg))
    await ctx.send(embed=createUserBalanceRetrival(arg, getUserBalance(arg[2:-1])[0]))

@bot.command(pass_context=True)
@commands.has_role("Admin")
async def give(ctx,user:discord.Member, points):
    if (int(points) > 0):
        addPointsToUser(user.id, int(points))

@bot.command(pass_context=True)
async def buy(ctx, itemname):
    if str(ctx.message.channel.id) == os.getenv("pointsShopID"):
        purchaseResult = await userAttemptToBuy(itemname, ctx.message.author)
        if not purchaseResult[1] == None:
            role = discord.utils.get(ctx.guild.roles, name=purchaseResult[1])
            await ctx.message.author.add_roles(role)
        await ctx.send(embed=purchaseResult[0])

@bot.command(pass_context=True)
@commands.has_role("Admin")
async def take(ctx,user:discord.Member, points):
    if (int(points) > 0):
        if (removePointsFromUser(user.id, int(points))):
            await ctx.send(embed=createUserTakePoints(user.mention, points, getUserBalance(user.id)))
        else:
            await ctx.send(embed=attemptToRemoveMoreThanBalError(user.mention, points, getUserBalance(user.id)))

@bot.event
async def on_message(message):
  #check who sent the message
  if message.author == bot.user:
    return
  msg = message.content
  if msg.lstrip() == "$bal":
    if getUserBalance(message.author.id) == -1:
        addNewUser(message.author.id)
    await message.channel.send(embed=createUserBalanceRetrival(message.author.mention, getUserBalance(message.author.id)[0]))
  if len(message.attachments) != 0:
    if str(message.channel.id) == os.getenv("successHaulChID"):
        if message.attachments[0].content_type == "image/png":
            addPointsToUser(message.author.id, 3)
            await message.channel.send(embed=createDealSuccessImageEmbed(message, 3))
        elif message.attachments[0].content_type == "image/jpeg":
            addPointsToUser(message.author.id, 3)
            await message.channel.send(embed=createDealSuccessImageEmbed(message, 3))
    if str(message.channel.id) == os.getenv("successChID") or str(message.channel.id) == os.getenv("exSuccessChID"):
        if message.attachments[0].content_type == "image/png":
            addPointsToUser(message.author.id, 1)
            await message.channel.send(embed=createDealSuccessImageEmbed(message, 1))
        elif message.attachments[0].content_type == "image/jpeg":   
            addPointsToUser(message.author.id, 1)
            await message.channel.send(embed=createDealSuccessImageEmbed(message, 1))
  if str(message.channel.id) == os.getenv("pointsShopID"):
    if msg.lstrip() == "$store":
            await message.channel.send(embed=createStoreEmbed())

  await bot.process_commands(message)

def getUserBalance(id):
    ctx = connectToPointsSystemDatabase()
    cursor = ctx.cursor()
    cursor.execute("SELECT balance FROM users WHERE userId = %s;", [id])
    finalValue = cursor.fetchone()
    if not finalValue:
        return -1
    return finalValue
    ctx.close()

def addNewUser(id):
    ctx = connectToPointsSystemDatabase()
    cursor = ctx.cursor()
    finalValue = cursor.execute("INSERT INTO users (userId, balance) VALUES (%s, 0);", [id])
    ctx.commit()
    ctx.close()

def addPointsToUser(id, ammount):
    return changePoints(True, id, ammount)

def removePointsFromUser(id, ammount):
    return changePoints(False, id, ammount)

def changePoints(add, id, ammount):
    currBalance = getUserBalance(id)[0]
    ctx = connectToPointsSystemDatabase()
    cursor = ctx.cursor()
    ammountToApply = int()
    if (add):
        ammountToApply = ammount
    else:
        if (currBalance < ammount): 
            return False
        ammountToApply = -ammount
    finalValue = cursor.execute("UPDATE users SET balance = %s WHERE userId = %s;", [currBalance + ammountToApply, id])
    ctx.commit()
    ctx.close()
    return True

def getStoreItems():
    ctx = connectToPointsSystemDatabase()
    cursor = ctx.cursor()
    finalResult = list()
    cursor.execute("SELECT * FROM listedrewards;")
    for row in cursor.fetchall():
        finalResult.append(row)
    return finalResult

async def userAttemptToBuy(itemname, userObj):
    ctx = connectToPointsSystemDatabase()
    cursor = ctx.cursor()
    cursor.execute("SELECT * FROM listedrewards WHERE item_name = %s;", [itemname])
    itemTobuy = cursor.fetchone()

    if itemTobuy != None:
        if not itemTobuy[4] == None and not isUserAlreadyInRole(userObj, itemTobuy[4]):
            if removePointsFromUser(userObj.id, itemTobuy[2]):
                return [createUserCompletedPurchaseAlert(userObj.mention,getUserBalance(userObj.id)), itemTobuy[4]]
            else:
                return [userCannotAffordRewardError(userObj.mention, itemTobuy[2], getUserBalance(userObj.id)), None]
        elif itemTobuy[4] == None:
            if removePointsFromUser(userObj.id, itemTobuy[2]):
                return [createUserCompletedPurchaseAlert(userObj.mention,getUserBalance(userObj.id)), None]
            else:
                return [userCannotAffordRewardError(userObj.mention, itemTobuy[2], getUserBalance(userObj.id)), None]
        else:
            return [userAttemptedTwoBuyRoleOwned(userObj.mention, itemTobuy[1]), None]
    else:
        return [noSuchItemOnTheStoreError(userObj.mention, itemname), None]

def connectToPointsSystemDatabase():
    return mysql.connector.connect(user=os.getenv("pointsDatabaseUser"), password=os.getenv("pointsDatabasePassword"),
                              host=os.getenv("pointsDatabaseHost"),
                              database=os.getenv("pointsDatabaseName"))

def createDealSuccessImageEmbed(message, pointCount):
    embed=discord.Embed(title=":white_check_mark: Success!", description="{} earned **{} point(s)!** Total {} points! 🥳".format(message.author.mention, pointCount, getUserBalance(message.author.id)[0]), color=0xFF5733)
    return embed

def createUserBalanceRetrival(userToGet, points):
    embed=discord.Embed(title="Points!", description="{} has **{} point(s)!**".format(userToGet, points), color=0xFF5733)
    return embed

def createUserRetrivalError(userToGet):
    embed=discord.Embed(title="❌ Error", description="{} is not registered in the database.".format(userToGet), color=0xFF5733)
    return embed

def createUserGivePoints(userToGet, numPoints, newPointsTotal):
    embed=discord.Embed(title=":white_check_mark: Success!", description="Successfully gave **{} points** to {}, who now has **{}**.".format(numPoints, userToGet, newPointsTotal[0]), color=0xFF5733)
    return embed

def createUserTakePoints(userToLose, numPoints, newPointsTotal):
    embed=discord.Embed(title="❌ Removed Points!", description="Successfully removed **{} points** to {}, who now has **{}**.".format(numPoints, userToLose, newPointsTotal[0]), color=0xFF5733)
    return embed

def attemptToRemoveMoreThanBalError(userToLose, ammountAttempted, currBalance):
    embed=discord.Embed(title="❌ Error", description="Attempted to remove **{} points**; however, {} has **{} points**.".format(ammountAttempted, userToLose, currBalance[0]), color=0xFF5733)
    return embed

def userCannotAffordRewardError(userToLose, ammountAttempted, currBalance):
    embed=discord.Embed(title="❌ Insufficient Funds", description="Attempted to buy a reward from the store worth **{} points**; however, {} has **{} points**.".format(ammountAttempted, userToLose, currBalance[0]), color=0xFF5733)
    return embed

def noSuchItemOnTheStoreError(userToLose, itemAttempted):
    embed=discord.Embed(title="❌ Reward Not Found", description="Error the {} attempted to buy **{}**; however, this is not present on the store.".format(userToLose, itemAttempted), color=0xFF5733)
    return embed

def createUserAttemptedCommand(userToGet, commandName):
    embed=discord.Embed(title=":bangbang: Alert!", description="User {} attempted to call the {} command.".format(userToGet, commandName), color=0xFF5733)
    return embed

def userAttemptedTwoBuyRoleOwned(userToGet, rewardName):
    embed=discord.Embed(title=":bangbang: Already Own This Role!", description="User {} attempted to purchase the role {}; however, they already have this role.".format(userToGet, rewardName), color=0xFF5733)
    return embed

def createUserCompletedPurchaseAlert(userToGet, balanceAfterwards):
    embed=discord.Embed(title=":dollar: Successful Purchase!", description="{} has successfully made a purchase and now has **{} points**.".format(userToGet, balanceAfterwards[0]), color=0xFF5733)
    return embed

def createStoreEmbed():
    embed=discord.Embed(title=":coin: Store Listing", color=0xFF5733)
    storeItems = getStoreItems()
    for item in storeItems:
        embed.add_field(name=f'**{item[1]}** - *{item[2]} points*', value=f'{item[3]}',inline=False)
    return embed

def isUserAlreadyInRole(user, roleName):
    for role in user.roles:
        if role.name == roleName:
            return True
    return False

bot.run(os.getenv("discordBotToken"))