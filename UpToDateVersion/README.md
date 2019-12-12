# ELG's Discord bot project 
&nbsp;
### Index
1. What is the "Discord bot project" ?
2. Command list / detail  
	2.A - Introduction  
	2.B - Command Index  
	2.C - The -help command  
	2.D - The -role command  
	2.E - The -report command  
	2.F - The -winner command  
3. Processes  
	3.A - Introduction  
	3.B - Processes Index  
	3.C - The role reaction process  
	3.D - The winner submission process  
4. Links  
5. Contacts  
	

### 1. What is the Discord bot project ? 
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;The purpose of this project is to create a bot that will make almost every management task automatized. For instance, the role management is a waste of time for the managers as a single command / reaction to a message from the bot can add / remove a role from the user.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Another good example of the usage of the bot is the automatisation of the ELG point system
(which wasn't in use before the bot was designed because it took too much time to attribute points to every user posting a performance).
Basically, by sending a command to the bot, the member wishing to send a performance in a tournament starts a process which allows him to submit his post to the admins who just have to accept / reject it.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;These were two main points of why this project was started. The main participants of this
project were **3x1** for the code and **EzEvoq** alias Max for additionnal ideas / corrections. (contacts link in the *Contacts* part below)

(This manual is detailling every command / process used by the bot.)  

__*Note from the author :*__
*This project was made in 2 days (08/05/2019 and 09/05/2019) and I didn't write any Python code for a year and a half so I apologize if the code can be a bit messy and not really well-written. This was a test to see what I could do in two days with a new library and something I've never tried before.*
&nbsp;  
&nbsp;  
### 2. Command list / detail

#### &nbsp;&nbsp;&nbsp;&nbsp;A. Introduction 
This section is covering the interaction of every command sent from an user to the bot.
Every command sub-section will contain 4 different parts :
- The command usage
- The command description.
- The user's permissions required to execute the command.
- The context / channels inwhich the command can be used.

Note that some commands may start a process which will not be covered in this section. Go to 
the *Processes* section for further informations (this will be repeated if needed)  
&nbsp;  
#### &nbsp;&nbsp;&nbsp;&nbsp;B. Command index

>-help in section 2.C  
>-role in section 2.D  
>-report in section 2.E  
>-winner command in section 2.F    

&nbsp;
#### &nbsp;&nbsp;&nbsp;&nbsp;C. The -help command 
	
**Usage :** "-help" or "-help command_name" 

(Note : the command_name should be any command without the '-' prefix used by the bot to recognize a command amongst received messages)  

**Description :**
	
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;As the name suggests it, sends a pre-defined message containing basic help on how to use the bot to the user.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Even if the bot is designed to be as user-friendly as possible, a message should be posted by the admins recommending anyone wishing to use this bot to start with the -help command.
Discord communities may be videogames oriented, some members might not be very familiar with computer's basics.  Regarding this fact, this is a must-have command that must be the first one used by anyone to understand how to use this bot.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;There are actually two ways to use this command as described in the *Usage* part : the first one is to simply type "-help" which displays global help on how to use the bot and the -help command. 
The second way is to type "-help *your_command_name*". This will display detailled help about the given command while keeping only the essential. This command does not send a part of this file but some precised help to let anyone use this command anywhere and not flood / make the channel unpleasant to watch.
Any user wishing to get more help on any command / process can visit the git deposit to read this file.

**Permissions required :** None

**Context / channels :** Anywhere the bot has the permission to read / send messages on the server and DM channels with the bot.  
&nbsp;  
#### &nbsp;&nbsp;&nbsp;&nbsp;D. The -role command
**Usage :** "-role" or "-role *role1* *role2* ..."

**Description :**

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Just like the -help command, the -role command has been greatly inspired by the [YAGPDB](https://yagpdb.xyz/) bot which was the bot in use when we started this project. In fact this was one of the only feature we were using from this bot with the autorole (described in the *Processes* section).
As well as the -help command, this one can be used in 2 ways too :
By sending "-role" alone, the bot will answer by displaying the list of the available roles. Thus by typing "-role *role1* *role2* ...", the user gets to grant / remove himself one or more roles (from this list only). 

__*Note from the author :*__
*Actually this command was one of the reasons we decided to change from the YAGPDB to this new bot. Typing "-role _roleName_" several time to get all the roles you want can be really fastidious and we received a lot of remarks about it. Two solutions were feasible : change to another bot or make our own one.*

**Permissions required :** "Read messages" and "Send messages" in the dedicated channel.

**Context / channels :** This command is restricted to a dedicated channel to avoid flood on the server.  
&nbsp;  
#### &nbsp;&nbsp;&nbsp;&nbsp;E. The -report command
**Usage :** "-report" or "-report *report_text*"

**Description :**

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Allows you to send a message which will be saved in a file on the bot's database. This message does not support emojis. The report message can be of any size / type (under the discord's message size restrictions of course). To send a report with more characters than the discord's characters restriction, the user must send several message starting with "-report".
Note that this report is not anonymous as the full discord tag, date, hour and channel are saved in the file.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;This command should mostly be used to send reports about a specific subject that doesn't need to be fixed immediatly by the admins or to submit and idea / request about the bot or server features. More specific demands should always be asked directly to admins in DM.

**Permissions required :** None

**Context / channels** : Anywhere the bot has the permission to read / send messages on the server and DM channels with the bot.  
&nbsp;  
#### &nbsp;&nbsp;&nbsp;&nbsp;F. The -winner command
**Usage :** "-winner"

**Description :** 

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;This command starts the *winner submission process* (described below in the concerned section *Processes*). The result of this command is a message from the bot describing the first part of the process. Reacting to this message will lead to the second part and so on until the end. 
Any member wishing to submit his performance in a tournament to the server should be using this command unless the case is an exception although this command has been designed to fit any special case.
(More details in the *Processes* section below)

__*Note from the author :*__
*This command was mainly Max's idea. The ELG's point system (detailled below) was a great idea but never implemented as I've already wrote in the introduction to this document. This command helps a lot the administrators and keeps a trace of every accepted submission in case of any system rework.*

**Permissions required :** None (Optionnal : "Read messages" / "Send messages" in the dedicated channel.

**Context / channels :** DM channels with the bot (Optionnal : Dedicated channel. This is not recommendend due to the spam of messages)
&nbsp;
#### &nbsp;&nbsp;&nbsp;&nbsp;G. Additionnal commands
**The $dc command :** Creator-only command. Used to disconnect the bot. (Mostly used for maintenance / code modifications). Sends a message to every server connected to the bot about the bot status.  
&nbsp;  
&nbsp;  
### 3. Processes
#### &nbsp;&nbsp;&nbsp;&nbsp;A. Introduction
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; This section is detailling every process used by the bot. "Process" here means everything the bot uses to interact with the user which is not a single command. However, this section does not describe any code. To see the code used for the bot, please refer to the git deposit linked in the *Links* section at the end of this document.

Every process sub-section will contain 3 different parts :
- Prerequisites.
- The channels inwhich the process takes place.
- The process description.


#### &nbsp;&nbsp;&nbsp;&nbsp;B. Processes index
> The role reaction process in section 3.C  
> The winner submission process in section 3.D  

#### &nbsp;&nbsp;&nbsp;&nbsp;C. The role reaction process
**Prerequisites :** (Very recommended) "Add reactions" permission removed from everyone (not admins if necessary) in the dedicated channel described below.

**Channels :** A dedicated channel where only the bot should be posting messages. (it is recommended that the "Send messages" permissions is removed to everyone but admins on this channel)

**Description :** 
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;A message is sent by the bot in the dedicated channel describing the different roles available and the emojis corresponding to these roles. Each emoji is added as a reaction to the message by the bot.
Each time a member adds a reaction (resp. removes one of his reactions) to the message, the corresponding role is added (resp. removed). 

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Even though this process is quite simple, it is way clearer and more user-friendly than the -role command. Because the available roles are the same for both methods, the -role command becomes quite useless as soon as the reaction process is implemented. In fact, some members prefer the -role command that's why both of them are described in this document.

__*Note from the author :*__
*As I've already mentionned in another note, the -role command was one of the main reasons of why we decided to change our bot. Therefore I decided to make an upgraded version of it but a reaction-only method seemed way better in my mind. On a long-term perspective, the -role method should not be used at all as the reaction method is better in every way and requires less actions from the bot.*  

#### &nbsp;&nbsp;&nbsp;&nbsp;D. The winner submission process
**Prerequisites :** A "-winner" command from any server member.

**Channels** : DM channels with the bot. (Optionnal : a dedicated channel. This is not recommended as explained in the -winner command section)
A dedicated channel must be created (admins-only) for the validation part. 

**Description :**
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;In order to make this section clear to anyone, we first need to explain what exactly is the winner submission process. As explained quickly in the "-winner" command section, this command allows the user to start a process which goal is to send a performance in a tournament to the admins. After validation, every player mentionned by the author of the submission will be granted points.
To grant points to anyone, the bot must be informed of the following informations :
- The type of tournament played
- At what place the user ended in the tournament
- How much Riot points / real money the user earned
- The list of all the members that were participating with the user
- One or more screenshots as a proof of the performance (tournament links can be asked from admins before validation if necessary) 

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;This process basically follows the list above in the same order. After the first "-winner" command is sent by the user, a message asking for the type of tournament played is answered in the same channel. Several reactions  are added to this messages by the bot (just like the reaction role process), letting the user chose his type by clicking on one of the reactions.
Right after the type selection, a new message is sent to the user confirming his choice and asking the amount of money / RP earned. At this point the user can chose between the "-rp *amount*" or the "-money *amount*" sub-commands to send the amount earned in the tournament to the bot. If the user earned both RP and money, the highest value between both should be sent.
Following the amount submission, a message asking for the list of players is sent by the bot. This message allows the user to use the "-player *player1* *player2* ..." command until he types "-player end", ending this phase. All players must be in the discord server and all names sent must be full discord tags (Eg : Player#0000). If this rule is not followed or a player not found, every not-found user is listed by the bot.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;After the "-player end" command from the user, the last part of the submission process starts, asking the user any screenshot. Each screenshot must be sent with "-screenshot" as a description to the image. After all the screenshots sent, the user is invited to type the last "-screenshot none" command, which leads to a summary sent by the bot, listing all the user's answers.
If nothing has to be modified, the user can click on a "green check" emoji, added by the bot to the summary message. Reacting to this message will send the submission to a dedicated channel.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;At this point, the admins receive a message in the dedicated channel described above, summarizing the user's submission and allowing them to validate or refuse it by reacting to the message. Because the user is mentionned in this summary, any admin can contact him / her for more details about the performance.
After validation of the submission, the bot automatically grants points to the listed players and informs the user of the validation. In the case of the admins refusing the submission, no points will be granted and the user is informed.

**Important informations about this process :** 
- Every non-finished process is saved by the bot, no time limit is set.
- Anyone can start a process, leave it for later and start a new one. This will not affect the first process which is still considered as "ongoing". 
- No modification can be made during the process, to change a part of the submission, the process must be restarted (by typing the "-winner" command again)
- As this takes a lot of messages to be finished, we do not recommend using this command in an open channel. DM channels with the bot is recommended.
- Sub-commands cannot be used unless the user is at the right step of the process. Same for reactions.
- If used on an open channel, reactions from other users will not affect the current submission. Every message is user-related.

__*Note from the author :*__
*This process was not worth developping on a short-term perspective due to the amount of time needed to code every step. But on a long-term perspective where a lot of members may want to submit performances, this can be a huge gain of time for the admins. Moreover, because every submission is saved, none of them are lost in the amount of messages an admin can receive during events for example.*


### 4. Links
[Git deposit (from 3x1)](https://github.com/3x1s/discord_bot_project)  
[The ELG discord server](https://discord.gg/3FRxFKc)

### 5. Contacts
If you have any question about this project, code or anything related, contact me at 3x1.contact@gmail.com or on discord @3x1#6160.
If you want to try the bot, get the code from the git deposit or go on the ELG discord server linked above.

**Thanks for reading.
3x1**








