from socialstats.main import UserFactory


def get_stat(platform: str, username: str) -> dict:
    """Return user information in dictionary format."""
    user = UserFactory.create_user(platform=platform, username=username)
    return dict(user)
