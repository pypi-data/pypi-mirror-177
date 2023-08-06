import numpy as np
from scipy.ndimage import map_coordinates


class Morphing:
    def __init__(self, target_shape, morph_file, zoom, shift=(0, 0)):
        self.zoom = zoom
        self.shift = np.asarray(shift, dtype=int)
        self.read_morph_file(morph_file)
        self.set_target_shape(target_shape)

    def read_morph_file(self, file_path):
        lens_model = np.load(file_path)
        self.hx = lens_model["dplx"]
        self.hy = lens_model["dply"]
        self.shape = np.asarray(self.hx.shape, dtype=int)

    def set_target_shape(self, new_shape):
        self.target_shape = np.asarray(new_shape, dtype=int)
        self.init_morphing()

    def init_morphing(self):
        height, width = self.target_shape
        lens_center = self.shape / 2
        img_center = self.target_shape / 2 + self.shift

        self.Y, self.X = np.indices(self.target_shape)

        # Create coordinates mapping between the image and the lens
        centred_coords = (
            np.indices(self.target_shape).reshape(2, -1) 
            - img_center[:, None] 
            + lens_center[:, None]).astype(int)

        centred_coords[0] = centred_coords[0].clip(0, self.shape[0]-1)
        centred_coords[1] = centred_coords[1].clip(0, self.shape[1]-1)

        lens_coords = np.reshape(centred_coords, (2, *self.target_shape))

        dpl1y = map_coordinates(self.hy / self.zoom, lens_coords, order=1)
        dpl1x = map_coordinates(self.hx / self.zoom, lens_coords, order=1)

        self.dply = np.array(self.Y - dpl1y).astype(int)
        self.dplx = np.array(self.X - dpl1x).astype(int)
        # Mirror lens effect on the horizontal axis
        self.dplx = width - self.dplx

    def apply(self, image):
        return np.asarray(
            list(map(lambda p, q: image[self.dply[p, q], self.dplx[p, q]], self.Y, self.X)))

    def increase_effect(self):
        if self.zoom > 0.005:
            self.zoom -= 0.005
        self.init_morphing()

    def decrease_effect(self):
        self.zoom += 0.005
        self.init_morphing()
