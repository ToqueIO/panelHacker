import re
import traceback
import keyPressEventManager

from panels import basePanel
from panels.preferences.scriptEditor import ColorPreference
from globals import Globals
from highlighters import syntaxPython
from PySide2 import QtGui, QtWidgets


class ScriptEditor(basePanel.BasePanel):

    requiredAttributes = ['textEditor']

    def __init__(self, panel, hackerParent=None):
        super(ScriptEditor, self).__init__(panel, hackerParent=hackerParent)

        self.panel = panel

        self.initialized = False
        self.highlighter = None
        self._textEditor = None
        self._outputWindow = None
        self._splitter = None
        self._buttons = None

        self.eventFilter = keyPressEventManager.KeyPressEventManager()

    def initialize(self):
        """
        Initializes the panel and sets up the event filter for the panel, so we can override some
        of the default nuke shortcuts for the script editor.

        Shortcut List:
            - Ctrl+V: Paste with normalization of spaces
            - Ctrl+Shift+V: Paste without normalization of spaces
            - Ctrl+/ : Toggle comment on selected text
        """
        if self.initialized:
            return

        self.highlighter = syntaxPython.PythonHighlighter(self.textEditor)
        self.textEditor.installEventFilter(self.eventFilter)
        self.eventFilter.registerSequence('Ctrl+V', self.paste)
        # Currently this is not working due to how nuke handles keyboard shortcuts at a global level
        # self.eventFilter.registerSequence('Ctrl+S',
        #                                   lambda: self.saveScriptButton.click())
        self.eventFilter.registerSequence('Ctrl+Shift+V',
                                          self.paste,
                                          **{'normalizeSpace': True})
        # Currently this is not working due to how nuke handles keyboard shortcuts at a global level
        # self.eventFilter.registerSequence('Ctrl+W', self.expandSelection)
        self.eventFilter.registerSequence('Ctrl+/', self.toggleComment)

        for preference in Globals.preferences.values():
            self.updatePreferences(preference)

        self.initialized = True

    def updatePreferences(self, preference):
        """
        Before doing any updates this will ensure that the preference is a ColorPreference object
        afterward this will update the preferences for the script editor
        Args:
            preference (dict, ColorPreference):  The preference that will be used for the update
        """
        if isinstance(preference, dict):
            preference = ColorPreference(**preference)
        super(ScriptEditor, self).updatePreferences(preference)

    @property
    def panelType(self):
        """
        Returns:
            str: The type of panel as defined in the globals
        """
        return Globals.scriptEditorType

    @property
    def splitter(self):
        """
        Returns:
            QtWidgets.QSplitter: The splitter that separates the script editor from the output
        """
        if self._splitter is None:
            for child in self.panel.children():
                if isinstance(child, QtWidgets.QSplitter):
                    self._splitter = child

        return self._splitter
        
    @property
    def textEditor(self):
        """
        Returns:
            QtWidgets.QPlainTextEdit: The text editor that is used for the script editor
        """
        if self._textEditor is None:
            for child in self.splitter.children():
                if isinstance(child, QtWidgets.QPlainTextEdit):
                    self._textEditor = child

        return self._textEditor

    @property
    def previousScriptButton(self):
        """
        Returns:
            QtWidgets.QPushButton: The button that will load the previous script
        """
        return self.buttons.get('previousScript')

    @property
    def nextScriptButton(self):
        """
        Returns:
            QtWidgets.QPushButton: The button that will load the next script
        """
        return self.buttons.get('nextScript')

    @property
    def clearHistoryButton(self):
        """
        Returns:
            QtWidgets.QPushButton: The button that will clear the history of the script editor
        """

        return self.buttons.get('clearHistory')

    @property
    def sourceScriptButton(self):
        """
        Returns:
            QtWidgets.QPushButton: The button that will source a script
        """
        return self.buttons.get('sourceScript')

    @property
    def loadScriptButton(self):
        """
        Returns:
            QtWidgets.QPushButton: The button that will load a script
        """
        return self.buttons.get('loadScript')

    @property
    def saveScriptButton(self):
        """
        Returns:
            QtWidgets.QPushButton: The button that will save a script
        """
        return self.buttons.get('saveScript')

    @property
    def runScriptButton(self):
        """
        Returns:
            QtWidgets.QPushButton: The button that will run the current script
        """
        return self.buttons.get('runScript')

    @property
    def showInputButton(self):
        """
        Returns:
            QtWidgets.QPushButton: The button that will show the input only
        """
        return self.buttons.get('showInput')

    @property
    def showOutputButton(self):
        """
        Returns:
            QtWidgets.QPushButton: The button that will show the output only
        """
        return self.buttons.get('showOutput')

    @property
    def showAllButton(self):
        """
        Returns:
            QtWidgets.QPushButton: The button that will show both input and output
        """
        return self.buttons.get('showAll')

    @property
    def clearButton(self):
        """
        Returns:
            QtWidgets.QPushButton: The button that will clear the output window
        """
        return self.buttons.get('clear')

    @property
    def buttons(self):
        """
        Returns:
            dict: Dictionary of all the buttons that are available in the script editor
        """

        if self._buttons is None:
            self._buttons = dict()
            for widget in self.panel.children():
                if isinstance(widget, QtWidgets.QPushButton):
                    toolTip = widget.toolTip()
                    if not toolTip:
                        continue

                    if 'Previous script' in toolTip:
                        self._buttons['previousScript'] = widget
                        continue
                    elif 'Next script' in toolTip:
                        self._buttons['nextScript'] = widget
                        continue
                    elif 'Clear history' in toolTip:
                        self._buttons['clearHistory'] = widget
                        continue
                    elif 'Source a script' in toolTip:
                        self._buttons['sourceScript'] = widget
                        continue
                    elif 'Load a script' in toolTip:
                        self._buttons['loadScript'] = widget
                        continue
                    elif 'Save a script' in toolTip:
                        self._buttons['saveScript'] = widget
                        continue
                    elif 'Run the current script' in toolTip:
                        self._buttons['runScript'] = widget
                        continue
                    elif 'Show input only' in toolTip:
                        self._buttons['showInput'] = widget
                        continue
                    elif 'Show output only' in toolTip:
                        self._buttons['showOutput'] = widget
                        continue
                    elif 'Show both input and output' in toolTip:
                        self._buttons['showAll'] = widget
                        continue
                    elif 'Clear output window' in toolTip:
                        self._buttons['clear'] = widget
                        continue

        return self._buttons

    @staticmethod
    def normalizeSpaces(text):
        """
        This will normalize the spaces in the given text by removing the smallest amount of spaces
        Args:
            text (str): The text that will have the spaces normalized

        Returns:
            str: The text with the spaces normalized
        """
        lines = text.split('\n')
        smallSpace = None

        for line in lines:
            spaceSearch = re.search('(\s+).*', line)
            if spaceSearch:
                space = len(spaceSearch.groups()[0])
                if not smallSpace:
                    smallSpace = space
                else:
                    if space:
                        smallSpace = min([smallSpace, space])

        if smallSpace:
            lines = [line[smallSpace:] for line in lines]

        return '\n'.join(lines)

    def paste(self, **kwargs):
        """
        This will paste the text from the clipboard into the text editor and format it as needed.
        This is primarily useful for pasting code from other sources into the script editor since
        they may not have the same formatting as the script editor

        Kwargs:
            normalizeSpace (bool):  If True then the spaces will be normalized before pasting

        Returns:
            bool: True if the paste was successful, False if it was not
        """
        normalizeSpace = kwargs.get('normalizeSpace', False)
        clipboard = QtGui.QClipboard()
        currentText = ''
        try:
            currentText = str(clipboard.mimeData().text())
        except Exception:
            traceback.print_exception()

        if not currentText:
            return False

        if normalizeSpace:
            currentText = self.normalizeSpaces(currentText)

        self.textEditor.insertPlainText(currentText)
        self.textEditor.ensureCursorVisible()

        return True

    def expandSelection(self):

        # Currently shortcuts are not working completely with the current context due to how nuke
        # is handling keyboard shortcuts.  This will need to be revisited in the future
        return

    def toggleComment(self):
        """
        This will toggle the comment on the selected text.  If the text is already commented then
        the comment will be removed, if the text is not commented then the comment will be added

        any blank lines will be ignored
        """
        cursor = self.textEditor.textCursor()

        # Get selection stats
        selectionStart = cursor.selectionStart()
        selectionEnd = cursor.selectionEnd()

        # Get selection split to lines
        singleLine = selectionStart == selectionEnd
        if singleLine:
            selectedText = cursor.block().text()
        else:
            cursor.movePosition(cursor.StartOfLine, cursor.KeepAnchor)
            selectedText = cursor.selectedText()

        selectedLines = selectedText.splitlines(keepends=True)
        comment = any([re.sub('\s+', '', line).startswith('#') for line in selectedText.splitlines()])

        if comment:
            newLines = [line.replace('# ', '', 1) for line in selectedLines]
            modifier = -1
        else:
            newLines = [f'# {line}' if line else line for line in selectedLines]
            modifier = 1

        newText = ''.join(newLines)
        addition = (selectedText.count('# ') if comment else newText.count('# ')) * 2

        # Replace text
        if singleLine:
            cursor.select(QtGui.QTextCursor.BlockUnderCursor)
            cursor.insertText(f'\n{newText}')
            cursor.setPosition(selectionStart + (2*modifier))
        else:
            cursor.insertText(newText)
            cursor.setPosition(selectionStart)
            cursor.setPosition(selectionEnd + addition*modifier,
                               QtGui.QTextCursor.KeepAnchor)

        self.textEditor.setTextCursor(cursor)

        return

    @classmethod
    def regex(cls):
        """
        Returns:
            str: The regex that will be used to find the nuke panel that we want to interact with
        """
        return str('.*scripteditor\.\d+')
