# TimerManager.py

from PyQt6.QtCore import QTimer, QObject, pyqtSignal

class TimerManager(QObject):
    countdown_update = pyqtSignal(int)
    countdown_finished = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.countdown_timer = QTimer()
        self.countdown_timer.timeout.connect(self.update_countdown)
        self.countdown_remaining = 0
        self.timer_action = "Scatta Foto"
        self.timer_delay_seconds = 5
        
    def start_timer(self, delay_seconds=None, action=None):
        if delay_seconds is not None:
            self.timer_delay_seconds = delay_seconds
        if action is not None:
            self.timer_action = action
            
        self.countdown_remaining = self.timer_delay_seconds
        self.countdown_timer.start(1000)
        
    def stop_timer(self):
        if self.countdown_timer.isActive():
            self.countdown_timer.stop()
            
    def update_countdown(self):
        self.countdown_remaining -= 1
        self.countdown_update.emit(self.countdown_remaining)
        
        if self.countdown_remaining <= 0:
            self.countdown_timer.stop()
            self.countdown_finished.emit()
            
    def set_timer_action(self, action):
        self.timer_action = action
        
    def set_timer_delay(self, delay_seconds):
        self.timer_delay_seconds = delay_seconds