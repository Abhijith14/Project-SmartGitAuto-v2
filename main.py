import http.client
import json

from github import Github, GithubException
import os
import tqdm

g = Github(os.environ["ACCESS_TOKEN"])
current_user = g.get_user()
maxStars, maxContributors, maxForks = 0, 0, 0
# maxStarsR, maxContributorsR, maxForksR = '', '', ''
print("Logged in as : SmartGitAuto. Username :", current_user.login)


def ret_ignored_projects():
    repos = current_user.get_repos()
    for repo in tqdm.tqdm(list(repos)):
        try:
            contents = repo.get_contents("")
            temp = False
            while contents:
                file_content = contents.pop(0)
                if file_content.path == '.SmartGitAuto':
                    temp = True
                    break

            if not temp:
                print(repo.name, ":", repo.language, ':', repo.html_url)
        except:
            pass



ret_ignored_projects()
