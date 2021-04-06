from Shared.utility.Helpers import nameof;

from Client.screens.ScreenBase import ScreenBase;

import tkinter as tk;

class ErrorDialog(ScreenBase):
    def __init__(self, root, context, error):
        super().__init__(root, context);

        self.InitializeScreen();
