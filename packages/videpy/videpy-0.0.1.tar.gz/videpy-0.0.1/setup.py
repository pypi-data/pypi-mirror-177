from setuptools import setup

with open('videpy/README.md', 'r') as arq:
    readme = arq.read()

setup(
    name='videpy',
    version='0.0.1',
    license='MIT License',
    author='Rodolpho Macedo dos Santos',
    long_description=readme,
    long_description_content_type='text/markdown',
    author_email='rodolpho.ime@gmail.com',
    keywords=['videpy', 'vide', 'bayesian', 'stan', 'pystan', 'rethinking'],
    description=u'Tools to handle samples posteriori from Stan (pystan)',
    packages=['videpy'],
    install_requiments=['numpy', 'pandas', 'matplotlib'],
)
