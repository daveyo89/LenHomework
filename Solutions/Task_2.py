import bs4 as bs
import urllib.request
import csv
import traceback


def max_page():
    url = "https://github.com/github"
    sauce = urllib.request.urlopen(url).read()
    soup = bs.BeautifulSoup(sauce, 'html.parser')
    for page_num in soup.find_all('em'):
        num = int(page_num["data-total-pages"])
        return num


def git_scraper(page):
    url = "https://github.com/github?page={}".format(str(page))

    sauce = urllib.request.urlopen(url).read()
    soup = bs.BeautifulSoup(sauce, 'html.parser')
    for div in soup.find_all('li', {'itemprop': ['owns']}):
        try:
            reps = []
            repo_name = div.find("div", {'class': ['d-inline-block mb-1']}).select('h3')[0].text.strip()
            for r in div.find_all('a', {'class': ['topic-tag topic-tag-link f6 my-1']}):
                reps.append(r.text.strip())

            repo_desc = div.find('p', {'itemprop': ['description']}).text.strip()
            pr_lang = div.find('span', {'itemprop': ['programmingLanguage']})
            if pr_lang is not None:
                pr_lang = pr_lang.text.strip()

            results = [[repo_name], [repo_desc], [pr_lang], [reps]]
            with open(r"results.csv", 'a') as f:
                writer = csv.writer(f)
                writer.writerow(results)

            print(" Repo name: {0}\n Short description: {1}\n Programming Language: {2}\n Repo tags: {3}\n".format(
                repo_name, repo_desc, pr_lang, reps))

        except Exception as e:
            traceback.print_exc()
            continue


if __name__ == '__main__':
    open('results.csv', 'w').close()
    j = max_page()
    for i in range(1, j):
        git_scraper(i)
    print("\n\t ### Writing to results.csv completed.. ###")
