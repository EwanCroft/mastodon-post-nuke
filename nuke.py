import configparser
import os
from mastodon import Mastodon

if not os.path.exists('config.ini'):
    url = input("Enter the URL of your Mastodon instance:\n")
    email = input("Enter your email address:\n")
    password = input("Enter your password:\n")
    
    app_info = Mastodon.create_app(
        "Post Nuke",
        api_base_url = f"{url}"
    )

    config = configparser.ConfigParser()
    config['MASTODON'] = {'url': url, 'email': email, 'password': password, 'client_id': app_info.client_id, 'client_secret': app_info.client_secret}
    with open('config.ini', 'w') as configfile:
        config.write(configfile)

config = configparser.ConfigParser()
config.read('config.ini')
url = config['MASTODON']['url']
email = config['MASTODON']['email']
password = config['MASTODON']['password']
client_id_str = config['MASTODON']['client_id']
client_secret_str = config['MASTODON']['client_secret']

mastodon = Mastodon(client_id = client_id_str)

mastodon.log_in(email, password)

max_id = None
while True:
    posts = mastodon.account_statuses(mastodon.me().id, max_id=max_id)
    if not posts:
        break
    for post in posts:
        mastodon.status_delete(post['id'])
        print(f"Post {post['id']} deleted.")
    max_id = min([p['id'] for p in posts]) - 1