from setuptools import setup, find_packages

version = '0.1'
readme = open("README.txt").read()

setup(name = 'plone.app.blob',
      version = version,
      description = 'ZODB 3.8 blob support for Plone 3.x',
      long_description = readme[readme.find('Overview'):],
      classifiers = [
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Plone',
        'Framework :: Zope2',
        'Framework :: Zope3',
        'Intended Audience :: Other Audience',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
      ],
      keywords = 'zodb blob support plone',
      author = 'Andreas Zeidler - Plone Foundation',
      author_email = 'plone-developers@lists.sourceforge.net',
      url = 'http://svn.plone.org/svn/plone/plone.app.blob/',
      download_url = 'http://cheeseshop.python.org/pypi/plone.app.linkintegrity/',
      license = 'GPL',
      packages = find_packages(),
      namespace_packages = ['plone.app'],
      include_package_data = True,
      platforms = 'Any',
      zip_safe = False,
      install_requires=[
          'setuptools',
          'ZODB3 >=3.8.0b2,<3.8.999',
          'zope.interface >=3.3,<3.3.999',
          'zope.testing >=3.0,<3.3.999',
          'ZConfig >=2.4a2,<2.4.999',
          'zdaemon >=1.4a2,<1.4.999',
          'zope.proxy >=3.4,<3.4.999',
          'zodbcode >=3.4,<3.4.999',
          'archetypes.schemaextender >=1.0a1',
      ],
)

