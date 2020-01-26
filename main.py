from PyQt5.QtCore import QUrl, QSize
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWebKitWidgets import QWebView
from PyQt5.QtWidgets import QToolBar, QAction, QLineEdit, QProgressBar, QLabel, QMainWindow, QTabWidget, QStatusBar


class BrowserEngineView(QWebView):
    tabs = []

    def __init__(self, Main, parent=None):
        super(BrowserEngineView, self).__init__(parent)
        self.mainWindow = Main

    def createWindow(self, QWebPage_WebWindowType):
        webview = BrowserEngineView(self.mainWindow)
        tab = BrowserTab(self.mainWindow)
        tab.browser = webview
        tab.setCentralWidget(tab.browser)
        self.tabs.append(tab)
        self.mainWindow.add_new_tab(tab)
        return webview


class BrowserTab(QMainWindow):
    def __init__(self, Main, parent=None):
        super(BrowserTab, self).__init__(parent)
        self.mainWindow = Main
        self.browser = BrowserEngineView(self.mainWindow)
        self.browser.load(QUrl("about:blank"))
        self.setCentralWidget(self.browser)
        self.navigation_bar = QToolBar('Navigation')
        self.navigation_bar.setIconSize(QSize(24, 24))
        self.navigation_bar.setMovable(False)
        self.addToolBar(self.navigation_bar)
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        self.back_button = QAction(QIcon('Assets/back.png'), '后退', self)
        self.next_button = QAction(QIcon('Assets/forward.png'), '前进', self)
        self.stop_button = QAction(QIcon('Assets/stop.png'), '停止', self)
        self.refresh_button = QAction(QIcon('Assets/refresh.png'), '刷新', self)
        self.home_button = QAction(QIcon('Assets/home.png'), '主页', self)
        self.enter_button = QAction(QIcon('Assets/enter.png'), '转到', self)
        self.add_button = QAction(QIcon('Assets/new.png'), '新建标签页', self)
        self.ssl_label1 = QLabel(self)
        self.ssl_label2 = QLabel(self)
        self.url_text_bar = QLineEdit(self)
        self.url_text_bar.setMinimumWidth(300)
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximumWidth(120)
        self.set_button = QAction(QIcon('Assets/setting.png'), '设置', self)
        self.navigation_bar.addAction(self.back_button)
        self.navigation_bar.addAction(self.next_button)
        # self.navigation_bar.addAction(self.stop_button)
        self.navigation_bar.addAction(self.refresh_button)
        self.navigation_bar.addAction(self.home_button)
        self.navigation_bar.addAction(self.add_button)
        self.navigation_bar.addSeparator()
        self.navigation_bar.addWidget(self.ssl_label1)
        self.navigation_bar.addWidget(self.ssl_label2)
        self.navigation_bar.addWidget(self.url_text_bar)
        self.navigation_bar.addAction(self.enter_button)
        self.navigation_bar.addSeparator()
        self.navigation_bar.addWidget(self.progress_bar)
        # self.navigation_bar.addAction(self.set_button)
        self.status_icon = QLabel()
        self.status_icon.setScaledContents(True)
        self.status_icon.setMaximumHeight(24)
        self.status_icon.setMaximumWidth(24)
        self.status_icon.setPixmap(QPixmap("Assets/main.png"))
        self.status_label = QLabel()
        self.status_label.setText(self.mainWindow.version + " - SimPyWeb X")
        self.status_bar.addWidget(self.status_icon)
        self.status_bar.addWidget(self.status_label)

    def navigate_to_url(self):
        s = QUrl(self.url_text_bar.text())
        if s.scheme() == '':
            s.setScheme('http')
        self.browser.load(s)

    def navigate_to_home(self):
        s = QUrl("https://www.baidu.com/")
        self.browser.load(s)

    def renew_urlbar(self, s):
        prec = s.scheme()
        if prec == 'http':
            self.ssl_label1.setPixmap(QPixmap("Assets/unsafe.png").scaledToHeight(24))
            self.ssl_label2.setText(" 不安全 ")
            self.ssl_label2.setStyleSheet("color:red;")
        elif prec == 'https':
            self.ssl_label1.setPixmap(QPixmap("Assets/safe.png").scaledToHeight(24))
            self.ssl_label2.setText(" 安全 ")
            self.ssl_label2.setStyleSheet("color:green;")
        self.url_text_bar.setText(s.toString())
        self.url_text_bar.setCursorPosition(0)

    def renew_progress_bar(self, p):
        self.progress_bar.setValue(p)


class BrowserWindow(QMainWindow):
    name = "SimPyWeb X"
    version = "3.0"
    date = "2020.1.26"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle(self.name + " " + self.version)
        self.setWindowIcon(QIcon('Assets/main.png'))
        self.resize(1200, 900)
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.setMovable(True)
        self.tabs.setTabShape(0)
        self.setCentralWidget(self.tabs)
        self.tabs.tabCloseRequested.connect(self.close_current_tab)
        self.tabs.currentChanged.connect(lambda i: self.setWindowTitle(self.tabs.tabText(i) + " - " + self.name))
        self.init_tab = BrowserTab(self)
        self.init_tab.browser.load(QUrl("https://www.baidu.com/"))
        self.add_new_tab(self.init_tab)

    def add_blank_tab(self):
        blank_tab = BrowserTab(self)
        self.add_new_tab(blank_tab)

    def add_new_tab(self, tab):
        i = self.tabs.addTab(tab, "")
        self.tabs.setCurrentIndex(i)
        self.tabs.setTabIcon(i,QIcon('Assets/main.png'))
        tab.back_button.triggered.connect(tab.browser.back)
        tab.next_button.triggered.connect(tab.browser.forward)
        tab.stop_button.triggered.connect(tab.browser.stop)
        tab.refresh_button.triggered.connect(tab.browser.reload)
        tab.home_button.triggered.connect(tab.navigate_to_home)
        tab.enter_button.triggered.connect(tab.navigate_to_url)
        tab.add_button.triggered.connect(self.add_blank_tab)
        tab.url_text_bar.returnPressed.connect(tab.navigate_to_url)
        tab.browser.urlChanged.connect(tab.renew_urlbar)
        tab.browser.loadProgress.connect(tab.renew_progress_bar)
        tab.browser.titleChanged.connect(lambda title: (self.tabs.setTabText(i, title),
                                                        self.tabs.setTabToolTip(i, title),
                                                        self.setWindowTitle(self.tabs.tabText(i) + " - " + self.name)))
        # tab.browser.iconChanged.connect(self.tabs.setTabIcon(i, tab.browser.icon()))

    def close_current_tab(self, i):
        if self.tabs.count() > 1:
            self.tabs.removeTab(i)
        else:
            self.close()
