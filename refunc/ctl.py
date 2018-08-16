# -*- coding: utf-8 -*-

import base64
import json
import os
import shutil
import re
import subprocess
import sys
import tarfile
from collections import defaultdict
from datetime import datetime
from io import BytesIO
from tarfile import TarInfo

import click
import refunc
import yaml
from jinja2 import Template
import oss2
from refunc import version as rf_version
from refunc import Context, Message, current_env, dotenv
from rfctllocal import version
from rfctllocal.util import gen_sh_util
from rfctllocal import dirtools


@click.group()
@click.option('--debug/--no-debug', default=True)
def cli(debug=False):
    if debug:
        from refunc.util import enable_logging

        env = current_env().new(pull_logs=True)
        refunc.push_env(env)
        enable_logging()


@cli.command(name="version")
def print_version():
    print('rfctl version:  {}'.format(version))
    print('refunc version: {}'.format(rf_version))


ID_PATTERN = re.compile('^([a-z0-9][-a-z0-9_.]*)?[a-z0-9]$')


def validate_id(ctx, param, value):
    try:
        ns, name = value.split('/', 2)
        if not ID_PATTERN.match(name):
            raise ValueError(
                "name must consist of alphanumeric characters, ' - ',"
                " '_' or '.', "
                "and must start and end with an alphanumeric character"
            )
        return (ns, name)
    except ValueError as e:
        raise click.BadParameter('be the form of "namespace/name", {}'.format(e))


VALID_TEMPLATES = ['python', 'tensorflow']

VALID_CATEGORY = ['text', 'voice', 'image']
REFUNC_ROOT = os.path.expanduser('~') + '/.refunc'  # os.environ['HOME'] + '/.refunc'

# config xevn prefix to template
xenvs2builders = {
    'python35': 'python',
    'python36': 'python',
    'python3': 'python',
    'py35-': 'python',
    'py36-': 'python',
    'tensorflow': 'python',
    'tensorflow-18': 'python',
}


@cli.command()
@click.option(
    '--id',
    'id',
    callback=validate_id,
    type=click.STRING,
    prompt='The id of the func(namespace/name)',
)
@click.option(
    '--zhname',
    'zhname',
    type=click.STRING,
    prompt='The chinese name of the func',
    default='',
)
@click.option(
    '--template',
    'template',
    type=click.Choice(VALID_TEMPLATES),
    prompt='Choose template:\n-  {}\n> '.format('\n-  '.join(VALID_TEMPLATES)),
    default='python',
)
@click.option(
    '--category',
    'cate',
    type=click.Choice(VALID_CATEGORY),
    prompt='Choose application category:\n-  {}\n> '.format(
        '\n-  '.join(VALID_CATEGORY)
    ),
    default='text',
)
@click.option(
    '--publish',
    'publish',
    prompt='Publish to ServMarket',
    type=click.BOOL,
    default=True,
)
@click.option('--target-dir', 'target_dir', default='', type=click.STRING)
@click.option(
    '--xenv',
    'xenvname',
    help="Override template's default runner",
    default='',
    type=click.STRING,
)
@click.option(
    '--init-git', 'git_init', prompt='Init git repo', type=click.BOOL, default=False
)
def new(
    id: str,
    zhname: str,
    template: str,
    cate: str,
    publish: bool,
    target_dir: str,
    xenvname: str,
    git_init: bool,
):
    refunc_new(id, zhname, template, cate, publish, target_dir, xenvname, git_init)


def refunc_new(
    id: str,
    zhname: str,
    template: str,
    cate: str,
    publish: bool,
    target_dir: str,
    xenvname: str,
    git_init: bool,
):
    '''
    create a new func in current folder
    '''
    ns, name = id
    if not template:
        raise ValueError('template name must be set')

    if not os.path.exists(os.path.join(REFUNC_ROOT, 'templates', template)):
        raise ValueError('no "{0}" template found in {1}'.format(template, REFUNC_ROOT))

    if not zhname:
        zhname = name

    dirctx = os.path.abspath(os.getcwd() if not target_dir else target_dir)
    dirname = to_camel_case(name)
    target = os.path.join(dirctx, dirname)
    if not xenvname:
        if template.startswith('tensorflow'):
            xenvname = 'tensorflow-18'
        else:
            xenvname = 'python36'

    if os.path.exists(target):
        click.secho(
            'folder with the name {} already exsits'.format(dirname), err=True, fg='red'
        )
        sys.exit(1)

    click.secho('Creating "{}" in {}'.format('/'.join(id), dirname), fg='green')

    # check xenv, raise error if not found
    builder_name = 'python'
    for k in xenvs2builders.keys():
        if xenvname.startswith(k):
            builder_name = xenvs2builders[k]

    # 设置函数服务图标路径，不含bucket-name
    iconpath = u'introduction/{0}/{1}/icon.png'.format(ns, name)
    click.secho('iconpath "{}"'.format(iconpath), fg='green')
    readmepath = u'introduction/{0}/{1}/README.md'.format(ns, name)
    click.secho('readmepath "{}"'.format(readmepath), fg='green')
    ctx = {
        'namespace': ns,
        'name': name,
        'zhname': zhname,
        'desc': '',
        'category': cate,
        'iconpath': iconpath,
        'readmepath': readmepath,
        'publish': publish,
        'xenvname': xenvname,
        'is_system': False,
        'builder': builder_name,
    }
    ctx['path'] = r'{namespace}/{name}'.format(**ctx)

    ##target为工作目录（实际使默认定位到工程目录）/函数名
    render_templates_local(template, ctx, target)
    # data = base64.b64encode(render_templates(template, ctx)).decode('utf-8')
    # fileobj = BytesIO(base64.decodebytes(data.encode('utf-8')))
    # os.makedirs(target)
    # with tarfile.open(mode='r:gz', fileobj=fileobj) as tar:
    #    tar.extractall(target)

    '''
    res = refunc.invoke(
        "refunc/builder",
        namespace=ns,
        name=name,
        template=template,
        xenvname=xenvname,
    )
    fileobj = BytesIO(base64.decodebytes(res['data'].encode('utf-8')))

    os.makedirs(target)
    with tarfile.open(mode='r:gz', fileobj=fileobj) as tar:
        tar.extractall(target)
    '''

    if git_init:
        sh = gen_sh_util(target)
        sh('git init')
        sh('git add -A')
        sh("git commit -a " "-m '[+] Initial commit of {}/{}'".format(*id))


@cli.command()
@click.argument(
    'target',
    default=os.getcwd(),
    type=click.Path(exists=True, dir_okay=True, resolve_path=True),
)
@click.option('--output', '-o', default='', type=click.Choice(['', 'yaml', 'json']))
@click.option(
    '--force',
    help='force apply func, ignore git repo checking',
    default=False,
    type=click.BOOL,
    is_flag=True,
    show_default=True,
)
def apply(target: str, output: str, force: bool):

    refunc_apply(target, output, force)


def refunc_apply(target: str, output: str, force: bool):
    '''
    update or create func under current dir context
    '''
    try:
        with open(os.path.join(target, 'refunc.yaml'), 'rb') as f:
            fndef_obj = yaml.safe_load(f)
    except FileNotFoundError:
        click.secho(
            'cannot find refunc.yaml, ' '"{}" is not a valid refunc ctx'.format(target),
            err=True,
            fg='red',
        )
        sys.exit(1)

    ns, name = fndef_obj['metadata']['namespace'], fndef_obj['metadata']['name']
    idpath = '/'.join([ns, name])

    # check if target in under a git repo
    sh = gen_sh_util(target, True)
    res = sh('git rev-parse --is-inside-work-tree')
    is_git_repo = res.returncode == 0 and res.stdout.strip() == 'true'

    if is_git_repo:
        if force:
            click.secho(
                '"{}" is under a git repo, ' 'but --force is supplied'.format(idpath),
                err=True,
                fg='yellow',
            )
        else:
            click.secho(
                '"{}" is under a git repo, checking'.format(idpath),
                err=True,
                fg='green',
            )
            if not check_git_repo(target):
                click.secho(
                    '\nPlz fix the issue above, and try again', err=True, fg='red'
                )
                sys.exit(1)

    click.secho('Packing "{}"'.format(idpath), fg='green')

    # load excludes
    excludes = ['.git/', '.hg/', '.svn/']
    if os.path.exists(os.path.join(target, '.gitignore')):
        excludes += dirtools.load_patterns(os.path.join(target, '.gitignore'))
    if os.path.exists(os.path.join(target, '.refuncignore')):
        excludes += dirtools.load_patterns(os.path.join(target, '.refuncignore'))

    # .env should not in scm, but is needed for builder
    while '.env' in excludes:
        excludes.remove('.env')
    files_filter = dirtools.Dir(directory=target, excludes=excludes)

    # create tarfile
    buf = BytesIO()
    with tarfile.open(mode='x:gz', fileobj=buf) as tar:
        tar.add(target, arcname='', exclude=files_filter.is_excluded)

    click.secho('Applying "{}"'.format(idpath), fg='green')
    res = refunc.invoke(
        'refunc/builder',
        method='apply',
        data=base64.encodebytes(buf.getvalue()).decode('utf-8'),
    )

    # 将函数服务图标上传至制定地址
    iconpath = ''
    envpath = ''
    readmepath = ''
    for root, dirs, files in os.walk(target, topdown=True):
        for filename in files:
            if filename.startswith("category_"):
                iconpath = os.path.join(target, filename)
                break

    for root, dirs, files in os.walk(target, topdown=True):
        for filename in files:
            if filename.upper() == 'README.MD':
                readmepath = os.path.join(target, filename)
                break

    for root, dirs, files in os.walk(REFUNC_ROOT, topdown=True):
        for filename in files:
            if filename.lower() == '.env':
                envpath = os.path.join(REFUNC_ROOT, filename)
                break

    if iconpath and readmepath and envpath:
        try:
            config = dotenv.dotenv_values(envpath)
            accessKeyId = config["AliyunAccessKeyId"]
            accessKeySecret = config["AliyunAccessKeySecret"]
            endpoint = config["AliyunEndpoint"]
            bucketName = config["AliyunBucketName"]
            auth = oss2.Auth(accessKeyId, accessKeySecret)
            bucketobj = oss2.Bucket(auth, endpoint, bucketName)
            # 上传icon
            osskey = u'introduction/{0}/{1}/icon.png'.format(ns, name)
            with open(iconpath, 'rb') as fileobj:
                bucketobj.put_object(osskey, fileobj)
                bucketobj.put_object_acl(osskey, oss2.OBJECT_ACL_PUBLIC_READ)
            # 上传deadme
            osskey = u'introduction/{0}/{1}/README.md'.format(ns, name)
            with open(readmepath, 'rb') as fileobj:
                bucketobj.put_object(osskey, fileobj)
                bucketobj.put_object_acl(osskey, oss2.OBJECT_ACL_PUBLIC_READ)
        except:
            pass
    else:
        click.secho('Applying iconpath/readmepath不存在', fg='green')

    if output == 'yaml':
        yaml.dump(res, sys.stdout)
    elif output == 'json':
        json.dump(res, sys.stdout, indent=2, sort_keys=True)
        sys.stdout.write('\n')
    else:
        click.secho('Done "{}"'.format(idpath), fg='green')
    return output


'''上传图片文件'''
'''
def applydata():
    # uploading plain content first
    ctx = current_env().context
    data_dir = 'data'
    ctx.put_object()
    for filename in file_list:
        with open(os.path.join(tmpdir, filename), 'r+b') as f:
            ctx.put_object(os.path.join(content_dir, filename), f)

    ctx.put_object(os.path.join(content_dir, '.checksum'), hash_val)
    ctx.put_object(os.path.join(content_dir, '.file_list.json'), json.dumps(file_list))

    if ctx.object_exists(objkey):
        ctx.log('funcdef with same checksum is already uploaded, skip building')
'''


@cli.command()
@click.argument(
    'target',
    default=os.getcwd(),
    type=click.Path(exists=True, dir_okay=True, resolve_path=True),
)
def upgrade(target: str):
    try:
        with open(os.path.join(target, 'refunc.yaml')) as f:
            old = yaml.safe_load(f)
    except FileNotFoundError:
        click.secho(
            'cannot find refunc.yaml, ' '"{}" is not a valid refunc ctx'.format(target),
            err=True,
            fg='red',
        )
        sys.exit(1)

    apiver = old['apiVersion']
    ns, name = old['metadata']['namespace'], old['metadata']['name']
    idpath = '/'.join([ns, name])

    if apiver == 'k8s.refunc.io/v1':
        click.secho('{} is already the latest version'.format(idpath), fg='green')
        return

    if apiver != 'refunc.v87.xyz/v1':
        click.secho('Unsupported object "{}"'.format(apiver), err=True, fg='red')
        sys.exit(1)

    new = {
        'apiVersion': 'k8s.refunc.io/v1',
        'kind': 'Funcdef',
        'metadata': old['metadata'],
        'spec': {'maxReplicas': 1, 'runtime': {'name': 'python35', 'timeout': 9}},
    }

    if 'annotations' in new['metadata']:
        anno = new['metadata']['annotations']
        if 'sys.refunc.v87.us/builder' in anno:
            anno['sys.funcs.refunc.io/builder'] = anno.pop('sys.refunc.v87.us/builder')

    if 'storePath' in old['spec'] and 'hash' in old['spec']:
        new['spec']['body'] = old['spec']['storePath']
        new['spec']['hash'] = old['spec']['hash']

    if 'entry' in old['spec']:
        new['spec']['entry'] = old['spec']['entry']

    if 'replicas' in old['spec']:
        new['spec']['maxReplicas'] = old['spec']['replicas']

    if 'meta' in old['spec']:
        new['spec']['meta'] = old['spec']['meta']

    if 'runner' in old['spec']:
        new['spec']['runtime'] = {'name': old['spec']['runner']['name']}
        if 'config' in old['spec']['runner']:
            cfg = old['spec']['runner']['config']
            if 'envs' in cfg:
                new['spec']['runtime']['envs'] = cfg['envs']
            if 'maxTimeout' in cfg:
                new['spec']['runtime']['timeout'] = cfg['maxTimeout']
            if 'systemFunc' in cfg:
                new['spec']['runtime']['systemFunc'] = cfg['systemFunc']

    with open(os.path.join(target, 'refunc.yaml'), 'w') as f:
        yaml.dump(new, f, default_flow_style=False)
        click.secho('{} upgraded to latest version'.format(idpath), fg='green')


@cli.command()
@click.argument('funcs', nargs=-1, type=click.STRING)
def logs(funcs: str):
    # merge topics
    topicmap = defaultdict(dict)
    for f in funcs:
        splitted = f.split('/')
        if len(splitted) != 2:
            click.secho('invalid endpoint: {}'.format(f), err=True, fg='red')
            sys.exit(1)
        ns, name = splitted
        # only set when current ns is not listed
        if '*' not in topicmap[ns]:
            topicmap[ns][name] = ns + "." + name

    funcs = []
    for ns in topicmap:
        funcs += [topicmap[ns][name] for name in topicmap[ns]]

    if not funcs:
        click.secho('func\'s endpoint is not set', err=True, fg='red')
        sys.exit(1)

    try:
        import asyncio
        from refunc.func_nats import nats_conn
        from refunc.util import start_or_get_running_loop, get_default_threadpool
    except ImportError:
        click.secho(
            'refunc version({}) is to low to support pull logs'.format(rf_version),
            err=True,
            fg='red',
        )
        sys.exit(1)

    loop = asyncio.get_event_loop()

    colors = ['green', 'blue', 'yellow', 'magenta', 'cyan']

    def color_picker():
        nonlocal colors
        color, colors = colors[0], colors[1:]
        colors.append(color)
        return color

    topic2color = defaultdict(color_picker)

    async def pull(msg):
        topic = '/'.join(msg.subject.split('.')[1:3])
        click.echo(
            click.style(
                '{}Z {}] '.format(datetime.utcnow().isoformat()[:-3], topic),
                fg=topic2color[topic],
            )
            + msg.data.decode(),
            sys.stderr,
        )

    async def sub():
        click.secho(
            'start pulling logs from "{!r}"'.format(funcs), err=True, fg='yellow'
        )
        # ensure nc
        nc, = await asyncio.gather(
            loop.run_in_executor(get_default_threadpool(), nats_conn)
        )
        for func in funcs:
            subject = 'refunc.' + func + '.logs.*'
            await nc.subscribe(subject, cb=pull)

    loop.create_task(sub())

    try:
        start_or_get_running_loop(loop=loop)
    except KeyboardInterrupt:
        click.secho('\r\npull logs from stopped', err=True, fg='yellow')


def check_git_repo(target: str) -> bool:
    _sh = gen_sh_util(target, True)

    def sh(cmd):
        res = _sh(cmd)
        return (
            res.returncode,
            ' '.join(res.stdout.split('\n')).strip(),
            ' '.join(res.stderr.split('\n')).strip(),
        )

    # check if current repo is clean
    code, stdout, stderr = sh(
        '''set -e
    git status --untracked-files=no --porcelain
    '''
    )
    if stdout:
        click.secho('repo is not clean, plz commit your changes:', err=True, fg='red')
        click.secho('\t' + stdout, err=True, fg='yellow')
        return False

    # check if current repo is clean
    code, stdout, stderr = sh(
        '''set -e
        git remote update >/dev/null
        LOCAL=$(git rev-parse @)
        REMOTE=$(git rev-parse @{u})
        BASE=$(git merge-base @ @{u})
        if [ $LOCAL = $REMOTE ]; then
            echo "up to date"
        elif [ $LOCAL = $BASE ]; then
            echo "using git to pull from remote"
        elif [ $REMOTE = $BASE ]; then
            echo "push push your local to remote"
        else
            echo "diverged"
        fi
    '''
    )
    if code != 0:
        click.secho('plz ensure your repo has a remote.\n' + stderr, err=True, fg='red')
        return False
    if stdout != 'up to date':
        click.secho(
            'your repo is outout sync with remote, you need:', err=True, fg='red'
        )
        click.secho('\t' + stdout, err=True, fg='yellow')
        return False

    return True


def to_camel_case(snake_str: str) -> str:
    # We capitalize the first letter of each component except the first one
    # with the 'title' method and join them together.
    return "".join(x.title() for x in snake_str.split('-'))


def render_templates_local(tpl_name, render_ctx, targetDir):
    '''
    将匹配模板中的yaml参数补齐，拷贝至目标目录
    :param tpl_name:
    :param render_ctx:
    :param targetDir:
    :return:
    '''
    category = render_ctx["category"]
    root = os.path.join(REFUNC_ROOT, 'templates', tpl_name, 'in')
    is_root, lr = True, len(root)
    for dir_name, _, file_list in os.walk(root):
        if is_root:
            is_root = False
            base = ''
        else:
            # create new dir
            base = dir_name[lr + 1 :] + '/'

        for name in file_list:
            filename = os.path.join(dir_name, name)
            # 创建模板地址
            targetBase = os.path.join(targetDir, base)
            targetFile = os.path.join(targetBase, name)
            if not os.path.exists(targetBase):
                os.makedirs(targetBase)
            # reunder template
            if name.startswith('_'):
                targetFile = os.path.join(targetBase, name[1:])
                shutil.copyfile(os.path.join(dir_name, name), targetFile)
                with open(filename, encoding="utf-8") as f:
                    rendered = Template(f.read(), keep_trailing_newline=True).render(
                        **render_ctx
                    )
                with open(targetFile, 'w', encoding="utf-8") as f:
                    f.write(rendered)
            else:
                if name.startswith("category_"):
                    if name == "category_{0}.png".format(category):
                        shutil.copyfile(os.path.join(dir_name, name), targetFile)
                else:
                    shutil.copyfile(os.path.join(dir_name, name), targetFile)


def render_templates(tpl_name, render_ctx):
    category = render_ctx["category"]
    buf = BytesIO()
    with tarfile.open(mode='x:gz', fileobj=buf) as tar:
        root = os.path.join(REFUNC_ROOT, 'templates', tpl_name, 'in')
        is_root, lr = True, len(root)
        for dir_name, _, file_list in os.walk(root):
            if is_root:
                is_root = False
                base = ''
            else:
                # create new dir
                base = dir_name[lr + 1 :] + '/'
                tar.add(dir_name, base, recursive=False)

            for name in file_list:
                filename = os.path.join(dir_name, name)
                # reunder template
                if name.startswith('_'):
                    with open(filename) as f:
                        rendered = Template(
                            f.read(), keep_trailing_newline=True
                        ).render(**render_ctx)
                        ti = TarInfo(name=base + name[1:])
                        ti.size = len(rendered)
                        tar.addfile(ti, BytesIO(rendered.encode('utf-8')))
                else:
                    if name.startswith("category_"):
                        if name == "category_{0}.png".format(category):
                            tar.add(filename, base + name, recursive=False)
                    else:
                        tar.add(filename, base + name, recursive=False)
    return buf.getvalue()


if __name__ == '__main__':
    # string1 = '����'
    # string2 = string1.encode('ANSI')
    # string3 = str(string2, 'utf-8')

    # cli()
    # new('nstest/nametest', 'tensorflow', 'text', True, '', 'tensorflow-18', False)
    # .m('','','',True,'','',False)
    new.main(
        [
            '--id',
            'ci-test/weibo2',
            '--zhname',
            '中文',
            '--template',
            'python',
            '--category',
            'text',
            '--publish',
            'True',
            '--init-git',
            'False',
        ]
    )
    ##apply.main(['--target', './Zzz'])# target应为option
    # apply.main(['./Zzz'])

