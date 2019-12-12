__author__ = "3x1"
__version__ = "1.0"
__email__ = "3x1.contact@gmail.com"
__discordContact__="3x1#6160"

import discord
from datetime import datetime
from discord.utils import get
import fileinput
client = discord.Client()

# Definition of the structures used in the program
roles_dic = {"Lanes" : 5 , "Others" : 6}
roles_list = ["top","jungle","mid","adc","support","lf_team","aram","sub","free_agent","hearthstone","csgo"]
real_roles_list = ["TOP","JUNGLE","MID","ADC","SUPPORT","lf_team","Substitutes","Aram Gods","FA","Hearthstone","CS:GO"]
roles_emoji_name = ["\N{FISTED HAND SIGN}","\N{HIGH VOLTAGE SIGN}","\N{FIRE}","\N{DIRECT HIT}","\N{EYES}","\N{SPEECH BALLOON}","\N{FACE WITHOUT MOUTH}","\U0001F170","\N{SQUARED FREE}","\N{CREDIT CARD}","\N{PISTOL}"]
command_list = ["-role","-report","-help","-winner"]
waiting_validation = {}
queue = {}

# Definition of the channel ID's used in the program
join_leave_channel = 0
role_channel = 0
reaction_role_channel = 0
win_report_channel = 0
win_report_channel_admins = 0

#Definition of the important members' ID
creator_id = 0
# -> 3x1#6160

# Definition of global str used in the program
unrecognized_command_str = "Unrecognized command. Did you mean : "
reaction_role_text_desc = "React to the message to get a role :\n\n---Lanes---\nFist ->top\nZap -> jungle\nFire -> mid\nTarget -> adc\nEyes -> support\n\n---Others---\nSpeech balloon -> lf_team\nFace without mouth -> substitute\nA letter -> Aram Gods\nSquared free-> free_agent\nCredit card -> hearthstone\nPistol -> CSGO"

# Definition of files used in the program
report_file = "reports.txt"
points_file = "points.txt"


#---------------------------- MAIN ----------------------------
#Definition of the function used in the program (Event function separated)

def is_me(m): return m.author==client.user
#Returns a str of the list of the available roles in the list roles_list 
def available_roles(message) : 
	message_list = []
	message_list.append("Here is a list of the available roles : ")
	i = 0
	embed = discord.Embed()
	
	for d_name,d_number in roles_dic.items() :
		field_value=""
		for j in range (i,i+d_number) : 
			field_value += roles_list[j]+'\n'
		embed.add_field(name=d_name+' : ',value=field_value,inline=False)
		i += d_number
		
	message_list.append(embed)
	return message_list

	
# f is a file / message is a discord.message type
# We suppose here that he file is already opened
def write_report(f,message) :
	try : name = message.channel.name 
	except : name = "DMChannel"
	f.write("---------- Report sent by '{}' at '{}' in channel : '{}' ----------\n".format(message.author.name+'#'+str(message.author.discriminator),str(datetime.now()),name))
	f.write("Message content :\n<"+message.content[7:]+">\n\n")
	
	return



#The point_attribution function : 
#Takes a user_id dictionnary containing all the important informations to attribute the points.
#Opens the file, reads the data to get all the existing players that have points and adds points to every player registered in the submission
#PS : the give_points function is not ready yet. Need to implement a system of points attributions depending on the place, type, etc...
def give_points(user_dict) : return 1

def points_attribution(user_dict) :
	f = open(points_file,"r")
	lines = f.readlines()
	splitted_lines=[] 
	modified_lines=[]
	i=0
	points_att=give_points(user_dict)
	
	for l in lines :
		splitted_lines.append(l.split(' : '))
		if splitted_lines[-1][0] in user_dict["players"] :
			splitted_lines[-1][1]=str(points_att+int(splitted_lines[-1][1]))
			lines[i]=' : '.join(splitted_lines[-1])
			user_dict["players"].remove(splitted_lines[-1][0])
			modified_lines.append(i)
		i+=1
	if len(user_dict["players"])!=0 :
		for player in user_dict["players"] :
			lines.append(player+' : '+str(points_att))
			modified_lines.append(i)
			i+=1
	print(lines)
	f.close()
	f=open(points_file,"w")
	for l in lines :
		if l[-1]!='\n' :
			l+='\n'
		f.write(l)
	f.close()
	return

#Finishing the winner submission process
def finishing_winner(msg_id,att=True) :
	i=0
	found=False
	user_id=waiting_validation[msg_id]["user_id"]
	print(queue[user_id],msg_id)
	while found==False :
		if queue[user_id][i]["message_id"]==msg_id:
			found=True
		else :
			i+=1	
	if att :
		points_attribution(queue[user_id][i])
	queue[user_id].pop(i)
	del waiting_validation[msg_id]
				
#Returns a str summarizing the last submission from the user_id 
def user_summary(user_id) :
	user_dict = queue[user_id][-1]
	display_message = "Game mode played : {}\nPlace : {}\n".format(user_dict["type"],user_dict["place"])
	if user_dict["rp"]!=-1 :
		display_message += "Total RP gain : {}\nPlayers :\n".format(user_dict["rp"])
	else :
		display_message += "Total money gain : {}\nPlayers :\n".format(user_dict["money"])
	for i in range(0,len(user_dict["players"])-1) :
		display_message+=user_dict["players"][i]+' , '
	if len(user_dict["players"])!=0 : display_message+=user_dict["players"][-1]+'\n'
	else : display_message+= "None"
	return display_message
	 
#Resets the user dict
def reset_dict(user_id) : 
	queue[user_id]["pos"]=0
	queue[user_id]["place"]=0
	queue[user_id]["rp"]=-1
	queue[user_id]["money"]=-1
	queue[user_id]["players"]=[]
	queue[user_id]["type"]=""
	queue[user_id]["screenshots"]=[]
	queue[user_id]["message_id"]=0
	return
# Defintion of the event functions

#Initializing fonction. The role_reaction message is cleared and remade
@client.event
async def on_ready():
	
	print('We have logged in as {0.user}'.format(client))
	#print(client.guilds[0].members)
	print(client.guilds)
	channel = get(client.guilds[0].channels,id=reaction_role_channel)
	#Initializing the role_reaction_channel
	await channel.purge(check=is_me)
	await channel.send(reaction_role_text_desc)
	global role_msg_id 
	role_msg_id = channel.last_message_id
	msg = await channel.fetch_message(id=role_msg_id)
	for i in range(0,len(roles_emoji_name)) : 
		emoji = roles_emoji_name[i]
		await msg.add_reaction(emoji)

#Event on member join. For now only displays a message and adds a "member" role
@client.event
async def on_member_join(member):
	desc = "Hello there {} !\nWelcome to ELG Community  :tada: :hugging: !\n".format(member.name)
	desc += " You have made the first step into our community and your journey is just about to begin !\n"
	desc += "Feel free to post in #looking-for-team tofind/create a team :smile: !\n"
	desc += "Fight your way through the placement of the teams through private tournaments and scrims to rank up !\nGLHF :fire:"
	embed = discord.Embed(title = "Welcome !",description = desc)
	embed.set_thumbnail(url=member.guild.icon_url)
	embed.set_footer(text="Made by @3x1#6160",icon_url="https://cdn.discordapp.com/avatars/223098551750754304/cd4c99bb8d40fdfb714395d01a9b6467.png")
	on_join_channel = get(member.guild.channels,id=join_leave_channel)
	await on_join_channel.send(embed=embed)
	await member.add_roles(get(member.guild.roles,name="member")) 


#Event on message from any user to any channel the bot has the read messages permission
@client.event
async def on_message(message):
	aut = message.author
	msg = message.content.split()
	dm_chan=False
	try :
		role_command_channel = get(aut.guild.channels,id=role_channel)
	except : dm_chan=True
	
	if aut == client.user :
		return
	
	#-------------- The "$dc" command --------------
	elif (message.content.startswith('$dc') and aut.id==creator_id):
		await message.channel.send('Disconnecting...')
		try :
			await get(aut.guild.channels,id=reaction_role_channel).send("Bot is currently offline")
		except : pass
		await client.close()
	#-------------- End of the "$dc" command --------------
	
	#-------------- The "-role" command : -------------- 
	elif (message.content.startswith('-role') and not dm_chan and message.channel==role_command_channel ) :
		errors = []
				
		#If msg == "-role ", send the available roles 
		if (len(msg)==1 and msg[0]=='-role'): 
			result = available_roles(message)
			await message.channel.send(result[0])
			await message.channel.send(embed=result[1])
			
		elif msg[0]=='-role':
			for role in msg[1:] :
				if not role in roles_list :
					errors.append(role)
			
			#Checks which roles haven't been identified and displays them
			if errors != [] : 
				error_chain = "Error. Role(s) not identified : "
				for er in errors :
					error_chain += "<{}>".format(er)
				result = available_roles(message)
				await message.channel.send(error_chain)
				await message.channel.send(result[0])
				await message.channel.send(embed=result[1])
				
			else : 
				#Checking the roles -> adding or removing in consequence
				added = removed = False
				for role in msg[1:] :
					role_up = get(client.guilds[0].roles,name=real_roles_list[roles_list.index(role)]) 
					if role_up in aut.roles :
						await aut.remove_roles(role_up)
						removed = True
					else : 
						await aut.add_roles(role_up)
						added = True
				
				#Displaying the correct message after looking at added and removed
				msg_sent =""
				if removed == True and added == True :
					msg_sent = 'Roles added / removed !'
				elif removed == True : 
					msg_sent = 'Roles removed !'
				elif added == True : 
					msg_sent = 'Roles added !'
				await message.channel.send(msg_sent)
		
		else : 
			await message.channel.send(unrecognized_command_str + "-role ?")
	#-------------- End of the "-role" command : -------------- 
	
	#-------------- The "-report" command --------------
	elif (message.content.startswith('-report')) :
		msg = message.content.split()
		if (msg[0] != "-report") :
			await message.channel.send(unrecognized_command_str + "-report ?")
		elif (len(msg)==1) : 
			await message.channel.send("Usage of the '-report' command : -report <your report here>") 
		else :
			f=open("reports.txt",'a')
			write_report(f,message)
			f.close()
			await message.channel.send("Your report has been sent. Thanks !")
	#-------------- End of the "-report" command : -------------- 

	#-------------- The "-help" command --------------
	elif (message.content.startswith('-help')) :
		if msg[0]!="-help" :
			await message.channel.send(unrecognized_command_str + "-help ?")
		# If the message is just '-help'
		elif len(msg)==1 : 
			chain=""
			for i in range(0,len(command_list)-1) :
				chain+=command_list[i]+ ' | '
			chain+=command_list[len(command_list)-1]
			await message.channel.send("Here is a list of the available commands : "+chain+"\nNote that only the -help, the -winner and the -report command are available in DMs to the bot.\nFor further informations about a command, please type '-help <the command name>'")
		
		# If the message is exactly '-help <command name>'
		elif len(msg)==2 :
			switcher = {"role" : "Gives you the roles if the bot has the right to give them. If you already have one of the roles, the bot takes it back instead.\nType -role to see the available roles.\nHow to use it : -role <role1> <role2> ...\n\nPS : To avoid spam, this command can only be used in the dedicated channel : {}.".format(get(client.guilds[0].channels,id=role_channel).mention),
						"report" : "Sends a report to the admins / dev. This can be used if you have a suggestion or anything that you think we should know.\nAny suggestions to improve the bot are welcome !\nHow to use it : -report <your report here>",
						"help" : "Displays the available commands or the help for one particular command.\nHow to use it : -help or -help <your command name>.",
						"winner" : "Starts the winner request process. Use it if you you placed well in a tournament to get ELG points.\n	<IMPORTANT !>\nThis command is only available in DM with the bot or in the {} channel. \nWe recommand using the DMs for now as the flood might not make the use of this command to be very pleasant.\nHow to use it : -winner".format(get(client.guilds[0].channels,id=win_report_channel).mention)}
			desc=switcher.get(msg[1],"Invalid command name. Please type -help to display all the commands")
			await message.channel.send(desc)
		else : 				
			await message.channel.send("Incorrect usage.\nUsage of the '-help' command : -help") 
	#-------------- End of the "-help" command : -------------- 

	#-------------- The "-winner" command --------------
	elif (message.content.startswith('-winner') and (dm_chan or message.channel.id==win_report_channel)) :
		if msg[0]!="-winner" :
			await message.channel.send(unrecognized_command_str + "-winner ?")
		elif len(msg)!=1 :
			await message.channel.send("Incorrect usage.\nUsage of the '-winner' command : -winner") 
		else :
			await message.channel.send("Welcome to the winner post process. Please indicate which type of tournament you won by reacting to this message as following :\n 5v5 -> 5 / Aram -> A / 3v3 -> 3 / 2v2 -> 2 / 1v1 -> 1")
			async for for_message in message.channel.history(limit=1) :
				if for_message.author==client.user:
					own_message=for_message
			
			await own_message.add_reaction("\N{DIGIT FIVE}\N{COMBINING ENCLOSING KEYCAP}")
			await own_message.add_reaction("\N{DIGIT THREE}\N{COMBINING ENCLOSING KEYCAP}")
			await own_message.add_reaction("\N{DIGIT TWO}\N{COMBINING ENCLOSING KEYCAP}")
			await own_message.add_reaction("\N{DIGIT ONE}\N{COMBINING ENCLOSING KEYCAP}")
			await own_message.add_reaction("\U0001F170")
			try : 
				queue[aut.id].append({"pos":0,"message_id":own_message.id,"players":[],"screenshots":[]})
			except :	
				queue[aut.id]=[{"pos":0,"message_id":own_message.id,"players":[],"screenshots":[]}]
	
	#Gets the place of the user for the winner post process
	elif (message.content.startswith('-place') and aut.id in list(queue) and queue[aut.id][-1]["pos"]==1 ):
		if msg[0]!="-place" :
			await message.channel.send(unrecognized_command_str + "-place ?")
		elif (int(msg[1])>32 or int(msg[1])<1):
			await message.channel.send("Please type a number between 1 and 32. If you ended up at more than 32, type 32")
		elif (1<=int(msg[1])<=32):
			queue[aut.id][-1]["place"]=int(msg[1])
			await message.channel.send("Answer registered ({}).".format(queue[aut.id][-1]["place"]))
			await message.channel.send("How much RP / money did you get (per participant) ? Please type '-money <amount>' for real money (in euros) or '-rp <amount>' for RPs")
			queue[aut.id][-1]["pos"]=2	
			
	#Gets the amount of rp/money of the user for the winner post process
	elif (message.content.startswith('-money') and aut.id in list(queue) and queue[aut.id][-1]["pos"]==2):
		if msg[0]!="-money" :
			await message.channel.send(unrecognized_command_str + "-money ?")
		elif (int(msg[1])<0) : 
			await message.channel.send("Please type a number above 0. If you didn't get any money reward just type -money 0")
		elif (int(msg[1])>=0) :
			queue[aut.id][-1]["money"]=int(msg[1])
			queue[aut.id][-1]["rp"]=-1
			await message.channel.send("Answer registered ({}).".format(queue[aut.id][-1]["money"]))
			await message.channel.send("Please type every player that played with you with the '-player <player1#0000> <player2#0000> ...' format (you can either do it one by one if you want).\n##### IMPORTANT ! #####\nIn order to automatically add your points in the database, we need the complete discord type (eg : 3x1#6160).\nIf you don't respect this format, no points will be allowed to the user.\n\nPS : the bot will tell you if we don't find one of the player") 
			queue[aut.id][-1]["pos"]=3
			
	elif (message.content.startswith('-rp') and aut.id in list(queue) and queue[aut.id][-1]["pos"]==2):
		if msg[0]!="-rp" :
			await message.channel.send(unrecognized_command_str + "-rp ?")
		elif (int(msg[1])<0) : 
			await message.channel.send("Please type a number above 0. If you didn't get any rp reward just type -rp 0")
		elif (int(msg[1])>=0) :
			queue[aut.id][-1]["rp"]=int(msg[1])
			queue[aut.id][-1]["money"]=-1
			await message.channel.send("Answer registered ({}).".format(queue[aut.id][-1]["rp"]))
			await message.channel.send("Please type every player that played with you with the '-player <player1#0000> <player2#0000> ...' format (you can either do it one by one if you want).\n##### IMPORTANT ! #####\nIn order to automatically add your points in the database, we need the complete discord type (eg : 3x1#6160).\nIf you don't respect this format, no points will be allowed to the user.\n\nPS : the bot will tell you if we don't find one of the player") 
			queue[aut.id][-1]["pos"]=3
			
	#Gets the players that played for the tournament
	elif (message.content.startswith('-player') and aut.id in list(queue) and queue[aut.id][-1]["pos"]==3):
		if msg[0]!="-player" :
			await message.channel.send(unrecognized_command_str + "-player ?")
		
		elif msg[1]=="end" :
			await message.channel.send("Players registration phase finished. If you have any screenshot please type '-screenshot' and attach your screenshot(s) to it. If you don't please type '-screenshot none'.")
			queue[aut.id][-1]["pos"]=4
			
		else :
			errors=""
			for player in msg[1:]:
				player_split=player.split('#')
				player_name=player_split[0]
				player_disc=player_split[1]
				print(player_name,player_disc,get(client.guilds[0].members,name=player_name,discriminator=player_disc))
				if get(client.guilds[0].members,name=player_name,discriminator=player_disc)!=None :
					print("went here")
					try : queue[aut.id][-1]["players"].append(player)
					except : queue[aut.id][-1]["players"]=[player]	
				else :
					errors+=player+'\n'
			if errors!="" :
				await message.channel.send("We couldn't find these players :\n"+errors+"\nPlease ensure you typed their discord tag right. If you finished entering players, type -player end. Either type -player <player1#0000> <player2#0000> ...")
			else :
				await message.channel.send("Players registered. If you finished entering players, type -player end. Either type -player <player1#0000> <player2#0000> ...")
	
	#Gets the screenshots url if attached
	elif (message.content.startswith('-screenshot') and aut.id in list(queue) and queue[aut.id][-1]["pos"]==4):
		if msg[0]!="-screenshot" :
			await message.channel.send(unrecognized_command_str + "-screenshot ?")
			
		elif (len(msg)>1 and msg[1]=="none") :
			await message.channel.send("Answer registered.\nThe winner post process is now finished. Here is a summary of your post. Please check everything is correct before reacting with the green check to validate your post.\nIf something is missing/not correct, please start from the beginning by typing the -winner command." )
			await message.channel.send(user_summary(aut.id))
			async for for_message in message.channel.history(limit=1) :
				if for_message.author==client.user:
					own_message=for_message
			await own_message.add_reaction("\N{WHITE HEAVY CHECK MARK}")
			queue[aut.id][-1]["message_id"]=own_message.id
			queue[aut.id][-1]["pos"]=5
			
		else :
			att_list=message.attachments
			if len(att_list)==0 :
				await message.channel.send("No attachments found. Please verify you sent the message with the screenshot attached.")
			else :
				for att in att_list:
					try : queue[aut.id][-1]["screenshots"].append(att.url)
					except : queue[aut.id][-1]["screenshots"]=[att.url]
				await message.channel.send("Screenshots registered. If you want to add more screenshots, make the same manipulation. If you don't have any more screenshots, please type -screenshot none")
				
# Definition of the role "reaction" fonction : 
# on_reaction_add() -> checks if a reaction is added to the concerned message and gives a role in consequence
# on_reaction_remove() -> checks if a reaction is removed to the concerned message and removes a role in consequence

@client.event
async def on_reaction_add(reaction,user):
	msg = reaction.message
	if user==client.user : return
	
	if (msg.id == role_msg_id and user!=client.user) :
		i=roles_emoji_name.index(reaction.emoji)
		role= get(user.guild.roles,name=real_roles_list[i]) 
		if not role in user.roles :
			await user.add_roles(role)
			
	#Second part of the winner function
	#print(queue)
	if (user.id in list(queue) and queue[user.id][-1]["pos"]==0 and msg.id==queue[user.id][-1]["message_id"]):
		user_dic=queue[user.id][-1]
		if (user_dic["pos"]==0):
			switcher={"\N{DIGIT FIVE}\N{COMBINING ENCLOSING KEYCAP}":"5v5",
						"\N{DIGIT THREE}\N{COMBINING ENCLOSING KEYCAP}":"3v3",
						"\N{DIGIT TWO}\N{COMBINING ENCLOSING KEYCAP}":"2v2",
						"\N{DIGIT ONE}\N{COMBINING ENCLOSING KEYCAP}":"1v1",
						"\U0001F170":"ARAM"}
			user_dic["type"]=switcher.get(reaction.emoji,"None")
			if user_dic["type"]!=None :
				await msg.channel.send("You chose the {} format.".format(user_dic["type"]))
				await msg.channel.send("At which place did you end up (between 1 and 32) ? Please type -place <your place>")
				user_dic["pos"]=1
				queue[user.id][-1]=user_dic
			
	if (user.id in list(queue) and queue[user.id][-1]["pos"]==5 and msg.id==queue[user.id][-1]["message_id"]):
		if reaction.emoji=="\N{WHITE HEAVY CHECK MARK}":
			channel_report_win = get(client.guilds[0].channels,id=win_report_channel_admins)
			admin_report_message = "~\n\n----- New submission (n°{}) from : {} at {} -----\n".format(len(waiting_validation),user.name+'#'+user.discriminator,str(datetime.now())) + user_summary(user.id)
			if len(queue[user.id][-1]["screenshots"])>0 :
				admin_report_message+="Screenshots URL :\n"
				for url in queue[user.id][-1]["screenshots"] :
					admin_report_message+="~ "+url +'\n'
			await channel_report_win.send(admin_report_message)
			async for for_message in channel_report_win.history(limit=1) :
				if for_message.author==client.user:
					own_message=for_message
			await own_message.add_reaction("\N{WHITE HEAVY CHECK MARK}")
			await own_message.add_reaction("\N{NEGATIVE SQUARED CROSS MARK}") 
			
			waiting_validation[own_message.id]={"name":user.name+'#'+user.discriminator,"number":len(waiting_validation),"user_id":user.id}
			await msg.channel.send("Your submission has been sent (ID : {} -> you will receive a message with this ID after the admins checked your submission).\n The admins will check it and you will be contacted if it is validated or not.\nIf you have any though about this process, feel free to use the '-report' command :)".format(own_message.id))
			queue[user.id][-1]["pos"]=6
			queue[user.id][-1]["message_id"]=own_message.id
		
	#Process for the winner validation by the admins	
	if (msg.id in list(waiting_validation)) :
		if reaction.emoji == "\N{WHITE HEAVY CHECK MARK}" :
			await msg.channel.send("Submission n°{} from {} validated. Points will be allowed to the players right after this message.\nPS : No post will be made by the bot in the winners memorial.".format(waiting_validation[msg.id]["number"],waiting_validation[msg.id]["name"]))
			#Gives the point following the dictionnary in argument
			user = get(client.guilds[0].members,id=waiting_validation[msg.id]["user_id"])
			try :
				await user.dm_channel.send("You're submission corresponding to the ID : {} has been accepted !".format(msg.id))
			except : 
				await user.create_dm()
				await user.dm_channel.send("You're submission corresponding to the ID : {} has been accepted !".format(msg.id))
			finishing_winner(msg.id)
			
			
		elif reaction.emoji =="\N{NEGATIVE SQUARED CROSS MARK}" :
			await msg.channel.send("Submission n°{} from {} refused.".format(waiting_validation[msg.id]["number"],waiting_validation[msg.id]["name"]))
			try :
				await user.dm_channel.send("You're submission corresponding to the ID : {} has been refused. Please contact and admin to know what was wrong with your submission.".format(msg.id))
			except :
				await user.create_dm()
				await user.dm_channel.send("You're submission corresponding to the ID : {} has been refused. Please contact and admin to know what was wrong with your submission.".format(msg.id))
			finishing_winner(msg.id,False)
						
@client.event
async def on_reaction_remove(reaction,user):
	msg = reaction.message
	if (msg.id == role_msg_id and user!=client.user) :
		i=roles_emoji_name.index(reaction.emoji)
		role= get(user.guild.roles,name=real_roles_list[i]) 
		if role in user.roles :
			await user.remove_roles(role)
client.run("client token is private :)")
