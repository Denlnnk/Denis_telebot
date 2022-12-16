import instaloader
import konfig

# Loading instaloader object
L = instaloader.Instaloader()

# Username
username = konfig.insta_username
password = konfig.insta_password

try:
    # Loading session stored in the system
    L.load_session_from_file(username)

except:
    # Login with username and password
    L.login(username, password)


def get_unfollowers(username_for_check: str = 'denlnnk'):
    # insta loader profile object
    profile = instaloader.Profile.from_username(L.context, username_for_check)

    # Current usernames
    current_followers = [i.username for i in profile.get_followers()]
    current_following = [i.username for i in profile.get_followees()]

    return set(current_following).difference(set(current_followers))
