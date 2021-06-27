import os
import discord
import mysql.connector
from discord import Intents
from mysql.connector import errorcode
from config import config
from config import TOKEN

intents=Intents.all()

try:
    cnx = mysql.connector.connect(**config)
    print('Logged in')
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)
else:
    cnx.close()
    print('Logged out')

client = discord.Client()

x1 = 0
x2 = 0
z1 = 0
z2 = 0
divisor = 15
position = 0.0
inputText = ''
coordList = []
inputList = []

def calculateStacks(totalNumber):
    stacks = int(totalNumber/64)
    remainder = totalNumber%64
    extra = int(remainder * stacks)
    message = totalNumber + " blocks is equal to " + stacks + " stacks with " + extra + " extra."
    
    return message
    
    
    
def updateChunks(userName, chunkName, x1, z1, x2, z2, userID):
    valid = True
    ##Query to get user id from user table
    GETUSERID = ("SELECT userid, username FROM users WHERE username = '"+userName+"'")

    ##Statement to create a user in the database if it doesn't already exist
    NEWUSER = ("INSERT INTO users (userid, username) VALUES ("+str(userID)+", '"+userName+"')")

    ##Query to check if chunk already exists in the database
    COUNTCHUNKDATA = ("SELECT count(userid) FROM chunkdata WHERE chunkname = '"+chunkName+"' AND userid = "+ str(userID))

    ##Statement to insert new chunk data
    INSERTCHUNK = ("INSERT INTO chunkdata (id, chunkname, x1, x2, z1, z2, userid) VALUES (default, '"+chunkName+"', "+str(x1) +", "+str(z1)+", "+str(x2)+", "+str(z2)+", "+str(userID)+")")

    try:
        cnx = mysql.connector.connect(**config)
        print('Logged in to store chunk')
        print("username: " + userName + "\nchunkName: " + chunkName + "\ncoords: " +str(x1) +", "+str(z1)+", "+str(x2)+", "+str(z2)+"\nuserID: " +str(userID))
        cursor = cnx.cursor()

        try:
            print('Attempting to get user id')
            query = (GETUSERID)
            result = cursor.fetchone()
            userid = result[0]
            print(userid)
            username = cursor.fetchone()
            username = result[1]
            print(username)

            if (str(userid) == str(userID)):
                if (username != userName.ignorecase()):
                    print('line 66')
                    cursor.fetchall()##burner
                    cursor.execute("UPDATE users SET username = '%s' WHERE userid = '%s'" %(userName, str(userID)))

            cursor.fetchall()##burner
            print('line 71 no user id match')
            print('Trying to create new user')
            query = (NEWUSER)
            cursor.fetchall()#burner
            cursor.execute(query)
            print('New user added: ' + userName)

        except:
            print('could not make new user')

            ##Count to see if the data already exists##
            query = (COUNTCHUNKDATA)
            cursor.execute(query)
            result = cursor.fetchone()
            count = result[0]
            print('Finished count: '+str(count))
            
            if (count == 0):
                print('Entered if statement to insert chunk line 89')
                cursor.fetchall()##You must fetch all rows for the current query before executing new statements using the same connection.
                query = (INSERTCHUNK)
                cursor.execute(query)
                print('Ran query')
            else:
                print('Entered else statement line 95')
                valid = False
                return valid

    except mysql.connector.Error as err:
        valid = False
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
            cnx.close()
            print('Logged out')

    cnx.commit()
    print('Chunk stored')
    cursor.close()
    cnx.close()
    print('Logged out')
    return valid

def removeStoredChunk(chunkName, userID):
    
    ##Statement to remove a named chunk's data
    REMOVECHUNK = ("DELETE FROM chunkdata WHERE userid = '"+str(userID)+"' AND chunkname = '"+chunkName+"'")
    ##Count to see if the data already exists## 
    COUNTCHUNKDATA = ("SELECT count(userid) FROM chunkdata WHERE chunkname = '"+chunkName+"' AND userid = "+ str(userID))
    valid = True
    
    try:
        cnx = mysql.connector.connect(**config)
        print("Logged in to remove chunk")
        cursor = cnx.cursor()
         
        query = (COUNTCHUNKDATA)
        cursor.execute(query)
        result = cursor.fetchone()
        count = result[0]
        
        if (count == 1):
            cursor.fetchall()##You must fetch all rows for the current query before executing new statements using the same connection.
            query = (REMOVECHUNK)
            cursor.execute(query)
        else:
            valid = False
            return valid
    except mysql.connector.Error as err:
        valid = False
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
            cnx.close()
            print('Logged out')
            
    cnx.commit()
    cursor.close()
    cnx.close()
    print('Logged out')
    return valid

def pullCoords(userID, chunkName):
    
    GETCHUNKDATA = ("SELECT chunkname, x1, z1, x2, z2 FROM chunkdata WHERE chunkname = '"+chunkName+"' AND userid = "+ str(userID))
    COUNTCHUNKDATA = ("SELECT count(userid) FROM chunkdata WHERE chunkname = '"+chunkName+"' AND userid = "+ str(userID))
    
    try:
        cnx = mysql.connector.connect(**config)
        print("Logged in to get chunk")
        cursor = cnx.cursor()

        query = (COUNTCHUNKDATA)
        cursor.execute(query)
        result = cursor.fetchone()
        count = result[0]
        
        if (count >= 1):
            cursor.fetchall()##You must fetch all rows for the current query before executing new statements using the same connection.
            query = (GETCHUNKDATA)
            cursor.execute(query)
            result = cursor.fetchone()
            valid = result[0]
            valid += "\n"+result[1]
            valid += ", "+result[3]
            valid += " to "+result[2]
            valid += ", "+result[4]
        else:
            valid = False
            return valid
    
    except mysql.connector.Error as err:
        valid = False
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
            cnx.close()
            print('Logged out')
            
    cursor.close()
    cnx.close()
    print('Logged out')
    return valid

def listChunks(userID):
    LISTCHUNKS = ("SELECT chunkname FROM chunkdata WHERE userid = "+ str(userID))
    COUNTTOTAL = ("SELECT count(userid) FROM chunkdata WHERE userid = "+ str(userID))

    try:
        cnx = mysql.connector.connect(**config)
        print("Logged in to list chunks")
        cursor = cnx.cursor()

        query = (COUNTTOTAL)
        cursor.execute(query)
        result = cursor.fetchone()
        count = result[0]
        
        if (count >= 1):
            cursor.fetchall()##You must fetch all rows for the current query before executing new statements using the same connection.
            query = (LISTCHUNKS)
            cursor.execute(query)
            valid = cursor.fetchall()            
            
        else:
            valid = False
            return valid
    
    except mysql.connector.Error as err:
        valid = False
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
            cnx.close()
            print('Logged out')
            
    cursor.close()
    cnx.close()
    print('Logged out')
    return valid

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    user = message.author
    userName = user.name
    userID = user.id
    chunkName = ''

    inputText = message.content
    inputText = inputText.lower()
    inputText.rstrip()

    if inputText.startswith('/findchunk'):
        if inputText.endswith('help') or inputText == '/findchunk':
            await message.channel.send('Enter your current X and Z coordinates separated by a comma.\nEx. /findChunk 32, 16')
            return

        inputText = inputText.replace('/findchunk','')
        coordList = inputText.split(',')

        if len(coordList) > 2:
            await message.channel.send('You have entered too many coordinates.\nPlease only enter your current x and z coordinates separated by a comma. \n Ex. /findChunk 32, 16')
            return

        for element in coordList:
            element = element.strip()

            if not(element.isdigit):
                await message.channel.send('You have entered an incorrect format.\nPlease only enter your current x and z coordinates separated by a comma. \n Ex. /findChunk 32, 16')
                return


        x1 = int(coordList[0])
        z1 = int(coordList[1])

        if x1 < 0:
            divisor = 16
            position = x1 % divisor

            x1 -= position
            x2 = x1 + 15

        if z1 < 0:
            divisor = 16
            position = z1 % divisor

            z1 -= position
            z2 = z1 + 15

        if x1 >= 0:
            divisor = 15
            position = x1 % divisor

            x1 -= position
            x2 = x1 + 15

        if z1 >= 0:
            divisor = 15
            position = z1 % divisor

            z1 -= position
            z2 = z1 + 15

        await message.channel.send('You are in a chunk from ' + str(x1) + ', ' + str(z1) + ' to ' + str(x2) + ', ' + str(z2) )

    if inputText.startswith('/storechunk'):
        if inputText.endswith('help') or inputText == '/storechunk':
            await message.channel.send('Enter a name for the chunk you want to save and the coordinates separated by commas.\nEx. /storeChunk chunkname, -336, 645, -321, 660')
            return

        inputText = inputText.replace('/storechunk ','')
        inputList = inputText.split(',')
        chunkName = inputList[0]
        x1 = int(inputList[1])
        z1 = int(inputList[2])
        x2 = int(inputList[3])
        z2 = int(inputList[4])

        valid = updateChunks(userName, chunkName, x1, z1, x2, z2, userID)

        if (valid == True):
            await message.channel.send('Chunk Stored')
        else:
            await message.channel.send('Error: Make sure the name "' +chunkName+ '" does not already exist.')

    if inputText.startswith('/delchunk'):
        if inputText.endswith('help') or inputText == '/delchunk':
            await message.channel.send('Enter the name of the stored chunk you would like to delete.\nEx. /delChunk chunkname')
            return
        inputText = inputText.replace('/delchunk ', '')
        inputList = inputText.split(' ')

        if len(inputList) > 1:
            await message.channel.send('Error: Only enter the name of the stored chunk you would like to delete.\nEx. /delChunk chunkname')
            return
        chunkName = inputText.strip()
        valid = removeStoredChunk(chunkName, userID)
        if valid:
            await message.channel.send('Stored Chunk "' + chunkName + '" removed.')
            return
        else:
            await message.channel.send('Error: Make sure the chunk named "' +chunkName+ '" exists.\nUse \listChunks to see all of your stored chunks.')

    if inputText.startswith('/listchunks'):
        if inputText.endswith('help'):
            await message.channel.send('Run this command to view a list of your stored chunks.\nEx. /listChunks')
            return

        matches = listChunks(userID)

        if matches == False:
            await message.channel.send('You have no stored chunks.')
            return
        else:   
            await message.channel.send(matches)

    if inputText.startswith('/showchunk'):
        if inputText.endswith('help') or inputText == '/showchunk':
            await message.channel.send('Run this command with a chunk name to view stored coordinates. \nEx. /showChunk chunkname')
            return
        
        inputText = inputText.replace('/showchunk ', '')
        inputList = inputText.split(' ')
        if len(inputList) > 1:
            await message.channel.send('Error: Too many arguments.\nOnly enter the command and the chunk name.\nEx. /showChunk chunkname')
            return
        chunkName = inputText.strip()
        chunk = pullCoords(userID, chunkName)
        if chunk == False:
            await message.channel.send('Error: Chunk name does not exist.')
            return
        
        await message.channel.send(chunk)

    if inputText.startswith('/command') or inputText.startswith('/help'):
        await message.channel.send(
            'List of commands:\n'+
            '=====================\n'+
            '/findChunk x, z\n'+
            '\tInsert your x and z coordinates to get the coordinates for the chunk you\'re standing in.\n\n'+
            '/storeChunk chunkname x1, z1, x2, z2\n'+
            '\tEnter a name for the chunk and the x and z for the chunk corners.\n\n'+
            '/delChunk chunkname\n'+
            '\tEnter the name of a stored chunk you would like to delete.\n\n'+
            '/listChunks\n'+
            '\tUse this command alone to view your saved chunks\n\n'+
            '/showChunk chunkname\n'+
            '\tEnter the name of a stored chunk to view it\'s coordinates.')
        
    if inputText.startswith('/stack'):
        if inputText.endswith('help') or inputText == '/stack':
            await message.channel.send('Run this command with a total number of blocks to calculate the stacks. \nEx. /showChunk chunkname')
            return
        
    

client.run(TOKEN)
