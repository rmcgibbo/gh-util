def configure_parser(sub_parsers):
    p = sub_parsers.add_parser('list-prs', help='List PRs merged since last release.')
    p.add_argument('repo', help='Repository spec (username/reponame)')
    p.set_defaults(func=execute)

def execute(args, parser):
    import re
    from datetime import datetime
    from .auth import github_handle

    gh = github_handle()
    try:
        user, repo = args.repo.split('/')
    except ValueError:
        parser.error('repo spec must contain single "/".')

    repo = gh.repository(user, repo)
    release = next(repo.iter_releases(number=1))
    print('Listing merged PRs since: %s\n' % release.name)

    for c in repo.iter_commits(since=release.created_at, until=datetime.now()):
        match = re.match('Merge pull request #(\d+)', c.commit.message)
        if match:
            number = int(match.group(1))
            lines = [e.strip() for e in c.commit.message.splitlines() if len(e.strip()) > 0]
            print('PR #%d: %s' % (number, lines[1]))


