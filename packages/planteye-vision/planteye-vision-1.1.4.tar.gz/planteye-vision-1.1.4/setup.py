import setuptools
import codecs
import os.path


def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()


def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")


setuptools.setup(
    name='planteye-vision',
    version=get_version("src/planteye_vision/__init__.py"),
    packages=setuptools.find_packages(where="src"),
    package_dir={'': 'src'},
    url='',
    license='MIT',
    author='Valentin Khaydarov',
    author_email='valentin.khaydarov@gmail.com',
    description='PlantEye-Vision'
)
