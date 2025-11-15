# MenuBar.py (CORRETTO)

from PyQt6.QtWidgets import QMenuBar
from PyQt6.QtGui import QAction, QKeySequence

class MenuBar(QMenuBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.create_menu()
        
    def create_menu(self):
        file_menu = self.addMenu("File")
        
        save_action = QAction("Salva con nome", self)
        save_action.triggered.connect(lambda: self.parent().save_as())
        file_menu.addAction(save_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("Esci", self)
        exit_action.setShortcut(QKeySequence("ESC"))
        exit_action.triggered.connect(lambda: self.parent().close())
        file_menu.addAction(exit_action)
        
        view_menu = self.addMenu("Visualizza")
        
        fullscreen_action = QAction("Schermo Intero", self)
        fullscreen_action.setShortcut(QKeySequence("F11"))
        fullscreen_action.triggered.connect(lambda: self.parent().toggle_fullscreen())
        view_menu.addAction(fullscreen_action)
        
        shortcuts_menu = self.addMenu("Scorciatoie")
        
        c_action = QAction("C - Scatta una foto", self)
        c_action.triggered.connect(lambda: self.parent().capture_photo())
        shortcuts_menu.addAction(c_action)

        m_action = QAction("M - Specchia Immagine", self)
        m_action.triggered.connect(lambda: self.parent().toggle_mirror_shortcut())
        shortcuts_menu.addAction(m_action)

        v_action = QAction("V - Avvia/Ferma Registrazione", self)
        v_action.triggered.connect(lambda: self.parent().on_record_clicked())
        shortcuts_menu.addAction(v_action)

        t_action = QAction("T - Avvia Timer", self)
        t_action.triggered.connect(lambda: self.parent().start_timer())
        shortcuts_menu.addAction(t_action)

        f11_action = QAction("F11 - Schermo Intero", self)
        f11_action.triggered.connect(lambda: self.parent().toggle_fullscreen())
        shortcuts_menu.addAction(f11_action)

        esc_action = QAction("ESC - Chiudi l'applicazione", self)
        esc_action.triggered.connect(lambda: self.parent().close())
        shortcuts_menu.addAction(esc_action)
        
        help_menu = self.addMenu("Aiuto")
        
        about_action = QAction("Informazioni", self)
        about_action.triggered.connect(lambda: self.parent().show_about())
        help_menu.addAction(about_action)