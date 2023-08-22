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
    await ctx.send("User attempted to get the balance of the user {}.".format(arg))
    await ctx.send("User {} has a balance of {}".format(arg, getUserBalance(arg[2:-1])[0]))

@bot.event
async def on_message(message):
  #check who sent the message
  if message.author == bot.user:
    return
  msg = message.content
  if msg.lstrip() == "$bal":
    if getUserBalance(message.author.id) is None:
        addNewUser(message.author.id)
    
    await message.channel.send("User {} has a balance of {}".format(message.author.mention, getUserBalance(message.author.id)[0]))
  await bot.process_commands(message)

def getUserBalance(id):
    ctx = connectToPointsSystemDatabase()
    cursor = ctx.cursor()
    query = "SELECT balance FROM users WHERE userId = {};".format(id)
    cursor.execute(query)
    finalValue = cursor.fetchone()
    return finalValue
    ctx.close()

def addNewUser(id):
    ctx = connectToPointsSystemDatabase()
    cursor = ctx.cursor()
    query = "INSERT INTO users (userId, balance) VALUES ({}, 0);".format(id)
    finalValue = cursor.execute(query)
    ctx.commit()
    ctx.close()

def connectToPointsSystemDatabase():
    return mysql.connector.connect(user=os.getenv("pointsDatabaseUser"), password=os.getenv("pointsDatabasePassword"),
                              host=os.getenv("pointsDatabaseHost"),
                              database=os.getenv("pointsDatabaseName"))



bot.run(os.getenv("discordBotToken"))
