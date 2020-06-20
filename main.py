import sys, hashlib
import qdarkstyle

from PyQt5.QtWidgets import (QApplication, QSplitter, QGridLayout, QHBoxLayout, QPushButton,
                             QTreeWidget, QFrame, QLabel, QHBoxLayout, QMainWindow,
                             QStackedLayout, QWidget, QVBoxLayout, QLineEdit, QTextEdit,QRadioButton,
                             QTreeWidgetItem, QDesktopWidget,QFileDialog,QProgressBar)
from PyQt5.QtCore import Qt, QUrl,QRect,QBasicTimer
from PyQt5.QtWebEngineWidgets import QWebEngineView
import time


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        # 设置窗口名称
        self.setWindowTitle("古汉语纠错系统")

        # 设置状态栏
        self.status = self.statusBar()
        self.status.showMessage("hello,古汉语～")

        # 设置初始化的窗口大小
        self.resize(600, 400)

        # 最开始窗口要居中显示
        self.center()

        # 设置窗口透明度
        self.setWindowOpacity(0.9)  # 设置窗口透明度

        # 设置窗口样式
        self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

        # 设置整体布局 左右显示
        pagelayout = QGridLayout()

        # 左侧开始布局
        # 创建左侧部件
        top_left_frame = QFrame(self)
        top_left_frame.setFrameShape(QFrame.StyledPanel)
        # 　左边按钮为垂直布局
        button_layout = QVBoxLayout(top_left_frame)

        # 登录按钮
        verifyid_btn = QPushButton(top_left_frame)
        verifyid_btn.setFixedSize(100, 30), verifyid_btn.setText("确认身份")
        button_layout.addWidget(verifyid_btn)
        # 输入用户名　密码按钮
        user_btn = QPushButton(top_left_frame)
        user_btn.setFixedSize(100, 30), user_btn.setText("登录")
        button_layout.addWidget(user_btn)
        # 申请账号　按钮
        registor_btn = QPushButton(top_left_frame)
        registor_btn.setFixedSize(100, 30), registor_btn.setText("申请帐号")
        button_layout.addWidget(registor_btn)
        # 录入信息按钮
        input_btn = QPushButton(top_left_frame)
        input_btn.setFixedSize(100, 30), input_btn.setText("上传文件")
        button_layout.addWidget(input_btn)
        # 查询按钮
        save_btn = QPushButton(top_left_frame)
        save_btn.setFixedSize(100, 30), save_btn.setText("保存信息")
        button_layout.addWidget(save_btn)
        # 建模之家　按钮
        check_btn = QPushButton(top_left_frame)
        check_btn.setFixedSize(100, 30), check_btn.setText("查看信息")
        button_layout.addWidget(check_btn)
        # 退出按钮
        quit_btn = QPushButton(top_left_frame)
        quit_btn.setFixedSize(100, 30), quit_btn.setText("退出")
        button_layout.addWidget(quit_btn)

        # 左下角为空白 必须要有布局，才可以显示至内容中
        bottom_left_frame = QFrame(self)
        self.blank_label = QLabel(bottom_left_frame)
        blank_layout = QVBoxLayout(bottom_left_frame)
        self.blank_label.setText("邓君~~~")
        self.blank_label.setFixedHeight(50)
        self.progressBar = QProgressBar(bottom_left_frame)
        #self.progressBar.setGeometry(QRect(210, 50, 118, 23))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.timer = QBasicTimer()
        self.step = 0
        self.analysis_time = 0
        blank_layout.addWidget(self.blank_label)
        blank_layout.addWidget(self.progressBar)
        self.webEngineView = QWebEngineView(bottom_left_frame)
        self.webEngineView.close()
        blank_layout.addWidget(self.webEngineView)

        # 右侧开始布局 对应按钮布局
        right_frame = QFrame(self)
        right_frame.setFrameShape(QFrame.StyledPanel)
        # 右边显示为stack布局
        self.right_layout = QStackedLayout(right_frame)

        # 确认身份
        # 管理员身份
        radio_btn_admin = QRadioButton(right_frame)
        radio_btn_admin.setText("我是老师，来输入数据的")
        # 游客身份
        radio_btn_user = QRadioButton(right_frame)
        radio_btn_user.setText("我是游客，就来看看")
        # 以处置布局管理器管理
        radio_btn_layout = QVBoxLayout()  # 这里没必要在传入frame，已经有布局了
        radio_btn_widget = QWidget(right_frame)
        radio_btn_layout.addWidget(radio_btn_admin)
        radio_btn_layout.addWidget(radio_btn_user)
        radio_btn_widget.setLayout(radio_btn_layout)
        self.right_layout.addWidget(radio_btn_widget)

        # 登录界面
        user_line = QLineEdit(right_frame)
        user_line.setPlaceholderText("输入账号：")
        user_line.setFixedWidth(400)
        password_line = QLineEdit(right_frame)
        password_line.setPlaceholderText("请输入密码：")
        password_line.setFixedWidth(400)
        login_btn = QPushButton("确认登陆")
        login_btn.setFixedSize(100, 30)
        login_layout = QVBoxLayout()
        login_widget = QWidget(right_frame)
        login_widget.setLayout(login_layout)
        login_layout.addWidget(user_line)
        login_layout.addWidget(password_line)
        login_layout.addWidget(login_btn)
        self.right_layout.addWidget(login_widget)

        # 申请帐号
        registor_id = QLineEdit(right_frame)
        registor_id.setPlaceholderText("请输入新帐号：")
        registor_id.setFixedWidth(400)
        registor_psd = QLineEdit(right_frame)
        registor_psd.setPlaceholderText("请输入密码：")
        registor_psd.setFixedWidth(400)
        registor_confirm = QLineEdit(right_frame)
        registor_confirm.setPlaceholderText("请确认密码：")
        registor_confirm.setFixedWidth(400)
        registor_confirm_btn = QPushButton("确认提交")
        registor_confirm_btn.setFixedSize(100, 30)
        registor_layout = QVBoxLayout()
        register_widget = QWidget(right_frame)
        register_widget.setLayout(registor_layout)
        registor_layout.addWidget(registor_id)
        registor_layout.addWidget(registor_psd)
        registor_layout.addWidget(registor_confirm)
        registor_layout.addWidget(registor_confirm_btn)
        self.right_layout.addWidget(register_widget)


        self.check_info = QTextEdit(right_frame)
        check_widget = QWidget(right_frame)
        check_layout = QVBoxLayout()
        check_widget.setLayout(check_layout)
        check_layout.addWidget(self.check_info)
        self.right_layout.addWidget(check_widget)

        self.url = ''  # 后期会获取要访问的url

        # 三分界面，可拖动
        self.splitter1 = QSplitter(Qt.Vertical)
        top_left_frame.setFixedHeight(250)
        self.splitter1.addWidget(top_left_frame)
        self.splitter1.addWidget(bottom_left_frame)

        self.splitter2 = QSplitter(Qt.Horizontal)
        self.splitter2.addWidget(self.splitter1)
        # 　添加右侧的布局
        self.splitter2.addWidget(right_frame)

        # 窗口部件添加布局
        widget = QWidget()
        pagelayout.addWidget(self.splitter2)
        widget.setLayout(pagelayout)
        self.setCentralWidget(widget)

        # 函数功能区
        verifyid_btn.clicked.connect(self.show_verifyid_page)
        user_btn.clicked.connect(self.show_login_page)
        registor_btn.clicked.connect(self.show_register_page)
        check_btn.clicked.connect(self.show_check_page)
        quit_btn.clicked.connect(self.quit_act)
        input_btn.clicked.connect(self.input_file)
        save_btn.clicked.connect(self.save_click)

    def input_file(self):
        print("hello")
        file_path, filetype = QFileDialog.getOpenFileNames(self,
                                                          "选取文件",
                                                          "./",
                                                          "DOC Files (*.docx);;DOC Files (*.doc)")  # 设置文件扩展名过滤,注意用双分号间隔
        if len(file_path)==0:
            print("取消选择,没有选择任何文件")
            return
        print(file_path, filetype)
        file_path_str = str(file_path)
        time_start = time.time()
        self.blank_label.setText("邓君正在帮你分析~~")
        time.sleep(5)
        time_end =time.time()
        self.analysis_time = time_end-time_start
        print(self.analysis_time)
        self.progressBar.setMaximum(self.analysis_time)
        self.timer.start(100, self)
        self.check_info.setPlainText("分析后的结果会在这里呈现，文本，HTML，图像等")
        '''
        bat_path=os.path.join(os.getcwd(),"kk.bat")
        time_start = time.time()
        cmd = "cmd.exe "+bat_path+" "+file_path_str
        print(cmd)
        result = Popen(cmd,stdout=PIPE,stderr=STDOUT)
        time_end =time.time()
        self.analysis_time = time_end-time_start
        self.progressBar.setMaximum(self.analysis_time)
        self.timer.start(100, self)#时间间隔为100ms
        print(result)
        doc = Document(result)
        '''
    def timerEvent(self, e):
        if self.step >= self.analysis_time:
            self.timer.stop()
            self.blank_label.setText('分析完成')
            return
        self.step = self.step + self.analysis_time/100
        print(self.step)
        self.progressBar.setValue(self.step)

    def save_click(self):
        file_save_path, ok2 = QFileDialog.getSaveFileName(self,
                                                     "文件保存",
                                                     "./",
                                                     "All Files (*);;Text Files (*.txt)")
        print(file_save_path)
        # doc.save(file_save_path) #'保存doc文件到路径file_save_path'

    def init(self):
        # 刚开始要管理浏览器，否则很丑
        self.webEngineView.close()
        # 注意先后顺序，resize　在前面会使代码无效
        self.splitter1.setMinimumWidth(150)
        self.splitter2.setMinimumWidth(250)
        self.resize(600, 400)

    def show_check_page(self):
        self.init()
        self.center()
        self.check_info.setPlainText("分析后的结果会在这里呈现，文本，HTML，图像等")
        self.right_layout.setCurrentIndex(3)

    # 显示注册帐号的页面
    def show_register_page(self):
        self.init()
        self.center()
        self.right_layout.setCurrentIndex(2)

    # 显示登录的页面
    def show_login_page(self):
        self.init()
        self.center()
        self.right_layout.setCurrentIndex(1)

    # stacklayout 布局，显示验证身份的页面
    def show_verifyid_page(self):
        self.init()
        self.center()
        self.right_layout.setCurrentIndex(0)

    # 设置窗口居中
    def center(self):
        '''
        获取桌面长宽
        获取窗口长宽
        移动
        '''
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)

    # 退出按钮 有信息框的提示　询问是否确认退出
    def quit_act(self):
        # sender 是发送信号的对象
        sender = self.sender()
        print(sender.text() + '键被按下')
        qApp = QApplication.instance()
        qApp.quit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())