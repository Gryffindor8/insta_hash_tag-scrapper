from instabot import Bot
import time, json

bot = Bot()

with open('config.json') as fl:
    config = json.load(fl)

try:
    us = config['username']
    ps = config['password']
    tag = config['hashtag']
    max_ = int(config['total posts to scrape'])
except:
    print('error in config file')
    input('please recheck the file and start again')

lgin = bot.login(username=us, password=ps, force=True, use_cookie=False)

if lgin:
    print('logged in successfully')
else:
    print('Couldn\'t log in, please check your credentials and try again!')
    input('hit ENTER to exit ')
    exit()


print('*'*8 + f'scraping {max_} posts from #{tag}' + "*"*8)

try:
    posts = bot.get_total_hashtag_medias(tag, max_)
except:
    print('an error occured')
    print('exiting...')
    exit()

print('resting for 15s')
time.sleep(15)

mails = set()

print('scrapping emails')
def work():
    for post in posts:
        try:
            uid = bot.get_media_owner(post)
            if uid not in usernames:
                ml = bot.get_user_info(uid)['public_email']
                if ml:
                    mails.add()
            print('total posts scrapped: {posts.index(post) + 1}; emails got: {len(mails)}', end='\r')
        except:
            pass

    with open('emails.txt', 'a+') as fl:
        fl.write('\n'.join(mails) + '\n')

try:
    work()
    print('work done!')
    print(f'{len(mails)} scrapped from {max_} posts')
    print('mails saved at "emails.txt"')
    input('hit ENTER to exit')
except:
    with open('emails.txt', 'a+') as fl:
        fl.write('\n'.join(mails) + '\n')
    posts = [str(post) for post in posts]
    with open('incomplete.txt', 'w+') as fl:
        fl.write('\n'.join(posts))
    print('an error was occured')
    print('files saved')
    input('please get new version to start where it left')
