import subprocess

class PopenAdapter:
    def __init__(self, stdout, stderr, retcode):
        self.stdout = stdout
        self.stderr = stderr
        self.returncode = retcode

def run(*args, **kwargs):
    p = subprocess.Popen(*args, **kwargs)
    out, err = p.communicate()
    return PopenAdapter(out, err, p.returncode)