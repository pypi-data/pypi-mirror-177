from typing import Any
from MySEAS.MOEE.MOES import *
from MySEAS.Setup.IPS import *
import sys
import threading

class _MOEC:
    def __init__(self) -> None:
        self.scenes = {}
        self.targetedScene = None

        self.sceneThreads = {}

    def newScene(self, sceneName:str, isTargeted:bool=True) -> Any:
        self.scenes[sceneName] = MOES()
        if self.isTargeted:
            self.targetedScene = [self.scenes[sceneName], threading.Thread(name=sceneName, target=self.scenes[sceneName].update)]

        return self.targetedScene

    def targetScene(self, sceneName:str) -> Any:
        self.stopMOEC()
        try: self.targetedScene = [self.scenes[sceneName], threading.Thread(name=sceneName, target=self.scenes[sceneName].update)]
        except: print("MOEC :: TargetScene() :: Error :: No Scene found with the name " + sceneName)
        self.startMOEC()

    def startMOEC(self):
        self.targetedScene[1].start() # Started thread

    def stopMOEC(self):
        self.targetedScene[1].join()


MOEC = _MOEC()
