import PyInstaller.__main__

PyInstaller.__main__.run([
    'Client\\ClientInstance.py',
    '--onefile',

    '--add-data=Shared\\*;.',
    '--add-data=Werewolf\\*;.',
    '--add-data=Client\\RLereWolf.png;.',
    '--add-data=Client\\views;.',

    '--hidden-import=pygubu',
])