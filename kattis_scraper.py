from bs4 import BeautifulSoup
import requests

_HEADERS = {'User-Agent': 'kattis-scraper'}

def login(s, login_url, username, password=None, token=None):
    """Log in to Kattis.

    At least one of password or token needs to be provided.

    Returns a requests.Response with cookies needed to be able to submit
    """
    login_args = {'user': username, 'script': 'true'}
    if password:
        login_args['password'] = password
    if token:
        login_args['token'] = token

    return s.post(login_url, data=login_args, headers=_HEADERS)


def getSolvedProblems(username, password):
    """Get a list of all solved problems corresponding to the username.

    Username can be interchanged with email.
    """
    # Start a session and log in
    s = requests.Session()
    loginurl = "https://open.kattis.com/login/email"
    if login(s, loginurl, username, password).text != "Login successful":
        print("Couldn't log you in. Are you sure you're using the right username/password?")
        return []

    # navigate to the solved problems page
    url = "https://open.kattis.com/problems?order=problem_difficulty&show_solved=on&show_tried=off&show_untried=off"
    r = s.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')

    # iterate through all pages of solved problems and grab their names
    solved_problems = []
    while True:
        nxt = soup.find('a', {'id': 'problem_list_next'})
        tds = soup.findAll("tr", {"class": "solved"})
        for problem in tds:
            td = (problem.find("td", {"class": "name_column"}))
            solved_problems.append(td.find("a").contents[0])
        # if there's another page, navigate to it. otherwise, we're doen
        if nxt.has_attr('href'):
            link = nxt['href']
            link = "https://open.kattis.com" + link
            r = s.get(link)
            soup = BeautifulSoup(r.text, 'html.parser')
        else:
            break
        
    return solved_problems
