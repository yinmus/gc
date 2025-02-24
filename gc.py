#!/usr/bin/env python3
import re, argparse, os, requests, subprocess, sys

GIT_URL = "https://github.com/"
USERS_API = "https://api.github.com/users/"
SEARCH_API = "https://api.github.com/search/"
REPO_API = "https://api.github.com/repos/"
ORG_API = "https://api.github.com/orgs/"
TOKEN_FILE = os.path.expanduser("~/.github_token")

RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"

def search_repos(repo_name=None, show_size=False, sort_by_stars=True):
    """
    :param repo_name: Имя репозитория для поиска
    :param show_size: Показать размер репозитория
    :param sort_by_stars: Сортировать по количеству звёзд
    """
    query = repo_name if repo_name else "stars:>10000"
    repos = search_github(query, "repositories")

    if sort_by_stars:
        repos = sorted(repos, key=lambda r: r["stargazers_count"], reverse=True)

    if repos:
        for repo in repos:
            size_info = f" ({YELLOW}{get_repo_size(repo['full_name'])}{RESET})" if show_size else ""
            print(f"{BLUE}{repo['html_url']}{RESET}  ({GREEN}{repo['stargazers_count']}★{RESET}){size_info}")
    else:
        print(f"{YELLOW}Репозитории не найдены{RESET}")

def get_token():
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "r") as f:
            return f.read().strip()
    return None

def save_token(token):
    with open(TOKEN_FILE, "w") as f:
        f.write(token)
    os.chmod(TOKEN_FILE, 0o600)
    print(f"{GREEN}Токен сохранён!{RESET}")

def show_token():
    token = get_token()
    if token:
        print(f"{GREEN}Сохранённый токен: {token}{RESET}")
    else:
        print(f"{YELLOW}Токен не найден!{RESET}")

def make_request(url):
    headers = {}
    token = get_token()
    if token:
        headers["Authorization"] = f"token {token}"
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 403:
            print(f"{RED}Превышен лимит запросов. Попробуйте позже.{RESET}")
        else:
            print(f"{RED}Ошибка запроса: {response.status_code}{RESET}")
    except Exception as e:
        print(f"{RED}Ошибка соединения: {e}{RESET}")
    return None

def search_github(query, search_type):
    data = make_request(f"{SEARCH_API}{search_type}?q={query}&per_page=10")
    return data.get("items", []) if data else []

def get_repo_size(repo_full_name):
    repo_data = make_request(f"{REPO_API}{repo_full_name}")
    if repo_data and "size" in repo_data:
        return f"{repo_data['size'] / 1024:.1f} MB"
    return "N/A"

def search_user_repos(username, show_size=False, sort_by_stars=False):
    repos = make_request(f"{USERS_API}{username}/repos")
    if repos:
        if sort_by_stars:
            repos = sorted(repos, key=lambda r: r["stargazers_count"], reverse=True)
        for repo in repos:
            size_info = f" ({YELLOW}{get_repo_size(repo['full_name'])}{RESET})" if show_size else ""
            print(f"{BLUE}{repo['html_url']}{RESET}  ({GREEN}{repo['stargazers_count']}★{RESET}){size_info}")
    else:
        print(f"{YELLOW}Репозитории пользователя не найдены{RESET}")

def search_users(username):
    users = search_github(username, "users")
    if users:
        for user in users:
            print(f"{BLUE}{user['html_url']}{RESET}  ({GREEN}{user['login']}{RESET})")
    else:
        print(f"{YELLOW}Пользователи не найдены{RESET}")

def search_organizations(org_name):
    orgs = search_github(org_name, "organizations")
    if orgs:
        for org in orgs:
            print(f"{BLUE}{org['html_url']}{RESET}  ({GREEN}{org['login']}{RESET})")
    else:
        print(f"{YELLOW}Организации не найдены{RESET}")

def handle_git_clone(repo):
    if not re.match(r"^[^/]+/[^/]+$", repo):
        print(f"{RED}Неверный формат репозитория! Используйте owner/repo.{RESET}")
        return

    repo_url = f"{GIT_URL}{repo}.git"
    response = make_request(f"{REPO_API}{repo}")

    if response:
        print(f"{GREEN}Клонирование {repo_url}...{RESET}")
        result = subprocess.run(f"git clone {repo_url}", shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"{RED}Ошибка при клонировании: {result.stderr}{RESET}")
    else:
        print(f"{RED}Репозиторий {repo} не найден!{RESET}")
def main():
    parser = argparse.ArgumentParser(description="GitHub CLI tool")
    parser.add_argument("-T", "--token", help="Сохранить GitHub-токен")
    parser.add_argument("-Tl", "--show-token", action="store_true", help="Показать сохранённый токен")
    parser.add_argument("-c", "--clone", help="Клонировать репозиторий")
    parser.add_argument("-sr", "--search-repo", help="Искать репозитории")
    parser.add_argument("-sur", "--search-user-repo", help="Искать репозитории пользователя")
    parser.add_argument("-su", "--search-user", help="Искать пользователей")
    parser.add_argument("-so", "--search-org", help="Искать организации")
    parser.add_argument("-k", "--show-size", action="store_true", help="Показать размер репозитория")
    parser.add_argument("-p", "--sort-by-stars", action="store_true", help="Сортировать по звёздам")
    args = parser.parse_args()
    if args.token:
        save_token(args.token)
    elif args.show_token:
        show_token()
    elif args.clone:
        handle_git_clone(args.clone)
    elif args.search_repo:
        search_repos(args.search_repo, args.show_size, args.sort_by_stars)
    elif args.search_user_repo:
        search_user_repos(args.search_user_repo, args.show_size, args.sort_by_stars)
    elif args.search_user:
        search_users(args.search_user)
    elif args.search_org:
        search_organizations(args.search_org)
    else:
        parser.print_help()
if __name__ == "__main__":
    main()
