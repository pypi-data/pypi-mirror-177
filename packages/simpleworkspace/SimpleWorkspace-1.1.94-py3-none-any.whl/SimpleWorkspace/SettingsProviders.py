from __future__ import annotations as _annotations
from abc import ABC, abstractmethod
from SimpleWorkspace.Utility import Console as _ConsoleUtility
import os as _os
import json as _json
import SimpleWorkspace as _sw

class SettingsManager_Base(ABC):
    _settingsPath = None
    settings = {}

    def __init__(self, settingsPath):
        self._settingsPath = settingsPath
        self.settings = self._GetDefaultSettings()

    def _GetDefaultSettings(self):
        return {}

    @abstractmethod
    def _ParseSettingsFile(filepath):
        pass
    @abstractmethod
    def _ExportSettingsFile(settingsObject, outputPath):
        pass

    def ClearSettings(self):
        self.settings = self._GetDefaultSettings()

    def LoadSettings(self):
        self.ClearSettings()
        if not (_os.path.exists(self._settingsPath)):
            return
        if _os.path.getsize(self._settingsPath) == 0:
            return
        try:
            self._ParseSettingsFile(self._settingsPath)
        except Exception as e:
            _os.rename(self._settingsPath, self._settingsPath + ".bak")
        return self.settings

    def SaveSettings(self):
        self._ExportSettingsFile(self.settings, self._settingsPath)


class SettingsManager_JSON(SettingsManager_Base):
    def _ParseSettingsFile(self, filepath):
        self.settings = _json.loads(_sw.IO.File.Read(filepath))
        return

    def _ExportSettingsFile(self, settingsObject, outputPath):
        jsonData = _json.dumps(settingsObject)
        _sw.IO.File.Create(outputPath, jsonData)
        return



class SettingsManager_InteractiveConsole(SettingsManager_JSON):
    __Command_Delete = "#delete"

    def __Console_ChangeSettings(self):
        while True:
            _ConsoleUtility.ClearConsoleWindow()
            _ConsoleUtility.LevelPrint(0, "[Change Settings]")
            _ConsoleUtility.LevelPrint(1, "0. Save Settings and go back.(Type cancel to discard changes)")
            _ConsoleUtility.LevelPrint(1, "1. Add a new setting")
            _ConsoleUtility.LevelPrint(2, "[Current Settings]")
            dictlist = []
            dictlist_start = 2
            dictlist_count = 2
            for key in self.settings:
                _ConsoleUtility.LevelPrint(3, str(dictlist_count) + ". " + key + " : " + str(self.settings[key]))
                dictlist.append(key)
                dictlist_count += 1
            _ConsoleUtility.LevelPrint(1)
            choice = input("-Choice: ")
            if choice == "cancel":
                self.LoadSettings()
                _ConsoleUtility.AnyKeyDialog("Discarded changes!")
                break
            if choice == "0":
                self.SaveSettings()
                _ConsoleUtility.LevelPrint(1)
                _ConsoleUtility.AnyKeyDialog("Saved Settings!")
                break
            elif choice == "1":
                _ConsoleUtility.LevelPrint(1, "Setting Name:")
                keyChoice = _ConsoleUtility.LevelInput(1, "-")
                _ConsoleUtility.LevelPrint(1, "Setting Value")
                valueChoice = _ConsoleUtility.LevelInput(1, "-")
                self.settings[keyChoice] = valueChoice
            else:
                IntChoice = None
                try:
                    IntChoice = int(choice)
                except Exception as e:
                    pass
                if IntChoice == None or (IntChoice >= dictlist_start and IntChoice < dictlist_count):
                    continue
                else:
                    key = dictlist[IntChoice - dictlist_start]
                    _ConsoleUtility.LevelPrint(2, '(Leave empty to cancel, or type "' + self.__Command_Delete + '" to remove setting)')
                    _ConsoleUtility.LevelPrint(2, ">> " + str(self.settings[key]))
                    choice = _ConsoleUtility.LevelInput(2, "Enter new value: ")
                    if choice == "":
                        continue
                    elif choice == self.__Command_Delete:
                        del self.settings[key]
                    else:
                        self.settings[key] = choice
        return

    def Console_PrintSettingsMenu(self):
        while(True):
            _ConsoleUtility.ClearConsoleWindow()
            _ConsoleUtility.LevelPrint(0, "[Settings Menu]")
            _ConsoleUtility.LevelPrint(1, "1.Change settings")
            _ConsoleUtility.LevelPrint(1, "2.Reset settings")
            _ConsoleUtility.LevelPrint(1, "3.Open Settings Directory")
            _ConsoleUtility.LevelPrint(1, "0.Go back")
            _ConsoleUtility.LevelPrint(1)
            choice = input("-")
            if choice == "1":
                self.__Console_ChangeSettings()
            elif choice == "2":
                _ConsoleUtility.LevelPrint(1, "-Confirm Reset! (y/n)")
                choice = _ConsoleUtility.LevelInput(1, "-")
                if choice == "y":
                    self.ClearSettings()
                    self.SaveSettings()
                    _ConsoleUtility.LevelPrint(1)
                    _ConsoleUtility.AnyKeyDialog("*Settings resetted!")
            elif choice == "3":
                fileInfo = _sw.IO.File.FileInfo(self._settingsPath)
                _os.startfile(fileInfo.tail)
            else:
                break
        return
 