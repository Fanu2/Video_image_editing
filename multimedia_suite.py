import sys, os, glob
import cv2
from PIL import Image
from moviepy.editor import VideoFileClip
from PyQt6.QtWidgets import (
    QApplication, QTabWidget, QWidget, QLabel, QPushButton,
    QLineEdit, QFileDialog, QVBoxLayout, QMessageBox
)
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import QTimer


# ----------------------------------------------------------
# Utility: Safe Haarcascade locator
# ----------------------------------------------------------
def get_haarcascade():
    # Try Conda locations
    paths = glob.glob(os.path.expanduser(
        "~/miniconda3/pkgs/opencv*/share/opencv4/haarcascades/haarcascade_frontalface_default.xml"
    ))

    if paths:
        return paths[0]

    # Try system locations
    system_paths = [
        "/usr/share/opencv4/haarcascades/haarcascade_frontalface_default.xml",
        "/usr/share/opencv/haarcascades/haarcascade_frontalface_default.xml"
    ]

    for p in system_paths:
        if os.path.exists(p):
            return p

    return None


# ----------------------------------------------------------
# TAB 1: IMAGE EDITOR
# ----------------------------------------------------------
class ImageEditorTab(QWidget):
    def __init__(self):
        super().__init__()

        self.image_label = QLabel("No Image Loaded")
        self.image_label.setFixedSize(400, 300)

        self.btn_open = QPushButton("Open Image")
        self.btn_gray = QPushButton("Convert to Grayscale")
        self.btn_save = QPushButton("Save Image")

        self.btn_open.clicked.connect(self.open_image)
        self.btn_gray.clicked.connect(self.to_gray)
        self.btn_save.clicked.connect(self.save_image)

        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        layout.addWidget(self.btn_open)
        layout.addWidget(self.btn_gray)
        layout.addWidget(self.btn_save)
        self.setLayout(layout)

        self.current_image = None
        self.preview_path = "temp_preview.png"

    def open_image(self):
        try:
            file, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Images (*.png *.jpg *.jpeg)")
            if not file:
                return

            self.current_image = Image.open(file)
            pix = QPixmap(file).scaled(400, 300)
            self.image_label.setPixmap(pix)

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def to_gray(self):
        try:
            if not self.current_image:
                QMessageBox.warning(self, "Warning", "No image loaded.")
                return

            self.current_image = self.current_image.convert("L")
            self.current_image.save(self.preview_path)
            self.image_label.setPixmap(QPixmap(self.preview_path).scaled(400, 300))

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def save_image(self):
        try:
            if not self.current_image:
                QMessageBox.warning(self, "Warning", "Nothing to save.")
                return

            file, _ = QFileDialog.getSaveFileName(self, "Save Image", "", "PNG (*.png)")
            if file:
                self.current_image.save(file)
                QMessageBox.information(self, "Saved", f"Image saved to:\n{file}")

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))


# ----------------------------------------------------------
# TAB 2: VIDEO CUTTER
# ----------------------------------------------------------
class VideoCutterTab(QWidget):
    def __init__(self):
        super().__init__()

        self.label = QLabel("No video loaded")
        self.btn_load = QPushButton("Load Video")
        self.start_input = QLineEdit()
        self.end_input = QLineEdit()
        self.start_input.setPlaceholderText("Start time (sec)")
        self.end_input.setPlaceholderText("End time (sec)")
        self.btn_cut = QPushButton("Cut Video")

        self.btn_load.clicked.connect(self.load_video)
        self.btn_cut.clicked.connect(self.cut_video)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.btn_load)
        layout.addWidget(self.start_input)
        layout.addWidget(self.end_input)
        layout.addWidget(self.btn_cut)
        self.setLayout(layout)

        self.video = None
        self.video_path = None

    def load_video(self):
        try:
            file, _ = QFileDialog.getOpenFileName(self, "Open Video", "", "Video (*.mp4 *.mkv *.mov)")
            if not file:
                return

            self.video = VideoFileClip(file)
            self.video_path = file
            self.label.setText(f"Loaded: {os.path.basename(file)}")

        except Exception as e:
            QMessageBox.critical(self, "Error loading video", str(e))

    def cut_video(self):
        try:
            if not self.video:
                QMessageBox.warning(self, "Warning", "Load a video first.")
                return

            start = float(self.start_input.text())
            end = float(self.end_input.text())

            output = "cut_output.mp4"
            clip = self.video.subclip(start, end)
            clip.write_videofile(output)

            QMessageBox.information(self, "Done", f"Saved as {output}")

        except ValueError:
            QMessageBox.warning(self, "Error", "Start/End time must be numbers.")
        except Exception as e:
            QMessageBox.critical(self, "Error cutting video", str(e))


# ----------------------------------------------------------
# Camera helper: Safely open a camera
# ----------------------------------------------------------
def try_open_camera():
    for i in range(5):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            return cap
    return None


# ----------------------------------------------------------
# TAB 3: WEBCAM VIEWER
# ----------------------------------------------------------
class WebcamViewerTab(QWidget):
    def __init__(self):
        super().__init__()

        self.label = QLabel("Webcam not available")
        self.quit_btn = QPushButton("Stop Webcam")
        self.quit_btn.clicked.connect(self.stop_cam)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.quit_btn)
        self.setLayout(layout)

        self.cap = try_open_camera()

        if not self.cap:
            self.label.setText("❌ No webcam detected.")
            return

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

    def update_frame(self):
        try:
            ret, frame = self.cap.read()
            if not ret:
                return

            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb.shape
            img = QImage(rgb.data, w, h, ch * w, QImage.Format.Format_RGB888)
            self.label.setPixmap(QPixmap.fromImage(img))

        except Exception:
            pass  # avoid crashes from intermittent camera issues

    def stop_cam(self):
        try:
            if self.cap:
                self.cap.release()
        except:
            pass


# ----------------------------------------------------------
# TAB 4: FACE DETECTION
# ----------------------------------------------------------
class FaceDetectionTab(QWidget):
    def __init__(self):
        super().__init__()

        self.label = QLabel("Waiting for camera...")
        self.quit_btn = QPushButton("Stop Camera")
        self.quit_btn.clicked.connect(self.stop_cam)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.quit_btn)
        self.setLayout(layout)

        self.cap = try_open_camera()
        if not self.cap:
            self.label.setText("❌ No webcam detected.")
            return

        cascade_path = get_haarcascade()
        if not cascade_path:
            self.label.setText("❌ Haarcascade not found.")
            self.detector = None
        else:
            self.detector = cv2.CascadeClassifier(cascade_path)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

    def update_frame(self):
        try:
            ret, frame = self.cap.read()
            if not ret:
                return

            if self.detector:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = self.detector.detectMultiScale(gray, 1.3, 5)

                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x,y), (x+w, y+h), (255, 0, 0), 2)

            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb.shape
            img = QImage(rgb.data, w, h, ch * w, QImage.Format.Format_RGB888)
            self.label.setPixmap(QPixmap.fromImage(img))

        except Exception:
            pass

    def stop_cam(self):
        try:
            if self.cap:
                self.cap.release()
        except:
            pass


# ----------------------------------------------------------
# MAIN APP
# ----------------------------------------------------------
class MultimediaSuite(QTabWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Python Multimedia Suite")
        self.resize(600, 500)

        self.addTab(ImageEditorTab(), "Image Editor")
        self.addTab(VideoCutterTab(), "Video Cutter")
        self.addTab(WebcamViewerTab(), "Webcam Viewer")
        self.addTab(FaceDetectionTab(), "Face Detection")


app = QApplication(sys.argv)
win = MultimediaSuite()
win.show()
app.exec()
