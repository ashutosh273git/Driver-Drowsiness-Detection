import sys,time,threading
class AlertSound:
    def __init__(self,enabled=True,cooldown_seconds=2):
        self.enabled=enabled; self.cooldown=cooldown_seconds; self.last=0
    def play(self):
        now=time.monotonic()
        if not self.enabled or now-self.last<self.cooldown: return
        self.last=now; threading.Thread(target=self._beep,daemon=True).start()
    @staticmethod
    def _beep():
        try:
            if sys.platform=="win32":
                import winsound; winsound.MessageBeep(winsound.MB_ICONWARNING)
            else: print("\a",end="",flush=True)
        except Exception: pass
