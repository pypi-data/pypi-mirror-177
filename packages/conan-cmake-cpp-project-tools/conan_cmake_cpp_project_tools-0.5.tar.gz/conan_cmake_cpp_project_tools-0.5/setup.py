# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['conan_cmake_cpp_project_tools']

package_data = \
{'': ['*']}

install_requires = \
['fspathtree>=0.5,<0.6',
 'pyyaml>=6.0,<7.0',
 'rich>=12.6.0,<13.0.0',
 'typer>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['ccc = conan_cmake_cpp_project_tools.cli:app']}

setup_kwargs = {
    'name': 'conan-cmake-cpp-project-tools',
    'version': '0.5',
    'description': '',
    'long_description': '# Clark\'s Conan, CMake, C++ Project Tools\n\n**Note: this is a rewrite of a another project [https://github.com/CD3/cccpt](https://github.com/CD3/cccpt) and does not fully support Windows yet.**\n\nThis project started out as a collection of small scripts to automate the configure, build, and testing steps of\nC++ projects I work on. It has since grown to include several small utilities that I have found useful while\nworking on C++ projects.\n\n\n## Overview\n\nWhile CMake has its issues, and there are many that despise it, it is the de facto standard for building C++ projects.\nMost people\'s objections with CMake have to do with its home-grown scripting language. The command line interface\nis actually quite nice. Not only does it support multiple generators, but it abstracts away many of the differences\nbetween the generated build systems. For example, on Linux, you might do something like this:\n\n```\n$ mkdir build\n$ cd build\n$ cmake ..\n$ make\n```\n\nBut on Windows you might do:\n```\n$ mkdir build\n$ cd build\n$ cmake ..\n$ msbuild MyProject.vcxproj\n```\n\nBut with the `cmake --build` tool, you can do\n```\n$ mkdir build\n$ cd build\n$ cmake ..\n$ cmake --build .\n```\nThis works for Makefiles, Visual Studio Solutions, Ninja, etc.\nWhat\'s more, if you follow the normal conventions, these four lines should\nbuild any CMake project you create (things get more complicated if you need to\nsupport custom options, but you should still have a default build that will just work).\n\nI found that I was constantly running these commands, so I just put them into a script and eventually that morphed into\n`ccc`. I also do most of my development on Linux, but occasionally need to build projects on Windows (mostly for testing),\nso I wanted something I could run on either platform and have it "just work".\n\n## Usage\n\n### Installing\n\nYou can install `ccc` with pip.\n\n```\n$ pip install conan-cmake-cpp-project-tools\n```\n\nThis may be an out-of-date version. To use the latest version, clone this repository and install with pip\n```\n$ cd cccpt\n$ pip install .\n```\n\n### Requirements\n\n`ccc` expects several standard tools to be installed. It makes use of these tools wherever possible, rather\nthan re-implementing functionality. Current dependencies are:\n\n- Python (required)\n- CMake (required)\n- git (required)\n- Conan (optional)\n\nIf you don\'t use these tools, then `ccc` won\'t be useful.\n\n### Commands\n\nTo build a C++ project, run\n```\n$ ccc build\n```\nfrom anywhere in the project directory.\nThis will create a build directory in the project root\n(`git` is used to find the project root), install any dependencies specified in a `conanfile.txt` file,\nand configure and build (by default, Debug mode is built) the project.\n\nTo run the unit tests\n```\n$ ccc test\n```\nThis will automatically run the build step, so it possible to run this command on a fresh copy of the project.\nCurrently this command just looks for executables created in the build directory that match file name patterns\nI commonly use, so it may not work for you.\n\nTo build or test in Release mode, pass either command the `-R` option.\n\nTo get a list of all source files in the project\n```\n$ ccc list-sources\n```\nThis is useful for triggering the unit tests to run when a file changes with the `entr` command.\n```\n$ ccc list-sources | entr ccc test\n```\n\nTo install a project into a given root directory\n```\n$ ccc install /path/to/install/dir\n```\nThis will run `CMake` with the `-DCMAKE_INSTALL_PREFIX=/path/to/install/dir` option, build the project in release mode,\nand then run `cmake --build . --target install`.\n\nThere are many other commands that I find useful in my developement workflow. You may or may not find them useful. To get\na list of all commands, run\n```\n$ ccc --help\n```\n',
    'author': 'CD Clark III',
    'author_email': 'clifton.clark@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
