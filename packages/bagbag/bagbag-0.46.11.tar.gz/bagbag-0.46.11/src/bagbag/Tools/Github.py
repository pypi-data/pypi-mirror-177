from __future__ import annotations

from github import Github as githubclient
from github.GithubException import RateLimitExceededException
from github.GithubException import GithubException

try:
    from .. import Http
    from .Ratelimit import RateLimit
    from ..String import String
    from .. import Time
    from .. import Lg
except:
    from Ratelimit import RateLimit
    import sys
    sys.path.append("..")
    import Http
    from String import String
    import Time
    import Lg

# class GithuException(Exception):
#     pass 

# class NoNewItem(GithuException):
#     pass 

class GithubSearchResult():
    def __init__(self):
        self.url:str = ""
        self.content:str = ""
        self.rawurl:str = ""

    def __str__(self) -> str:
        content = String(self.content.replace("\n", "\\n")).Ommit(160)
        return f"GithubSearchResult(url={self.url}, content={content}, rawurl={self.rawurl})"
    
    def __iter__(self):
        # first start by grabbing the Class items
        iters = dict((x,y) for x,y in GithubSearchResult.__dict__.items() if x[:2] != '__')

        # then update the class items with the instance items
        iters.update(self.__dict__)

        # now 'yield' through the items
        for x,y in iters.items():
            yield x,y

class GithubSearchResults():
    def retryOnRateLimitAfterSleep(func): # func是被包装的函数
        def ware(self, *args, **kwargs): # self是类的实例
            while True:
                try:
                    res = func(self, *args, **kwargs)
                    break
                except RateLimitExceededException:
                    Lg.Trace("GitHub rest API ratelimit, sleep for 30 seconds.")
                    Time.Sleep(30)

            return res

        return ware

    @retryOnRateLimitAfterSleep
    def __init__(self, github:Github, pattern:str):
        self.token = github.token 
        self.g = github.g 
        self.rl = github.rl 

        self.repos = self.g.search_code(pattern)

        self.rl.Take()
        self.total = self.repos.totalCount
        self.pages = [i for i in range(0, int(self.total / self.g.per_page) + 1)]
        self.items = []

    @retryOnRateLimitAfterSleep
    def Get(self) -> GithubSearchResult | None:
        if self.total == 0:
            return None 

        if len(self.items) == 0 and len(self.pages) == 0:
            return None 

        if len(self.items) == 0:
            page = self.pages.pop(0)
            try:
                self.items = self.repos.get_page(page)
            except GithubException:
                return None 
        
            if len(self.items) == 0:
                return None 

        item = self.items.pop(0)

        url = item.html_url
        rawurl = url.replace("https://github.com", "https://raw.githubusercontent.com").replace("blob/", "")
        content = Http.Get(rawurl).Content

        res = GithubSearchResult()
        res.url = url 
        res.content = content 
        res.rawurl = rawurl
        
        return res

    def __iter__(self) -> GithubSearchResult:
        while True:
            res = self.Get()
            if res != None:
                yield res 
            else:
                return 

class Github():
    def __init__(self, token:str, ratelimit:str="30/m"):
        self.token = token 
        self.g = githubclient(token)
        self.rl = RateLimit(ratelimit)

        self.g.per_page = 100

    def Search(self, pattern:str) -> GithubSearchResults:
        return GithubSearchResults(self, pattern)

if __name__ == "__main__":
    import yaml 

    languages = Http.Get("https://raw.githubusercontent.com/github/linguist/master/lib/linguist/languages.yml").Content
    languages = yaml.safe_load(languages)

    token = ""
    keyword = ""

    g = Github(token, ratelimit = "60/m")

    for k in languages:
        v = languages[k]
        if 'codemirror_mode' in v and 'extensions' in v:
            for i in v['extensions']:
                pattern = "extension:" + i.lstrip('.') + " " + keyword
                Lg.Trace(f"Searching: {pattern}") # Searching: extension:py shadon_api_key
                for r in g.Search(pattern):
                    Lg.Trace("Found:", r)
