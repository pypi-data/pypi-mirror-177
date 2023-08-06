# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vim_quest_cli',
 'vim_quest_cli.corpus',
 'vim_quest_cli.deps',
 'vim_quest_cli.deps.ansi',
 'vim_quest_cli.deps.ansi.colour',
 'vim_quest_cli.deps.prompt_toolkit',
 'vim_quest_cli.engine',
 'vim_quest_cli.engine.pure_python',
 'vim_quest_cli.engine.vim_exe',
 'vim_quest_cli.engine.vim_exe.resources',
 'vim_quest_cli.interface',
 'vim_quest_cli.mode',
 'vim_quest_cli.old',
 'vim_quest_cli.view']

package_data = \
{'': ['*']}

install_requires = \
['ansi>=0.3.6,<0.4.0', 'argparse-dataclass>=0.2.1,<0.3.0']

entry_points = \
{'console_scripts': ['main = vim_quest_cli.__main__:main',
                     'stdin_test = vim_quest_cli.deps.test_stdin:main']}

setup_kwargs = {
    'name': 'vim-quest-cli',
    'version': '0.1.13',
    'description': '',
    'long_description': '# VimQuestCLI\n\nThis is a vim implementation in python that tries to implement game using the vim shortcuts.\n\n## Why python ?\n\nI love python. Maybe one day it\'s going to be converted in Rust (for easy webassembly and faster execution). But for now it\'s python 3.8.\n\n## Choice when doing executions\n\nExecutor :\n- local (the python vim implementation)\n- vim (calling vim to execute stuff, for compatibility tests)\n\nTerminal handling :\n- Curses wrapper : the way it\'s usually done in python.\n  It allows for curses to catch the input.\n- "manual" curses : Without using the full curses capabilities.\n\nExecution loop :\n- One method to start the whole loop.\n- One method that have the input as argument and returns what to print.\n\nThe python version doesn\'t have just vim capabilities, but allows to expand for allowing for hooks and data attached to the cells.\n\n## Todo\n\n- Separate presentation layer\n\n- Add a vim executor (to be able to compare tests).\n- Have a context that is not a copy but modify itself (for speed).\n- Have a bunch of hooks, and use them to have game modes.\n- Have a command to choose between game modes.\n- See how neovim is made so I can use the same architecture.\n- Maybe have syntax highliting for game modes too ?\n- Activate the UTF-8, see how I can activate it.\n- Create docker images for website and terminal.\n- Add git hook for cleaning python before commit.\n- Use unicode characters (not necesseraly emojii) with colors for differents things happening.\n\nBUG CORRECTION :\n- Clean codebase.\n- ANSI is blinking.\n- Image location is not working.\n- Size of the terminal is not used.\n- Unicode block behavior is inconsistent.\n  - Maybe having replacement for unicode that include colors.\n\n# References\n\n- [vim-adventures.com](https://vim-adventures.com/) : really cool game. I keep paying for it as the licence is only for 6 months.\n- [vim.so](https://www.vim.so/lessons) : Manual tests using a modified javascript editor.\n- [vimgenius.com](http://www.vimgenius.com/lessons/vim-intro/levels/level-1)\n- [github.com/iggredible/Learn-Vim](https://github.com/iggredible/Learn-Vim/blob/master)\n\n- Python prompt toolking has a python implementation of vi commands :\n  - https://github.com/prompt-toolkit/python-prompt-toolkit/blob/master/src/prompt_toolkit/key_binding/bindings/vi.py\n\nNow vim implementationthat I could use for corectness :\n- ace js : https://github.com/ajaxorg/ace/blob/master/src/keyboard/vim_test.js\n- ideavim : https://github.com/JetBrains/ideavim/tree/master/src/test/java/org/jetbrains/plugins/ideavim\n\nncurses implementation : https://github.com/mscdex/node-ncurses\nMaybe this implementation would be easier to understand than the c ncurses one.\n# Next steps to cover\n\n- hjkl x\n- [number]command\n- i\n- aA\n- dd\n- wbe\n- v, Shift-v\n- ypP\n- "ci<symbol>"\n\n\n# Next step.\n\nVim core. That execute the commands and return a status. From a Contains the screen size and \n\nVim window. That take that buffer and return a screen. (matrix of data points with metadata).\n\nAttachable are game modes.\n\nThen there is terminal that push characters and returns a  \n\nUse an alternate screen : https://stackoverflow.com/questions/11023929/using-the-alternate-screen-in-a-bash-script\n\n',
    'author': 'Stolati',
    'author_email': 'stolati@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
