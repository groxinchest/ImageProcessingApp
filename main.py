import sys
import cv2
import numpy as np

from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QLabel,
    QVBoxLayout,
    QFileDialog,
    QMessageBox,
    QLineEdit,
    QHBoxLayout
)

from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt


class ImageApp(QWidget):

    def __init__(self):
        super().__init__()

        self.image = None

        self.setWindowTitle("Image Processing App")
        self.setGeometry(100, 100, 900, 800)


        # кнопки

        self.load_button = QPushButton(
            "Загрузить изображение"
        )
        self.load_button.clicked.connect(
            self.load_image
        )


        self.camera_button = QPushButton(
            "Сделать фото с камеры"
        )
        self.camera_button.clicked.connect(
            self.take_photo
        )


        # каналы

        self.red_button = QPushButton(
            "Красный канал"
        )
        self.red_button.clicked.connect(
            self.show_red_channel
        )


        self.green_button = QPushButton(
            "Зеленый канал"
        )
        self.green_button.clicked.connect(
            self.show_green_channel
        )


        self.blue_button = QPushButton(
            "Синий канал"
        )
        self.blue_button.clicked.connect(
            self.show_blue_channel
        )


        # порог для маски

        self.threshold_input = QLineEdit()
        self.threshold_input.setPlaceholderText(
            "Порог красного 0-255"
        )


        self.mask_button = QPushButton(
            "Создать маску красного"
        )
        self.mask_button.clicked.connect(
            self.create_red_mask
        )


        # резкость

        self.sharp_button = QPushButton(
            "Повысить резкость"
        )
        self.sharp_button.clicked.connect(
            self.sharpen_image
        )


        # координаты линии

        self.x1_input = QLineEdit()
        self.x1_input.setPlaceholderText("X1")

        self.y1_input = QLineEdit()
        self.y1_input.setPlaceholderText("Y1")

        self.x2_input = QLineEdit()
        self.x2_input.setPlaceholderText("X2")

        self.y2_input = QLineEdit()
        self.y2_input.setPlaceholderText("Y2")

        self.width_input = QLineEdit()
        self.width_input.setPlaceholderText("Толщина")


        self.line_button = QPushButton(
            "Нарисовать зеленую линию"
        )

        self.line_button.clicked.connect(
            self.draw_line
        )


        # окно картинки

        self.image_label = QLabel()

        self.image_label.setFixedSize(
            800,
            500
        )


        # расположение элементов

        layout = QVBoxLayout()


        layout.addWidget(
            self.load_button
        )

        layout.addWidget(
            self.camera_button
        )


        rgb = QHBoxLayout()

        rgb.addWidget(
            self.red_button
        )

        rgb.addWidget(
            self.green_button
        )

        rgb.addWidget(
            self.blue_button
        )


        layout.addLayout(rgb)


        layout.addWidget(
            self.threshold_input
        )

        layout.addWidget(
            self.mask_button
        )


        layout.addWidget(
            self.sharp_button
        )


        line = QHBoxLayout()

        line.addWidget(
            self.x1_input
        )

        line.addWidget(
            self.y1_input
        )

        line.addWidget(
            self.x2_input
        )

        line.addWidget(
            self.y2_input
        )

        line.addWidget(
            self.width_input
        )


        layout.addLayout(line)


        layout.addWidget(
            self.line_button
        )


        layout.addWidget(
            self.image_label
        )


        self.setLayout(
            layout
        )


    # загрузка изображения

    def load_image(self):

        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Выберите изображение",
            "",
            "Images (*.png *.jpg *.jpeg)"
        )


        if filename:

            self.image = cv2.imread(
                filename
            )


            if self.image is None:

                QMessageBox.warning(
                    self,
                    "Ошибка",
                    "Не удалось открыть файл"
                )

                return


            self.show_image(
                self.image
            )
        # камера

    def take_photo(self):

        camera = cv2.VideoCapture(
            0,
            cv2.CAP_AVFOUNDATION
        )


        if not camera.isOpened():

            QMessageBox.warning(
                self,
                "Ошибка",
                "Камера не найдена"
            )

            return


        # немного ждём запуск камеры

        for i in range(15):
            camera.read()


        ret, frame = camera.read()


        camera.release()


        if not ret:

            QMessageBox.warning(
                self,
                "Ошибка",
                "Не получилось сделать фото"
            )

            return


        self.image = frame


        self.show_image(
            self.image
        )



    # вывод картинки

    def show_image(self, image):

        rgb = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2RGB
        )


        h, w, ch = rgb.shape


        bytes_line = ch * w


        q_img = QImage(
            rgb.data,
            w,
            h,
            bytes_line,
            QImage.Format_RGB888
        )


        pixmap = QPixmap.fromImage(
            q_img
        )


        pixmap = pixmap.scaled(
            self.image_label.width(),
            self.image_label.height(),
            Qt.KeepAspectRatio
        )


        self.image_label.setPixmap(
            pixmap
        )



    # красный канал

    def show_red_channel(self):

        if self.image is None:
            return


        img = self.image.copy()


        # убираем синий и зелёный

        img[:, :, 0] = 0
        img[:, :, 1] = 0


        self.show_image(
            img
        )



    # зелёный канал

    def show_green_channel(self):

        if self.image is None:
            return


        img = self.image.copy()


        # убираем синий и красный

        img[:, :, 0] = 0
        img[:, :, 2] = 0


        self.show_image(
            img
        )



    # синий канал

    def show_blue_channel(self):

        if self.image is None:
            return


        img = self.image.copy()


        # убираем зелёный и красный

        img[:, :, 1] = 0
        img[:, :, 2] = 0


        self.show_image(
            img
        )



    # маска красного цвета

    def create_red_mask(self):

        if self.image is None:

            QMessageBox.warning(
                self,
                "Ошибка",
                "Сначала загрузите изображение"
            )

            return


        try:

            value = int(
                self.threshold_input.text()
            )


        except:

            QMessageBox.warning(
                self,
                "Ошибка",
                "Введите число"
            )

            return


        # берём красный канал

        red = self.image[:, :, 2]


        # делаем маску

        mask = cv2.threshold(
            red,
            value,
            255,
            cv2.THRESH_BINARY
        )[1]


        mask = cv2.cvtColor(
            mask,
            cv2.COLOR_GRAY2BGR
        )


        self.show_image(
            mask
        )
        # повышение резкости

    def sharpen_image(self):

        if self.image is None:

            return


        # фильтр резкости

        kernel = np.array(
            [
                [-1, -1, -1],
                [-1,  9, -1],
                [-1, -1, -1]
            ]
        )


        result = cv2.filter2D(
            self.image,
            -1,
            kernel
        )


        self.show_image(
            result
        )



    # рисование линии

    def draw_line(self):

        if self.image is None:

            return


        try:

            x1 = int(
                self.x1_input.text()
            )

            y1 = int(
                self.y1_input.text()
            )

            x2 = int(
                self.x2_input.text()
            )

            y2 = int(
                self.y2_input.text()
            )

            width = int(
                self.width_input.text()
            )


        except:

            QMessageBox.warning(
                self,
                "Ошибка",
                "Проверь координаты"
            )

            return



        img = self.image.copy()


        # рисуем зелёную линию

        cv2.line(
            img,
            (x1, y1),
            (x2, y2),
            (0, 255, 0),
            width
        )


        self.show_image(
            img
        )



# запуск программы

if __name__ == "__main__":

    app = QApplication(
        sys.argv
    )


    window = ImageApp()


    window.show()


    sys.exit(
        app.exec_()
    )