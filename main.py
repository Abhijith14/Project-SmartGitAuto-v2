import http.client
import json

from github import Github, GithubException
import os
import tqdm
# import time

repo_list = []
sorted_categories = ["Artificial Intelligence", "Python", "VB.NET", "C/C++", "Java", "Apps", "C#", "Websites", "Others"]
projectTypes_list = {
    'None': 'Others',
    'Python': 'Python',
    'Jupyter Notebook': 'Python',
    'HTML': 'Websites',
    'CSS': 'Websites',
    'PHP': 'Websites',
    'JavaScript': 'Websites',
    'Hack': 'Websites',
    'C': 'C/C++',
    'C++': 'C/C++',
    'C#': 'C#',
    'Visual Basic .NET': 'VB.NET',
    'Java': 'Java',
    'Dart': 'Apps',
    'Kotlin': 'Apps',
    'PowerShell': 'VB.NET'
}

projectLogo_list = {
    'Others': 'media/lang/project.png',
    'Python': 'media/lang/python.png',
    'Jupyter Notebook': 'media/lang/jupyter.png',
    'Artificial Intelligence': 'media/lang/ai.png',
    'Java': 'media/lang/java.png',
    'C': 'media/lang/C.png',
    'C++': 'media/lang/cpp.png',
    'C#': 'media/lang/csharp.png',
    'VB.NET': 'media/lang/vb.png',
    'Websites': 'media/lang/web.png',
    'Kotlin': 'media/lang/kotlin.png',
    'Dart': 'media/lang/kotlin.png'
}

g = Github(os.environ["ACCESS_TOKEN"])
current_user = g.get_user()
maxStars, maxContributors, maxForks = 0, 0, 0
# maxStarsR, maxContributorsR, maxForksR = '', '', ''
print("Logged in as : SmartGitAuto. Username :", current_user.login)


def ret_ignored_projects():
    repos = current_user.get_repos()
    for repo in repos:
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


def start_scraping(repos):
    global repo_list, current_user
    global maxStars, maxContributors, maxForks  # , maxStarsR, maxContributorsR, maxForksR
    # find all the repos with config file
    c = 0

    print("Scraping Initiated ...")

    for repo in tqdm.tqdm(list(repos)):
        try:
            if not repo.organization:
                # print(repo.name, ":", repo.language)

                contents = repo.get_contents("")
                while contents:
                    file_content = contents.pop(0)
                    if file_content.path == '.SmartGitAuto':
                        repo_list.append(repo)

                        if not repo.fork:
                            if repo.get_stargazers().totalCount > maxStars:
                                maxStars = repo.get_stargazers().totalCount
                                # maxStarsR = repo
                            if repo.get_contributors().totalCount > maxContributors:
                                maxContributors = repo.get_contributors().totalCount
                                # maxContributorsR = repo
                                # print("NEXT : ", maxContributorsR, " - ", maxContributors)
                            if repo.get_forks().totalCount > maxForks:
                                maxForks = repo.get_forks().totalCount
                                # maxForksR = repo

                c = c + 1
        except GithubException:
            pass


def get_project_logo(repo, projectCat):

    multipleImg = ['C/C++', 'Apps']
    if projectCat in multipleImg:
        projectCat = str(repo.language)

    projectLogo_ret = projectLogo_list[projectCat]

    if projectCat == 'Python':
        try:
            projectLogo_ret = projectLogo_list[str(repo.language)]
        except KeyError:  # Forcing the category to be Python
            projectLogo_ret = projectLogo_list['Python']

    try:
        contents = repo.get_contents("readme_assets/logo.png")
        if 'ignore-assets' not in list(repo.get_topics()):
            projectLogo_ret = contents.download_url
    except Exception as e:
        # print(e)
        pass

    return projectLogo_ret


def get_project_links(repo):
    if repo.homepage:
        homeurl = repo.homepage
    else:
        homeurl = ''
    if not repo.private:
        return repo.html_url, homeurl
    else:
        return '', homeurl


def get_project_header(repo):
    # Todo: algo for multiple headers together
    if repo.get_stargazers().totalCount == maxStars:
        return "MOST STARRED REPO"
    elif repo.get_contributors().totalCount == maxContributors:
        return "MOST CONTRIBUTED REPO"
    elif repo.get_forks().totalCount == maxForks:
        return "MOST FORKED REPO"
    else:
        return ''


def get_homepage_visible(repo):
    if 'web-homepage' in list(repo.get_topics()):
        return 1
    else:
        return 0


def sort_the_repos(projList):
    global sorted_categories
    projectList = []
    for cat in sorted_categories:
        [projectList.append(i) for i in projList if i['category'] == cat]
    return projectList


def get_project_category(repo):
    global sorted_categories
    curr_cat = ""
    for _, i in enumerate(sorted_categories):
        i = i.lower()
        i = i.replace(" ", "-")

        if i in list(repo.get_topics()):
            curr_cat = sorted_categories[_]
            break

    if not curr_cat:
        curr_cat = projectTypes_list[str(repo.language)]

    return curr_cat


def get_variables(repo_list_new):
    global maxStars, maxContributors, maxForks
    project_list = []
    print("Collecting Variables ...")
    for repo in tqdm.tqdm(repo_list_new):
        # repo = g.get_repo(repo)
        temp_dict = {}
        projectName = repo.name
        if str(repo.language) in projectTypes_list.keys():
            projectCategory = get_project_category(repo)  # projectTypes_list[str(repo.language)]
            projectLogo = get_project_logo(repo, projectCategory)
            projectContributors = repo.get_contributors().totalCount
            projectIssues = repo.get_issues().totalCount
            projectStars = repo.get_stargazers().totalCount
            projectForks = repo.get_forks().totalCount
            if repo.description:
                projectDescription = repo.description
            else:
                projectDescription = ''
            projectRepo, projectLink = get_project_links(repo)
            projectHeader = get_project_header(repo)
            projectH_visible = get_homepage_visible(repo)
            if repo.private:
                projectAccess = 1
            else:
                projectAccess = 0

            temp_dict['name'] = projectName
            temp_dict['category'] = projectCategory
            temp_dict['logo'] = projectLogo
            temp_dict['contributors'] = projectContributors
            temp_dict['issues'] = projectIssues
            temp_dict['stars'] = projectStars
            temp_dict['forks'] = projectForks
            temp_dict['desc'] = projectDescription
            temp_dict['repo'] = projectRepo
            temp_dict['link'] = projectLink
            temp_dict['header'] = projectHeader
            temp_dict['H_visible'] = projectH_visible
            temp_dict['Access'] = projectAccess
            project_list.append(temp_dict)

        else:
            print("Project Category - [{}] Does Not Exist !! ({})".format(repo.language, repo.html_url))
            # return False

    project_list = sort_the_repos(project_list)
    # project_list = json.dumps(project_list, indent=4)
    return project_list


def save(json_file):
    global g
    # Repo Object
    repo = g.get_repo("Abhijith14/Portfolio-v2")
    contents = repo.get_contents('database.json')
    repo.delete_file(contents.path, 'db deleted', contents.sha)
    print("DB RESET")
    while True:
        try:
            new_cont = repo.get_contents('database.json')
            continue
        except GithubException as e:
            print("Database not found, breaking from the loop...")
            break
#     time.sleep(5)
    repo.create_file("database.json", "db created", json_file)


def main():
    global repo_list, current_user
    repos = current_user.get_repos()
    start_scraping(repos)
    project_list = get_variables(repo_list)

    # reading database.json
    data_file = dict(json.load(open('database.json')))
    data_file['works'] = project_list
    data_file = json.dumps(data_file, indent=4)
    # print(data_file)

    save(data_file)


main()
# ret_ignored_projects()
