"""Create json with information for custom_updater."""
from json import dumps
from github import Github
import customjson.defaults as ORG


class CreateJson():
    """Class for json creation."""

    def __init__(self, token, repo, push):
        """Initilalize."""
        self.token = token
        self.repo = repo
        self.push = push
        self.github = Github(token)

    def component(self):
        """Generate json for components."""
        org = 'custom-components'
        data = {}
        if self.repo is None:
            repos = []
            for repo in list(self.github.get_user(org).get_repos()):
                repos.append(repo.name)
            self.repo = repos
        for repo in self.repo:
            repo = self.github.get_repo(org + '/' + repo)
            if repo.name not in ORG.SKIP_REPOS and not repo.archived:
                print("Generating json for repo:", repo.name)
                name = repo.name
                updated_at = repo.updated_at.isoformat().split('T')[0]
                if len(name.split('.')) > 1:
                    location = 'custom_components/{}/{}.py'
                    location = location.format(name.split('.')[0],
                                               name.split('.')[1])
                else:
                    location = 'custom_components/{}.py'.format(name)
                    try:
                        repo.get_file_contents(location)
                    except Exception:
                        location = 'custom_components/{}/__init__.py'
                        location = location.format(name)

                version = None
                try:
                    content = repo.get_file_contents(location)
                    content = content.decoded_content.decode().split('\n')
                    for line in content:
                        if '_version_' in line or 'VERSION' in line:
                            version = line.split(' = ')[1]
                            break
                except Exception:
                    version = None

                try:
                    changelog = list(repo.get_releases())[0].html_url
                except Exception:
                    changelog = ORG.VISIT.format(org, name)

                updated_at = updated_at
                version = version
                local_location = '/{}'.format(location)
                remote_location = ORG.REUSE.format(org, name, location)
                visit_repo = ORG.VISIT.format(org, name)
                changelog = ORG.CHANGELOG.format(org, name)

                data[name] = {}
                data[name]['updated_at'] = updated_at
                data[name]['version'] = version
                data[name]['local_location'] = local_location
                data[name]['remote_location'] = remote_location
                data[name]['visit_repo'] = visit_repo
                data[name]['changelog'] = changelog
        if self.push:
            print("push it!")

        else:
            print(dumps(data, indent=4, sort_keys=True))

    def card(self):
        """Generate json for components."""
        print("Not implemented")
