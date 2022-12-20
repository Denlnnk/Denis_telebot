import instaloader
import config
import logging


class Instagram:

    def __init__(self, target: str):
        self.loader = instaloader.Instaloader(user_agent=config.user_agent)

        self.username = config.insta_username
        self.password = config.insta_password
        self.login()

        self.target = target

        self.profile = instaloader.Profile.from_username(self.loader.context, self.target)

    def login(self):
        try:
            self.loader.load_session_from_file(self.username)
        except FileNotFoundError:
            logging.error('Log in with username and passwrd')
            self.loader.login(self.username, self.password)

    def get_followers(self):
        return [i.username for i in self.profile.get_followers()]

    def get_following(self):
        return [i.username for i in self.profile.get_followees()]

    def get_unfollowers(self) -> tuple[int, set]:
        current_followers = self.get_followers()
        current_following = self.get_following()
        if len(current_followers) == len(current_following):
            raise ValueError('You dont have unfollowers or your account is private')

        difference = set(current_following).difference(set(current_followers))
        difference_length = len(difference)

        return difference_length, difference