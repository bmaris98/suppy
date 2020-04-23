from pathlib import Path
from suppy.app.visual_constants import NODE_HEIGHT, NODE_WIDTH
from PIL import ImageTk, Image
from suppy.utils.stats_constants import BUFFER, CONVERGENCE, CUSTOM, END, RANDOM_ERROR, REPAIR, START, TEST, TRANSPORT

class ImageLoader:

    def __init__(self):
        self._assets_path = Path(__file__).parent / '../data/assets'
        self._node_types = [BUFFER, CUSTOM, RANDOM_ERROR, TEST, CONVERGENCE, TRANSPORT, START, END, REPAIR]
        self._images = {}
        self._load_images()

    def _load_images(self):
        for node_type in self._node_types:
            path = (self._assets_path / (node_type + '.png')).resolve()
            img = Image.open(path)
            img = img.resize((NODE_WIDTH, NODE_HEIGHT))
            self._images[node_type] = ImageTk.PhotoImage(img)

    def get_image(self, node_type: str):
        return self._images[node_type]