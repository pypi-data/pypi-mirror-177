from pathlib import Path

import cv2


class Camera:
    def __init__(self, cam_id=0, output_shape=None, output_dir=None):
        self.cam_id = cam_id
        self.output_shape = output_shape or (1280, 800)
        self.output_dir = output_dir or str(Path.cwd().resolve())
        self.save_counter = 0
        self.set_capture_device()
        self.read_image_properties()

    def set_capture_device(self):
        self.camera = cv2.VideoCapture(self.cam_id)

    def read_capture_device(self):
        ack, img = self.camera.read()
        if not ack:
            raise ValueError('Image could not be read from device')        
        return img

    def read_image_properties(self):
        img = self.read_capture_device()
        self.shape = img.shape[:2]
    
    def show(self, image=None):
        image = image if image is not None else self.read_capture_device()
        image = cv2.resize(image, self.output_shape)
        cv2.imshow('Face Lensing', image)

    def switch_capture_device(self):
        self.cam_id = 1 - self.cam_id   
        self.release()
        print(f'Switching to camera {self.cam_id}')
        self.set_capture_device()
        self.read_image_properties()

    def take_screenshot(self, img):
        img_name = f"face_lensing_screenshot_{self.save_counter}.jpg"
        img_path = str(Path(self.output_dir) / img_name)
        cv2.putText(
            img = img,
            text = "Made with Face Lensing - CNRS",
            org = (30, self.shape[0] - 30),
            fontFace = cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=0.8,
            color=(240, 240, 240),
            thickness=2
        )
        cv2.imwrite(img_path, img)
        self.save_counter += 1
        print(f"Image written as {img_path}")

    def release(self):
        self.camera.release()
