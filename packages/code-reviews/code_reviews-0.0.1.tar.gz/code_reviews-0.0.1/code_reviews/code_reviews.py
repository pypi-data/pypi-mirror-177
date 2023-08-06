import configparser
import logging
import os
import sys

from github import Github
import base64
import requests
import appdirs

logging.basicConfig(filename='/tmp/code_reviews.log',
                    filemode='w',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.INFO)

logger = logging.getLogger('code_reviews')


CONFIG_FILE = 'code_reviews.ini'


# TODO: small rewrite config
#  add approved/commented, add draft, add --manager mode?


def config():
    cfg = configparser.ConfigParser()
    if sys.platform == 'linux':
        os.environ['XDG_CONFIG_DIRS'] = '/etc:/usr/local/etc'
    cfg_dirs = appdirs.site_config_dir('code_reviews', multipath=True).split(':')
    cfg_dirs.append(appdirs.user_config_dir('code_reviews'))
    cfg_dirs.append(os.path.dirname(os.path.abspath(__file__)))
    cfg_dirs.reverse()
    for d in cfg_dirs:
        cfg_file_path = os.path.join(d, CONFIG_FILE)
        cfg.read(cfg_file_path)
        if 'github.com' in cfg:
            access_token = cfg['github.com']['access_token']
            alias = cfg['github.com']['alias']
            repo = cfg['github.com']['repo']
            if access_token == '<INSERT_ACCESS_TOKEN>' or alias == '<INSERT_ALIAS>' or repo == '<INSERT_REPO>':
                print(f'insert your credentials in {cfg_file_path}')
                return
            return access_token, alias, repo
    else:
        cfg_file_path = os.path.join(appdirs.user_config_dir('code_reviews'), CONFIG_FILE)
        try:
            cfg['github.com'] = {
                'access_token': '<INSERT_USER>', 
                'alias': '<INSERT_PASSWORD>', 
                'repo': '<INSERT_REPO>'
            }
            if not os.path.exists(cfg_file_path):
                os.makedirs(os.path.dirname(cfg_file_path))
            with open(cfg_file_path, 'w') as configfile:
                cfg.write(configfile)
            print(f"config auto created on {cfg_file_path}")
        except Exception as e:
            print(f"failed config read, error '{str(e)}' to auto-create empty config: {cfg_file_path}")


def print_github_info(access_token, alias, repo, argos):
    try:
        g = Github(access_token)
        repo = g.get_repo(repo)
    
        count_reviewed_not_approved = 0
        count_to_review = 0
        prs_reviewed_not_approved = []
        prs_to_review = []
        n_files = 0
    
        notifications = [n for n in repo.get_notifications(all=True) if n.reason == 'review_requested']
        for n in notifications:
            pr = n.get_pull_request()
            if pr.state not in ['closed', 'merged']:  # open
                # review_requests: is about pending review requests.
                # Once a person approves, comments, or rejects, it disappears from the list.
                # Thus, it is a perfectly valid situation to have this list empty
                # while there are might be 5 different people who left their feedback
                my_pr_pending_reviews = list(filter(lambda reviewer: reviewer.login == alias, pr.get_review_requests()[0]))
                if my_pr_pending_reviews:
                    count_to_review += 1
                    prs_to_review.append(pr)
                    n_files += len(list(pr.get_files()))
                else:
                    my_pr_reviews = filter(lambda review: review.user.login == alias, pr.get_reviews())
                    my_pr_reviews = sorted(my_pr_reviews, key=lambda review: review.id, reverse=True)
                    if my_pr_reviews and my_pr_reviews[0].state != 'APPROVED':
                        count_reviewed_not_approved += 1
                        prs_reviewed_not_approved.append(pr)
                        n_files += len(list(pr.get_files()))
    
        logger.info(f'prs_reviewed_not_approved: {prs_reviewed_not_approved}')
        logger.info(f'prs_to_review: {prs_to_review}')
    
        my_prs_waiting_g = filter(lambda mpr: mpr.user.login == alias, repo.get_pulls(state='open'))
        my_prs_waiting = list(my_prs_waiting_g)
        my_prs_waiting_count = len(my_prs_waiting)
        n_comments = 0
        my_prs_waiting_ = []
        for pr in my_prs_waiting:
            n_comments += len(list(pr.get_comments()))
            my_prs_waiting_.append(pr)
    
        logger.info(f'my_prs_waiting: {my_prs_waiting_}')
    
        def short_name(name):
            name = name.split(' ')
            return f'{name[0]} {name[1][0].upper()}.'
    
        def get_reviewers(pull_req):
            reviewers = [short_name(rr.name) for rr in pull_req.get_review_requests()[0] if rr.login != alias]
            if not reviewers:
                reviewers = [short_name(rr.user.name) for rr in pull_req.get_reviews() if rr.user.login != alias]
            return sorted(set(reviewers))

        if not argos:
            print(f'CR[{n_files}]: todo {count_to_review}, doing {count_reviewed_not_approved}; '
                  f'PR[{n_comments}]: waiting {my_prs_waiting_count}')
            print('---')
            print('My code reviews to do')
            for cr in prs_to_review:
                print(
                    f"--{cr.number} - {cr.title} from {cr.user.name} at '{cr.html_url}'")
            print('---')
            print('My code reviews in doing')
            for cr in prs_reviewed_not_approved:
                print(
                    f"--{cr.number} - {cr.title} from {cr.user.name} at '{cr.html_url}'")
            print('---')
            print('My pull request in waiting')
            for pr in my_prs_waiting_:
                print(
                    f"--{pr.number} - {pr.title} to {', '.join(get_reviewers(pr))} at '{pr.html_url}'")
        else:
            favicon = str(base64.b64encode(requests.get('https://github.com/favicon.ico').content).decode("utf-8"))
            print(f'CR[{n_files}]: todo {count_to_review}, doing {count_reviewed_not_approved}; '
                  f'PR[{n_comments}]: waiting {my_prs_waiting_count}')
            print('---')
            print('My code reviews to do')
            for cr in prs_to_review:
                print(f"--{cr.number} - {cr.title} from {cr.user.name} | "
                      f"image='{favicon}' imageWidth=30 href='{cr.html_url}'")
            print('---')
            print('My code reviews in doing')
            for cr in prs_reviewed_not_approved:
                print(f"--{cr.number} - {cr.title} from {cr.user.name} | "
                      f"image='{favicon}' imageWidth=30 href='{cr.html_url}'")
            print('---')
            print('My pull request in waiting')
            for pr in my_prs_waiting_:
                print(f"--{pr.number} - {pr.title} to {', '.join(get_reviewers(pr))} | "
                      f"image='{favicon}' imageWidth=30 href='{pr.html_url}'")
        
    except Exception as e:
        logger.exception(e)
        print('CR[?]: error; PR[?]: error')


def main():
    argos = len(sys.argv) > 1 and sys.argv[1] == '--output-argos'
    cfg = config()
    if cfg:
        print_github_info(*cfg, argos)


if __name__ == "__main__":
    main()
