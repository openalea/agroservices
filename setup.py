# -*- python -*-
#
#       Copyright INRIA - CIRAD - INRA
#
#       File author(s):
#
#       File contributor(s):
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.rtfd.io
#
# ==============================================================================
"""
"""
# ==============================================================================
from setuptools import setup, find_packages, Extension, Command
# ==============================================================================

pkg_root_dir = 'src'
packages = find_packages(pkg_root_dir)
top_pkgs = [pkg for pkg in packages if len(pkg.split('.')) <= 2]
package_dir = dict([('', pkg_root_dir)] +
                   [(pkg, pkg_root_dir + "/" + pkg.replace('.', '/'))
                    for pkg in top_pkgs])

name = "agroservices"

version = {}
with open("src/agroservices/__init__.py") as fp:
    exec(fp.read(), version)

description = ''
long_description = '''
AgroService is a Python package that provides access 
to IPM Web Services (at least) and a framework to 
easily implement Web Services wrappers. 
This package is intended to be close to the webservice. 
Therefore the requests will have the same API that each web service. 
'''
author= 'Christian Fournier, Marc Labadie, Christophe Pradal'
url='https://github.com/H2020-IPM-openalea/agroservices'
license="GPL-v3"

setup(
    name=name,
    version=version,
    description=description,
    long_description=long_description,

    author=author,

    url=url,
    license=license,
    keywords='openalea, web services, DSS',

    # package installation
    packages=packages,
    package_dir=package_dir,
    zip_safe=False,

    # See MANIFEST.in
    include_package_data=True,
    )
