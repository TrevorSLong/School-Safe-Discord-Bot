# School Safe Discord Bot
This repository contains the code to run School Safe Bot. School Safe Bot is a Discord bot designed to help teachers and professors keep a Discord server school appropriate and safe for all the students. This page explains what School Safe Bot does and how to use each feature. You are more then welcome to download School Safe Bots code to modify and deploy to make it better for you, but please do not profit off of my code. To add School Safe Bot to your Discord server click [Here](). If you like School Safe Bot please consider contributing to the code or donating so that we can make it better! [Donate](https://www.paypal.com/donate?hosted_button_id=RBYUJ5M6QSB52).

## Event responding
These are events that happen in the server that School Safe Bot will automatically respond to with no user input. Currently, these features cannot be disabled, but that is a feature that is in the pipeline.

**Remove swear words** 
* School Safe Bot will automatically detect swear words sent in chat and instantly delete them.
* School Safe Bot will then direct message the user letting them know what happened
* School Safe Bot will also send a notification to the Admin update channel containing the User that sent the message and the message contents

**Remove excessive caps messages** 
* Messages that contain more then 50% capital letters will be automatically removed from chat.
* The user who sent the message will recieve a direct message letting them know what happened
* The admin updates channel will display who sent the message and what it contained.

**Updates on role changes**
* School Safe Bot will detect when a user has gained or lost a role and send a message in the admin updates channel.

**Welcome messages**
* School Safe Bot will welcome students into the server with friendly messages in the updates channel.
* A message will also be sent in the admin channel whenever someone joins the server.

**Leave messages**
* School Safe Bot will detect when someone leaves the server and will send a goodbye message
* A message will also be sent in the admin channel logging that a student has left the server.

**Join server direct message**
* When someone joins the server School Safe Bot will send them a direct message outlining basic rules and directing the student to check a rules channel to find a complete list.

**Auto-assign admin and updates channels**
* When School Safe Bot joins your server it will automatically assign the admin and updates channel to the top text channel in your server.

**Introduction**
* When School Safe Bot joins a server it will introduce itself in the top-most text channel in the server.

## Commands
A list of commands can be brought up by typing / in a text channel. Commands are sent by an authorized user to perform actions in the server.

**Ping**
* `/ping`
* Verify the bot and your internet are working by typing
* The bot will respond with the latency if everything is working

**Donate**
* `/donate`
* The bot will bring up information on how to contribute to the development of the bot

**Server Count**
* `/servercount`
* The bot will display how many servers it is active in

**Announcements**
* `/announce <message> <channel>`
* `<message>` is the message for the announcement you would like to send
* `<channel>` is the channel the announcement will be sent in 
* User must have permisson `Manage Server` to execute.
* You can use this command to have School Safe Bot send an announcement on your behalf into any channel.

**Kick**
* `/kick <member> <reason>`
* `<member>` is the member of the server you want to kick
* `<reason>` is the reason they are being kicked **they will be sent this reason**
* User must have permisson `Kick` to execute.
* This command can be used to kick a user in a way that they know why they got kicked.
* Once executed, the user will recieve a direct message saying why they got kicked.
* The admin channel will also get an update as to who kicked who and why.

**Ban**
* `/ban <member> <reason>`
* `<member>` is the member of the server you want to ban
* `<reason>` is the reason they are being banned **they will be sent this reason**
* User must have permisson `Ban` to execute.
* This command can be used to ban a user in a way that they know why they got banned.
* Once executed, the user will recieve a direct message saying why they got banned.
* The admin channel will also get an update as to who banned who and why.

**Temporary Ban**
* `/tempban <member> <reason> <duration>`
* `<member>` is the member of the server you want to temp ban
* `<reason>` is the reason they are being temp banned **they will be sent this reason**
* `<duration>` is the number of days for them to be banned.
* User must have permisson `Ban` to execute.
* This command can be used to temp ban a user in a way that they know why they got banned.
* Once executed, the user will recieve a direct message saying why they got temp banned and for how long.
* The admin channel will also get an update as to who banned who, why, and for how long.
* Once the ban expires the user will be automatically unbanned.

**Un-Ban**
* `/unban <Member#1234>`
* `<Member#1234>` is the member you want to unban, it must be typed out as Member#1234
* User must have permisson `Ban` to execute.
* This command can be used to unban a member without scrolling through the list in server settings.

**Change Update Channel**
* `/updatechannel <#Update-Channel>`
* `<#Update-Channel>` is the channel the updates will be sent in, this should autofill
* User must have permisson `Manage Server` to execute.
* This command changes where updates are sent (Welcome messages, leave messages, etc.)

**Change Admin Channel**
* `/adminchannel <#Admin-Channel>`
* `<#Admin-Channel>` is the channel the admin updates will be sent in, this should autofill
* User must have permisson `Manage Server` to execute.
* This command changes where admin updates are sent (Kicking, banning, role changes, swear word removals, etc.)

**Check Update Channel**
* `/checkupdatechannel`
* Will return the channel updates are sent to
* If it returns nothing: Try using `/updatechannel` to change it to a new channel

**Check Admin Channel**
* `/checkadminchannel`
* Will return the admin channel updates are sent to
* If it returns nothing: Try using `/adminchannel` to change it to a new channel


# More coming soon!
School Safe Bot is always under developement. If you like using School Safe Bot please consider contributing to the code or donating! Thanks!