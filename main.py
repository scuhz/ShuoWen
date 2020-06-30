import sys, hashlib
import qdarkstyle

from PyQt5.QtWidgets import (QApplication, QSplitter, QGridLayout, QHBoxLayout, QPushButton,
                             QTreeWidget, QFrame, QLabel, QHBoxLayout, QMainWindow,QButtonGroup,
                             QStackedLayout, QWidget, QVBoxLayout, QLineEdit, QTextEdit,QRadioButton,
                             QTreeWidgetItem, QDesktopWidget,QFileDialog,QProgressBar)
from PyQt5.QtCore import Qt, QUrl,QRect,QBasicTimer,QObject,pyqtSignal
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtGui import QTextCursor
import time
from shuowen import *


def analysis(file_path_str, style=1):
    print('开始分析文档~~')
    tb = tuban(file_path_str)
    try:
        flag = tb.parse()
        tb.array2dict_save()
    except:
        flag = -2
    if flag == -1:
        tb.dict2order_save()
        tb.get_output_docx_by_docx(style)
    else:
        print(tb.get_error())


class Stream(QObject):
    """Redirects console output to text widget."""
    newText = pyqtSignal(str)

    def write(self, text):
        QApplication.processEvents()
        self.newText.emit(str(text))


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        sys.stdout = Stream(newText=self.onUpdateText)
        self.style=1
        # 设置窗口名称
        self.setWindowTitle("古汉语纠错系统")

        # 设置状态栏
        self.status = self.statusBar()
        self.status.showMessage("你好,古汉语～")

        # 设置初始化的窗口大小
        self.resize(1000, 800)

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

        # 输入用户名　密码按钮
        self.user_btn = QPushButton(top_left_frame)
        self.user_btn.setFixedSize(150, 30), self.user_btn.setText("登录")
        button_layout.addWidget(self.user_btn)
        # 确认按钮
        self.verifyid_btn = QPushButton(top_left_frame)
        self.verifyid_btn.setFixedSize(150, 30), self.verifyid_btn.setText("确认文件形式")
        button_layout.addWidget(self.verifyid_btn)

        # 申请账号　按钮
        '''
        registor_btn = QPushButton(top_left_frame)
        registor_btn.setFixedSize(100, 30), registor_btn.setText("申请帐号")
        button_layout.addWidget(registor_btn)
        '''
        # 录入信息按钮
        self.input_btn = QPushButton(top_left_frame)
        self.input_btn.setFixedSize(150, 30), self.input_btn.setText("上传文件")
        button_layout.addWidget(self.input_btn)
        # 查询按钮
        '''
        save_btn = QPushButton(top_left_frame)
        save_btn.setFixedSize(100, 30), save_btn.setText("保存信息")
        button_layout.addWidget(save_btn)
        '''
        # 查看　按钮
        self.check_btn = QPushButton(top_left_frame)
        self.check_btn.setFixedSize(150, 30), self.check_btn.setText("查看信息")
        button_layout.addWidget(self.check_btn)
        # 退出按钮
        quit_btn = QPushButton(top_left_frame)
        quit_btn.setFixedSize(150, 30), quit_btn.setText("退出")
        button_layout.addWidget(quit_btn)

        # 左下角为空白 必须要有布局，才可以显示至内容中
        bottom_left_frame = QFrame(self)
        self.blank_label = QLabel(bottom_left_frame)
        blank_layout = QVBoxLayout(bottom_left_frame)
        self.blank_label.setText("古汉语~~~")
        self.blank_label.setFixedHeight(50)
        #self.progressBar = QProgressBar(bottom_left_frame)
        #self.progressBar.setGeometry(QRect(210, 50, 118, 23))
        #self.progressBar.setProperty("value", 0)
        #self.progressBar.setObjectName("progressBar")
        self.timer = QBasicTimer()
        self.step = 0
        self.analysis_time = 0
        blank_layout.addWidget(self.blank_label)
        #blank_layout.addWidget(self.progressBar)
        self.webEngineView = QWebEngineView(bottom_left_frame)
        self.webEngineView.close()
        blank_layout.addWidget(self.webEngineView)

        # 右侧开始布局 对应按钮布局
        right_frame = QFrame(self)
        right_frame.setFrameShape(QFrame.StyledPanel)
        # 右边显示为stack布局
        self.right_layout = QStackedLayout(right_frame)

        # 登录界面
        self.user_line = QLineEdit(right_frame)
        self.user_line.setPlaceholderText("输入账号：")
        self.user_line.setFixedWidth(400)
        self.password_line = QLineEdit(right_frame)
        self.password_line.setEchoMode(QLineEdit.Password)
        self.password_line.setPlaceholderText("请输入密码：")
        self.password_line.setFixedWidth(400)
        self.login_btn = QPushButton("确认登陆")
        self.login_btn.setFixedSize(100, 30)
        login_layout = QVBoxLayout()
        login_widget = QWidget(right_frame)
        login_widget.setLayout(login_layout)
        login_layout.addWidget(self.user_line)
        login_layout.addWidget(self.password_line)
        login_layout.addWidget(self.login_btn)
        self.right_layout.addWidget(login_widget)


        # 确认输出文件的组织形式
        #
        select_output_type_lab = QLabel(right_frame)
        select_output_type_lab.setText("请选择要保存的文件组织形式：")
        select_output_type_lab.setFixedHeight(100)
        radio_btn_admin = QRadioButton(right_frame)
        radio_btn_admin.setText("1.id+小篆+字")
        radio_btn_admin.setFixedHeight(100)
        #
        radio_btn_user = QRadioButton(right_frame)
        radio_btn_user.setText("2. id+字")
        radio_btn_user.setFixedHeight(100)
        #
        radio_btn_user1 = QRadioButton(right_frame)
        radio_btn_user1.setText("3. 字")
        radio_btn_user1.setFixedHeight(100)
        #
        self.bg1 = QButtonGroup(self)
        self.bg1.addButton(radio_btn_admin, 1)
        self.bg1.addButton(radio_btn_user, 2)
        self.bg1.addButton(radio_btn_user1, 3)
        # 以处置布局管理器管理
        radio_btn_layout = QVBoxLayout()  # 这里没必要在传入frame，已经有布局了
        radio_btn_widget = QWidget(right_frame)
        radio_btn_layout.addWidget(select_output_type_lab)
        radio_btn_layout.addWidget(radio_btn_admin)
        radio_btn_layout.addWidget(radio_btn_user)
        radio_btn_layout.addWidget(radio_btn_user1)
        radio_btn_widget.setLayout(radio_btn_layout)
        self.right_layout.addWidget(radio_btn_widget)

        #查看信息
        self.check_info = QTextEdit(right_frame,readOnly=True)
        self.check_info.ensureCursorVisible()
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
        self.verifyid_btn.clicked.connect(self.show_verifyid_page)
        self.user_btn.clicked.connect(self.show_login_page)
        #registor_btn.clicked.connect(self.show_register_page)
        self.check_btn.clicked.connect(self.show_check_page)
        quit_btn.clicked.connect(self.quit_act)
        self.input_btn.clicked.connect(self.input_file)
        self.bg1.buttonClicked.connect(self.rbclicked)
        self.login_btn.clicked.connect(self.login_press)
        #save_btn.clicked.connect(self.save_click)

        # 禁用按钮
        self.verifyid_btn.setEnabled(False)
        self.input_btn.setEnabled(False)
        self.check_btn.setEnabled(False)

    def login_press(self):
        user = self.user_line.text()
        passwd = self.password_line.text()
        print("do match operation with input user and passwd")
        self.verifyid_btn.setEnabled(True)
        self.input_btn.setEnabled(True)
        self.check_btn.setEnabled(True)

    def rbclicked(self):
        if self.bg1.checkedId()==1:
            self.style =1
        elif self.bg1.checkedId()==2:
            self.style =2
        elif self.bg1.checkedId()==3:
            self.style =3
        #print(self.style)

    def onUpdateText(self, text):
        """Write console output to text widget."""
        cursor = self.check_info.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(text)
        self.check_info.setTextCursor(cursor)
        self.check_info.ensureCursorVisible()


    def input_file(self):
        self.right_layout.setCurrentIndex(2)
        #print("hello")
        file_path, filetype = QFileDialog.getOpenFileName(self,
                                                          "选取文件",
                                                          "./",
                                                          "DOC Files (*.docx);;DOC Files (*.doc)")  # 设置文件扩展名过滤,注意用双分号间隔
        if file_path=='':
            print("取消选择,没有选择任何文件")
            return
        #print(file_path)
        file_path_str = str(file_path)
        time_start = time.time()

        ### python file analysis block start
        analysis(file_path_str,self.style)
        ### python file analysis block end

        #print(sys.stderr)
        self.blank_label.setText("正在帮你分析~~")
        time_end =time.time()
        self.analysis_time = time_end-time_start
        print(self.analysis_time)
        self.blank_label.setText('分析完成')
        #self.progressBar.setMaximum(self.analysis_time)
        #self.timer.start(100, self)
        #self.check_info.setPlainText("分析后的结果会在这里呈现，文本，HTML，图像等")
    
    def timerEvent(self, e):
        if self.step >= self.analysis_time:
            self.timer.stop()
            self.blank_label.setText('分析完成')
            return
        self.step = self.step + self.analysis_time/100
        #print(self.step)
        #self.progressBar.setValue(self.step)

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
        self.resize(1000, 800)

    def show_check_page(self):
        self.init()
        self.center()
        #self.check_info.setPlainText("分析后的结果会在这里呈现，文本，HTML，图像等")
        self.right_layout.setCurrentIndex(2)

    # 显示注册帐号的页面
    '''
    def show_register_page(self):
        self.init()
        self.center()
        self.right_layout.setCurrentIndex(2)
    '''
    # 显示登录的页面
    def show_login_page(self):
        self.init()
        self.center()

        self.right_layout.setCurrentIndex(0)

    # stacklayout 布局，显示验证身份的页面
    def show_verifyid_page(self):
        self.init()
        self.center()
        self.right_layout.setCurrentIndex(1)

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