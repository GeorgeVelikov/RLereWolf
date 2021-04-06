import PyInstaller.__main__

PyInstaller.__main__.run([
    'Server\\ServerInstance.py',
    '--onefile',

    '--add-data=Shared\\*;\\',
    '--add-data=Werewolf\\*;\\',
    '--add-data=Server\\*;\\',
    '--add-data=Client\\RLereWolf.png;\\',
])