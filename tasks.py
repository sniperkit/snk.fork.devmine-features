from invoke import (
    task,
    run
)

# define projects directories
dirs = 'parsing'


@task
def pep8():
    cmd = 'pep8 tasks.py ' + dirs
    run_cmd(cmd)


@task
def pyflakes():
    cmd = 'pyflakes tasks.py ' + dirs
    run_cmd(cmd)


@task('pep8', 'pyflakes')
def check():
    pass


@task
def clean():
    run_cmd("find . -name '__pycache__' -exec rm -rf {} +")
    run_cmd("find . -name '*.pyc' -exec rm -f {} +")
    run_cmd("find . -name '*.pyo' -exec rm -f {} +")
    run_cmd("find . -name '*~' -exec rm -f {} +")
    run_cmd("find . -name '._*' -exec rm -f {} +")


@task('clean')
def clean_env():
    run_cmd('rm -r ./env && mkdir env && touch env/.keep')


@task
def compute_login_id(input='dataset/raw/users.bson', output='dataset/id.txt'):
    get_fields_bson("login id", input, output)

@task
def compute_location(input='dataset/raw/users.bson', output='dataset/id.txt'):
    #get_fields_bson("login location", input, output)
    # TODO
    pass


@task
def compute_followers(input='dataset/raw/users.bson',
                      output='dataset/followers.txt'):
    get_fields_bson("login followers", input, output)

@task
def compute_date_joined_github(input='dataset/raw/users.bson',
                     output='dataset/date_joined_github.txt'):
    get_fields_bson("login created_at", input, output)

@task
def compute_last_active(input='dataset/raw/users.bson',
                     output='dataset/last_active.txt'):
    get_fields_bson("login updated_at", input, output)


@task
def compute_hireable(input='dataset/raw/users.bson',
                     output='dataset/hireable.txt'):
    get_fields_bson("login hireable", input, output)

@task
def precompute_issues_detected(input='dataset/raw/issues.bson',
                         output='dataset/issues_detected.txt'):
    get_fields_bson("user/login", input, output)

@task
def compute_issues_detected(input='dataset/raw/issues.bson',
                         output='dataset/issues_detected'):
    precompute_issues_detected(input, output + '.txt')
    run_cmd('python parsing/issues_detected.py %s.txt %s' %(output, output))
    
@task
def precompute_issues_solved(input='dataset/raw/issues.bson',
                         output='dataset/issues_solved.txt'):
    get_fields_bson("state assignee/login", input, output)

@task
def compute_issues_solved(input='dataset/raw/issues.bson',
                         output='dataset/issues_solved'):
    precompute_issues_solved(input, output + '.txt')
    run_cmd('python parsing/issues_solved.py %s.txt %s' %(output, output))

@task
def precompute_languages(input='dataset/raw/repos.bson',
                         output='dataset/languages.txt'):
    get_fields_bson("owner/login language size", input, output)


@task
def compute_languages(input='dataset/raw/repos.bson',
                      output='dataset/languages'):
    precompute_languages(input, output + '.txt')
    run_cmd('python parsing/languages.py \
    dataset/languages.txt dataset/languages')


@task('compute_login_id', 'compute_followers', 'compute_languages')
def compute_all():
    pass


def run_cmd(cmd):
    "Run a system command verbosely."
    print('Running \'' + cmd + '\'...')
    run(cmd)
    print('Done')


def get_fields_bson(fields, input, output, has_null=False):
    run_cmd('bsondump %s | python parsing/get_fields.py %s > %s 2> /dev/null' % (input, fields, output))
