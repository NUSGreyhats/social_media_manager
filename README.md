# Social Media Manager
A Tool to help post on various social media simultaneously

## Quick Start guide
1. Install dependencies using `pip install -r requirements.txt`
2. Start the website by running `python3 flaskr`
3. Stop the website using `Ctrl+C`
4. Fill up the configuration under `config.ini`
5. Run the server again by running `python3 flaskr`
6. Navigate to [`http://localhost:5000/`](http://localhost:5000/)
7. Fill up the form


## Guide to generating tokens for all the relavant settings

### Twitter
1. Create a twitter account
2. Request for developer access [here](https://developer.twitter.com/)
3. Request for elevated access

### Facebook
1. Create a facebook account
2. Go to [https://developers.facebook.com/](https://developers.facebook.com/) and create a developer account
3. Create an application
4. Go to [https://developers.facebook.com/tools/explorer/](https://developers.facebook.com/tools/explorer/) and generate an user token
5. Give `pubish_to_group` permission to the application
6. For facebook group ids follow the tutorial [here](https://www.slickremix.com/how-to-get-your-facebook-group-id/)


### Telegram
1. Go to `@BotFather` on telegram
2. Follow the instructions to create a new bot
3. Id will be shown at the end
4. For group id (Credits to [this post](https://stackoverflow.com/questions/32423837/telegram-bot-how-to-get-a-group-chat-id))
   1. open web.telegram in browser ( chrome in my case )
   2. right click on the group name on the left menu
   3. click 'inspect' button
   4. You will see the group id in the attribute data-peer-id="-xxxxxxxxxx" or peer="-xxxxxxxxxx"

