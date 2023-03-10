import os
import instaloader
import pandas as pd

from bot.settings import config


class Instagram:

    def __init__(self, target: str):
        self.loader = instaloader.Instaloader(user_agent=config.USER_AGENT)

        self.username = os.getenv('INSTA_USERNAME')
        self.password = os.getenv('INSTA_PASSWORD')
        self.login()

        self.target = target

        self.profile = instaloader.Profile.from_username(self.loader.context, self.target)

    def login(self):
        try:
            self.loader.load_session_from_file(self.username)
        except FileNotFoundError:
            self.loader.login(self.username, self.password)

    def get_unfollowers(self) -> tuple[int, set]:
        current_followers = self.get_followers()
        current_following = self.get_following()
        if len(current_followers) == len(current_following):
            raise ValueError('You dont have unfollowers or your account is private')

        difference = set(current_following).difference(set(current_followers))
        difference_length = len(difference)

        return difference_length, difference

    def get_followers(self) -> list:
        return [followers.username for followers in self.profile.get_followers()]

    def get_following(self) -> list:
        return [following.username for following in self.profile.get_followees()]

    def save_to_scv(self, data: list):
        df = pd.DataFrame(data)
        df.to_csv(f'./static/{self.target}/{self.target}.scv', index=False)
