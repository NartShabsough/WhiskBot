# WhiskBot
Is a bot for managing restaurants, which allows to respond for basics tasks, and taking reservations. The bot works on Telegram App.


---------------

## Getting Started

1)  Download all files in one folder.
2)  Open terminal, and go to that directory 
```shell
  cd Desktop/yourDirectory
```

3)  Run bot.py file
```shell
  python3.6 bot.py
```
- bot should be now runnging

5)  Download Telegram App on iOS/Android and create an account.

6)  Add the bot @Whisk_Bot.

7)  Try using the bot.

---------------

## Documentation 

This bot is created from 4 files:

1)  bot.py: The mian file wiht all algorithms and methods.

2)  dbhelper.py: The database handling file.

3)  word.json and repleis.json: JSON files to read from common words.


### 1) bot.py

```python
def prepareResponse()
```
- This method handles all the messages and analyse the content of it for further computing.

```python
def handle_updates()
```
- This method get called every 0.5s to check for new comming messages.

```python
def handle_reservation()
```
- This method is called once a reservation request is detected.

```python
def new()
```
- This method create a new reservation once requested.

```python
def cancel()
```
- This method cancle a new reservation once requested.

```python
def showDates()
```
- This method display the dates on the keyoard instead of the normal keyboard.

```python
def handle_command()
```
- This method helps in the reservation making.

```python
def set_Date()
```
- This method create a list of dates based on the currunt date for reservation purposes.



### 2) dbhelper.py
### 3) word.json
### 4) repleis.json



















