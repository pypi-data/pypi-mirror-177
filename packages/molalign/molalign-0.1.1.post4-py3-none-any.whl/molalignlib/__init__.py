try:
    from .molalignlib import Alignment
except ModuleNotFoundError:
    from os import path, environ
    from shutil import copyfile
    from subprocess import Popen, PIPE, STDOUT
    pkgdir = path.dirname(__file__)
    command = [path.join(pkgdir, 'build.sh'), '-lpy']
    sub_env = environ.copy()
    sub_env['DESTDIR'] = pkgdir
    try:
        copyfile(path.join(pkgdir, 'config', 'gnu.cfg'), path.join(pkgdir, 'build.cfg'))
    except FileExistsError:
        pass
    with Popen(command, env=sub_env, stdout=PIPE, stderr=STDOUT, bufsize=0) as p:
        for line in p.stdout:
            print(line.decode('utf-8').rstrip())
