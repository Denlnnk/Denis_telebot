import instaloader
import konfig


class InstaLoader:

    def __init__(self, username_for_check: str):
        self.L = instaloader.Instaloader()

        self.username = konfig.insta_username
        self.password = konfig.insta_password

        self.username_for_check = username_for_check

        try:
            self.L.load_session_from_file(self.username)
        except FileNotFoundError:
            self.L.login(self.username, self.password)

    def get_unfollowers(self) -> set[str]:
        profile = instaloader.Profile.from_username(self.L.context, self.username_for_check)

        current_followers = [i.username for i in profile.get_followers()]
        current_following = [i.username for i in profile.get_followees()]
        if len(current_followers) == len(current_following):
            raise ValueError('You dont have unfollowers or your account is private')

        return set(current_following).difference(set(current_followers))
