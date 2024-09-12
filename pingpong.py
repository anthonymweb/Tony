from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer, Qt


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(866, 547)
        
        # Add background image
        self.widget = QtWidgets.QWidget(Form)
        self.widget.setGeometry(QtCore.QRect(0, 0, 861, 541))
        self.widget.setStyleSheet("background-image: url('ping_pong_background.jpg');")  # Add your image path here
        self.widget.setObjectName("widget")

        # Left paddle (widget_2)
        self.widget_2 = QtWidgets.QWidget(self.widget)
        self.widget_2.setGeometry(QtCore.QRect(10, 200, 21, 111))
        self.widget_2.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.widget_2.setObjectName("widget_2")

        # Right paddle (widget_3)
        self.widget_3 = QtWidgets.QWidget(self.widget)
        self.widget_3.setGeometry(QtCore.QRect(830, 200, 21, 111))
        self.widget_3.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.widget_3.setObjectName("widget_3")

        # Add ball widget
        self.ball = QtWidgets.QWidget(self.widget)
        self.ball.setGeometry(QtCore.QRect(420, 260, 20, 20))  # Ball in the center
        self.ball.setStyleSheet("background-color: rgb(255, 255, 255); border-radius: 10px;")
        self.ball.setObjectName("ball")

        # Set up ball movement using QTimer
        self.timer = QTimer()
        self.timer.timeout.connect(self.move_ball)
        self.timer.start(20)  # Speed of ball movement

        self.ball_dx = 3  # Horizontal movement step
        self.ball_dy = 3  # Vertical movement step

        # Set up key events for paddle movement
        Form.keyPressEvent = self.keyPressEvent

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Ping Pong Game"))

    def move_ball(self):
        # Move the ball and handle boundary collisions
        ball_rect = self.ball.geometry()
        new_x = ball_rect.x() + self.ball_dx
        new_y = ball_rect.y() + self.ball_dy

        # Check for collision with top and bottom walls
        if new_y <= 0 or new_y >= self.widget.height() - ball_rect.height():
            self.ball_dy = -self.ball_dy

        # Check for collision with paddles
        if self.check_paddle_collision():
            self.ball_dx = -self.ball_dx

        # Check if ball is out of bounds (left or right)
        if new_x <= 0 or new_x >= self.widget.width() - ball_rect.width():
            # Reset ball to center
            self.ball.setGeometry(420, 260, 20, 20)
            self.ball_dx = 3
            self.ball_dy = 3

        self.ball.move(new_x, new_y)

    def check_paddle_collision(self):
        ball_rect = self.ball.geometry()
        left_paddle_rect = self.widget_2.geometry()
        right_paddle_rect = self.widget_3.geometry()

        if ball_rect.intersects(left_paddle_rect) or ball_rect.intersects(right_paddle_rect):
            return True
        return False

    def keyPressEvent(self, event):
        # Move paddles with up/down arrows for the right paddle
        # and W/S for the left paddle
        if event.key() == Qt.Key_Up:
            self.move_paddle(self.widget_3, -10)
        elif event.key() == Qt.Key_Down:
            self.move_paddle(self.widget_3, 10)
        elif event.key() == Qt.Key_W:
            self.move_paddle(self.widget_2, -10)
        elif event.key() == Qt.Key_S:
            self.move_paddle(self.widget_2, 10)

    def move_paddle(self, paddle, delta):
        rect = paddle.geometry()
        new_y = rect.y() + delta

        # Keep paddle within the window
        if new_y >= 0 and new_y <= self.widget.height() - rect.height():
            paddle.move(rect.x(), new_y)
