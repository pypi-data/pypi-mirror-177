import re
from abc import ABCMeta, abstractmethod
from collections import defaultdict
from datetime import datetime
from types import MappingProxyType

import requests
from bs4 import BeautifulSoup
from dateutil import relativedelta


class Constant:
    """Class for organizing constants."""

    # API endpoints

    # codeforces endpoints
    cf_user_info = 'https://codeforces.com/api/user.info?handles={0}'
    cf_user_status = 'https://codeforces.com/api/user.status?handle={0}'
    cf_user_rating = 'https://codeforces.com/api/user.rating?handle={0}'

    # leet-code endpoints
    leetcode_api_endpoint = 'https://leetcode.com/graphql'

    # codechef endpoint
    codechef_web_endpoint = 'https://www.codechef.com/users/{0}'

    available_platforms = MappingProxyType({
        'codeforces': 'codeforces',
        'leetcode': 'leetcode',
        'codechef': 'codechef',
    })


class BaseUser:
    """Base user class."""

    first_name: str = ''
    last_name: str = ''
    email: str = ''
    username: str = ''

    def __iter__(self):
        """Provide dict representation of the class."""
        iters = {key: val_ for key, val_ in self.__dict__.items() if key[:2] != '__'}
        iters.update(self.__dict__)

        for key, val_ in iters.items():
            yield key, val_

    def __str__(self):
        """Override default str."""
        return str(self.__class__) + '\n' + '\n'.join(
            ('{0} = {1}'.format(attr, self.__dict__[attr]) for attr in self.__dict__),
        )


class CFUser(BaseUser):
    """Codeforces user class."""

    org: str = ''
    rating: int = 0
    rank: int = 0
    max_rating: int = 0
    max_rank: str = ''
    contests: int = 0
    submissions: int = 0
    accepted: int = 0
    wrong_ans: int = 0
    tle: int = 0
    contributions: int = 0
    registration_unix_time: int = 0

    @property
    def rating_color(self):
        """Return the rating color."""
        return self._get_color(self.rating)

    @property
    def max_rating_color(self):
        """Return color of max_rating."""
        return self._get_color(self.max_rating)

    @property
    def member_since(self):
        """Return the number of years at codeforces."""
        joined_at = datetime.fromtimestamp(self.registration_unix_time)
        rd = relativedelta.relativedelta(datetime.now(), joined_at)
        return int(rd.years)

    @classmethod
    def _get_color(cls, rating):  # NOQA: WPS231
        """Return the HEX of appropriate color according to the rating."""
        if rating <= 1199:  # NOQA: WPS223
            col = '#cec8c1'
        elif 1199 < rating <= 1399:
            col = '#43A217'
        elif 1399 < rating <= 1599:
            col = '#22C4AE'
        elif 1599 < rating <= 1899:
            col = '#1427B2'
        elif 1899 < rating <= 2099:
            col = '#700CB0'
        elif 2099 < rating <= 2299:
            col = '#F9A908'
        elif 2299 < rating <= 2399:
            col = '#FBB948'
        else:
            col = '#FF0000'
        return col


class LeetUser(BaseUser):
    """Leetcode user class."""

    about: str = ''
    avatar_url: str = ''
    skills: list = []
    country: str = ''
    ranking: int = 0
    submission: int = 0
    easy: int = 0
    medium: int = 0
    hard: int = 0
    contest_rating: float = 0
    contest_rank: int = 0
    badge: str = ''


class CodeChefUser(BaseUser):
    """Codechef user model."""

    motto: str = ''
    avatar_url: str = ''
    org: str = ''
    country: str = ''
    rating: int = 0
    profession: str = ''
    highest_rating: int = 0
    star: int = 0
    solved: int = 0
    authored: int = 0
    tested: int = 0
    contributed: int = 0


class CFBuilder:
    """Codeforces builder class."""

    user = CFUser()

    def __init__(self, username):
        """Construct builder."""
        self.user.username = username

    def _get_user_info(self):
        """Get data from codeforces user.info api."""
        url = Constant.cf_user_info.format(self.user.username)
        try:
            response = requests.get(url)
        except Exception:
            raise ValueError('Could not connect to the codeforces API')
        return response.json().get('result')[0]

    def _get_user_sub(self):
        """Get data from codeforces user.status api."""
        url = Constant.cf_user_status.format(self.user.username)
        try:
            response = requests.get(url)
        except Exception:
            raise ValueError('Could not connect to the codeforces API')
        return response.json().get('result')

    def _get_rating_changes(self):
        """Get all rating changes from codeforces api."""
        url = Constant.cf_user_rating.format(self.user.username)
        try:
            response = requests.get(url)
        except Exception:
            raise ValueError('Could not connect to the codeforces API')
        return response.json().get('result')

    def build_user_info(self):
        """Build user info part."""
        user_info = self._get_user_info()
        self.user.first_name = user_info.get('firstName', '')
        self.user.last_name = user_info.get('lastName', '')
        self.user.org = user_info.get('organization', '')
        self.user.rating = user_info.get('rating', 0)
        self.user.rank = user_info.get('rank', 'newbie')
        self.user.max_rating = user_info.get('maxRating', 0)
        self.user.max_rank = user_info.get('maxRank', 'newbie')
        self.user.contributions = user_info.get('contribution', 0)
        self.user.registration_unix_time = user_info.get('registrationTimeSeconds', 0)
        return self

    def build_user_submission(self):
        """Build user submission detail part."""
        user_submission = self._get_user_sub()
        self.user.submissions = len(user_submission)
        freq: dict = defaultdict(lambda: 0)
        for sb in user_submission:
            freq[sb['verdict']] += 1

        self.user.accepted = freq['OK']
        self.user.wrong_ans = freq['WRONG_ANSWER']
        self.user.tle = freq['TIME_LIMIT_EXCEEDED']
        return self

    def build_rating_changes(self):
        """Set total number of contests participated by the user."""
        rating_changes = self._get_rating_changes()
        self.user.contests = len(rating_changes)
        return self

    def return_user(self):
        """Return an instance of user."""
        return self.user


class LeetBuilder:
    """Leetcode builder class."""

    user = LeetUser()

    def __init__(self, username: str):
        """Construct builder."""
        self.user.username = username

    def _query_basic_profile(self):
        """Query data from leetcode graphql API."""
        query = {
            'operationName': 'data',
            'variables': {'username': self.user.username},
            'query': """
                query data($username: String!) {
                    user: matchedUser(username: $username) {
                        username
                        profile { 
                            realname: realName 
                            about: aboutMe 
                            avatar: userAvatar 
                            skills: skillTags 
                            country: countryName 
                            ranking
                        }
                    }
            }
            """,
        }
        try:
            response = requests.post(Constant.leetcode_api_endpoint, json=query)
        except Exception:
            raise ValueError('Could not connect to the leetcode API')
        return response.json().get('data')

    def _query_submissions(self):
        """Query data from leetcode graphql API."""
        query = {
            'operationName': 'data',
            'variables': {'username': self.user.username},
            'query': """
                query data($username: String!) {
                    submissions: matchedUser(username: $username) {
                        submits: submitStats {
                            ac: acSubmissionNum { difficulty count }
                        }
                    }
                }
            """,
        }
        try:
            response = requests.post(Constant.leetcode_api_endpoint, json=query)
        except Exception:
            raise ValueError('Could not connect to the leetcode API')
        return response.json().get('data')

    def _query_contest_info(self):
        """Query data from leetcode graphql API."""
        query = {
            'operationName': 'data',
            'variables': {'username': self.user.username},
            'query': """
                query data($username: String!) {
                    contest: userContestRanking(username: $username) {
                        rating
                        ranking: globalRanking
                        badge {
                            name
                        }
                    }
                }
            """,
        }
        try:
            response = requests.post(Constant.leetcode_api_endpoint, json=query)
        except Exception:
            raise ValueError('Could not connect to the leetcode API')
        return response.json().get('data')

    def build_basic_profile(self):
        """Build user basic profile info."""
        user_data = self._query_basic_profile().get('user')
        if not user_data:
            raise ValueError('No user data found.')
        profile = user_data.get('profile')
        self.user.first_name = profile.get('realname')
        self.user.about = profile.get('about')
        self.user.avatar_url = profile.get('avatar')
        self.user.skills = profile.get('skills')
        self.user.country = profile.get('country')
        self.user.ranking = profile.get('ranking')

        return self

    def build_submission_info(self):
        """Build user submission info."""
        submissions = self._query_submissions().get('submissions')
        if not submissions:
            raise ValueError('No user data found.')

        acc_sub = submissions.get('submits').get('ac')
        for sub_data in acc_sub:  # NOQA: WPS110
            if sub_data.get('difficulty') == 'All':
                self.user.submission = sub_data.get('count')
            elif sub_data.get('difficulty') == 'Easy':
                self.user.easy = sub_data.get('count')
            elif sub_data.get('difficulty') == 'Medium':
                self.user.medium = sub_data.get('count')
            elif sub_data.get('difficulty') == 'Hard':
                self.user.hard = sub_data.get('count')

        return self

    def build_contest_info(self):
        """Build user contest info."""
        contest = self._query_contest_info().get('contest')
        if not contest:
            raise ValueError('No user data found.')

        self.user.contest_rating = contest.get('rating')
        self.user.contest_rank = contest.get('ranking')
        self.user.badge = contest.get('badge', '')

        return self

    def return_user(self):
        """Return an instance of user."""
        return self.user


class CodeChefBuilder:
    """Codechef stat builder class."""

    user = CodeChefUser()

    def __init__(self, username: str):
        """Construct builder."""
        self.user.username = username

    def _scrap_data(self):
        """Scrap codechef profile data."""
        scrapped_data = {}
        try:
            response = requests.get(
                Constant.codechef_web_endpoint.format(self.user.username),
            )
        except Exception:
            raise ValueError('Could not load the codechef website.')
        soup = BeautifulSoup(response.text, 'lxml')

        scrapped_data['name'] = soup.find('h1', class_='h2-style').text
        scrapped_data['avatar_url'] = soup.find('img', class_='profileImage').get('src')

        star_text = soup.find('span', class_='rating').text
        scrapped_data['star'] = re.findall(r'\d+', star_text)[0]

        scrapped_data['country'] = soup.find('span', class_='user-country-name').text

        star_text = soup.find('a', class_='rating').text
        scrapped_data['rating'] = re.findall(r'\d+', star_text)[0]

        lis = soup.find_all('li')
        for li in lis:
            if 'Motto' in li.text:
                scrapped_data['motto'] = li.text.replace('Motto:', '')
            elif 'Student/Professional' in li.text:
                scrapped_data['profession'] = li.text.replace('Student/Professional:', '')
            elif 'Institution' in li.text:
                scrapped_data['org'] = li.text.replace('Institution:', '')

        solved_html = soup.find('section', class_='rating-data-section problems-solved').h5.text
        scrapped_data['solved'] = re.findall(r'\d+', solved_html)[0]

        contribution_html = soup.find_all('h5', class_='collapse')
        for h5 in contribution_html:
            if 'Authored' in h5.text:
                scrapped_data['authored'] = re.findall(r'\d+', h5.text)[0]
            elif 'Tested' in h5.text:
                scrapped_data['tested'] = re.findall(r'\d+', h5.text)[0]
            elif 'Contributed' in h5.text:
                scrapped_data['contributed'] = re.findall(r'\d+', h5.text)[0]

        small_tags = soup.find_all('small')
        for tag in small_tags:
            if 'Highest Rating' in tag.text:
                scrapped_data['highest_rating'] = re.findall(r'\d+', tag.text)[0]

        return scrapped_data

    def build_profile(self):
        """Build user basic profile info."""
        scrapped_data = self._scrap_data()
        self.user.first_name = scrapped_data.get('name')
        self.user.avatar_url = scrapped_data.get('avatar_url')
        self.user.star = scrapped_data.get('star')
        self.user.rating = scrapped_data.get('rating')
        self.user.highest_rating = scrapped_data.get('highest_rating')
        self.user.motto = scrapped_data.get('motto')
        self.user.profession = scrapped_data.get('profession')
        self.user.country = scrapped_data.get('country')
        self.user.org = scrapped_data.get('org')
        self.user.solved = scrapped_data.get('solved')
        self.user.authored = scrapped_data.get('authored')
        self.user.tested = scrapped_data.get('tested')
        self.user.contributed = scrapped_data.get('contributed')

        return self

    def return_user(self):
        """Return an instance of user."""
        return self.user


class IDirector(metaclass=ABCMeta):
    """Director interface."""

    @staticmethod
    @abstractmethod
    def construct(username: str):
        """Construct an object."""


class CFDirector(IDirector):
    """Director class for building codeforces user."""

    @staticmethod
    def construct(username: str):
        """Construct codeforces user part by part."""
        return CFBuilder(username) \
            .build_user_info() \
            .build_user_submission() \
            .build_rating_changes() \
            .return_user()


class LeetDirector(IDirector):
    """Director class for building leetcode user."""

    @staticmethod
    def construct(username: str):
        """Construct leetcode user part by part."""
        return LeetBuilder(username) \
            .build_basic_profile() \
            .build_submission_info() \
            .build_contest_info() \
            .return_user()


class CodeChefDirector(IDirector):
    """Director class for building codechef user."""

    @staticmethod
    def construct(username: str):
        """Construct codechef user part by part."""
        return CodeChefBuilder(username) \
            .build_profile() \
            .return_user()


class UserFactory:
    """Builds user."""

    @classmethod
    def create_user(cls, platform: str, username: str):
        """Return expected user according to the platform."""
        director = None
        if platform == Constant.available_platforms.get('codeforces'):
            director = CFDirector
        if platform == Constant.available_platforms.get('leetcode'):
            director = LeetDirector  # type: ignore
        if platform == Constant.available_platforms.get('codechef'):
            director = CodeChefDirector  # type: ignore
        if not director:
            raise ValueError('unsupported platform: {0}'.format(platform))

        return director.construct(username)


if __name__ == '__main__':
    print('############## CODEFORCES ##############')
    cf_user = UserFactory.create_user(platform='codeforces', username='tourist')
    print(cf_user)
    print('############## LEETCODE ##############')
    leet_user = UserFactory.create_user(platform='leetcode', username='sudiptob2')
    print(leet_user)
    print('############## CODECHEF ##############')
    codechef_user = UserFactory.create_user(platform='codechef', username='sudiptob2')
    print(codechef_user)
