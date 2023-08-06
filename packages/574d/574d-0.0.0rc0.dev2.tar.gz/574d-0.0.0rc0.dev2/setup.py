# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['WM', 'WM.TK', 'WM.Win32']

package_data = \
{'': ['*'], 'WM': ['images/*']}

setup_kwargs = {
    'name': '574d',
    'version': '0.0.0rc0.dev2',
    'description': 'A Window Manager for Tkinter On Windows 10',
    'long_description': "# WM\nA Window Manager for Tkinter On Windows 10\n\n[Video Test](https://user-images.githubusercontent.com/73524758/200260996-18de1043-4b5f-4f9c-b3ee-6e27d1903594.mp4)\n* [WM/Wiki](https://github.com/XxFULLDLCxX/WM/wiki)\n\n## How to install\n```Bash\npip install 574d\n```\n\n## How to test\n> ```Python\n> from WM import TK\n>\n> ...\n>\n> if __name__ == '__main__':\n>     Tk = TK()\n>     Tk.mainloop()\n> ```\n\nI developed a code pattern based on the Sword Art Online (SAO) for Tkinter\n\n###  For Example:\n\n**`System Call Generate`** `Button` **`Element`** `<Object-ID>` _`Discharge`_ !\n\n_Discharge_ is only a SAO reference.\n\n[`./WM/core.py`](./WM/core.py)\n> ```Python\n> class Call(TkData, INHERIT):  # Object-IDs are here.\n>     ...\n>     szTitle, szWindowClass = 'WM', 'WM'\n>     ...\n>\n> class System(Call):  # class TK(System, Call.Tk): \n>     Call = Call  # System.Call\n>     ...\n> ```\n\n [`./WM/views.py`](./WM/views.py)\n> ```python\n> class Element(E.Widget, E.PhotoImage, System, Call):  # type: ignore\n>     def __new__(cls, name: str = '', *_: E.Any, generic: bool = False, **__: E.Any):\n>         E = GENERATE.__dict__[name](*_, **__)\n>         if generic:\n>             del E._[-1]\n>         return E\n>\n>\n> class Generate(System, Call):\n>     def __init__(self):\n>         super(System, self).__init__()  # info when called\n>         ...\n>         # with Element Constructor\n>         Element('Frame', self.TK).grid(0, 0, 'nsew', padx=1, pady=1)({0: (1, 1), 1: (0, 1), 2: (1, 0)}).grid_remove()\n>         self.W['F'][-1].grid()\n>         # another way to do the same\n>         my_frame = ttk.Frame(self.TK)\n>         my_frame.grid(row=0, column=0, sticky='nsew', padx=1, pady=1)\n>         my_frame.grid_rowconfigure(0, weight=1)\n>         my_frame.grid_rowconfigure(2, weight=1)\n>         my_frame.grid_columnconfigure(0, weight=1)\n>         my_frame.grid_columnconfigure(1, weight=1)\n>         my_frame.grid_remove()\n>         my_frame.grid()\n> ```\n\n\n\n\n",
    'author': 'XxFULLDLCxX',
    'author_email': 'XxFULLDLCxX@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
