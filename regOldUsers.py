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

@bot.event
async def on_ready():
    for guild in bot.guilds:
        if (str(guild.id) == "1096290306430869575"):
            for member in guild.members:
                if getUserBalance(member.id) == -1:
                    addNewUser(member.id)

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


def getUserBalance(id):
    ctx = connectToPointsSystemDatabase()
    cursor = ctx.cursor()
    query = "SELECT balance FROM users WHERE userId = {};".format(id)
    cursor.execute(query)
    finalValue = cursor.fetchone()
    if not finalValue:
        return -1
    return finalValue
    ctx.close()

bot.run(os.getenv("discordBotToken"))