from pathlib import Path
from suppy.app.visual_constants import NODE_HEIGHT, NODE_WIDTH
from PIL import ImageTk, Image
from suppy.utils.stats_constants import DIVERGENCE, BUFFER, CONVERGENCE, CUSTOM, END, RANDOM_ERROR, REPAIR, START, TEST, TRANSPORT

PORT1 = 'port1'
PORTN = 'portn'
PORT1ERR = 'port1err'
PORT1OK = 'port1ok'

class ImageLoader:

    def __init__(self):
        self._assets_path = Path(__file__).parent / '../data/assets'
        self._node_types = [DIVERGENCE, BUFFER, CUSTOM, RANDOM_ERROR, TEST, CONVERGENCE, TRANSPORT, START, END, REPAIR]
        self._ports = [PORT1, PORTN, PORT1ERR, PORT1OK]
        self._images = {}
        self._load_images()
        self._load_ports()

    def _load_images(self):
        for node_type in self._node_types:
            path = (self._assets_path / (node_type + '.png')).resolve()
            img = Image.open(path)
            img = img.resize((NODE_WIDTH, NODE_HEIGHT))
            self._images[node_type] = ImageTk.PhotoImage(img)

    def _load_ports(self):
        for port in self._ports:
            path = (self._assets_path / (port + '.png')).resolve()
            img = Image.open(path)
            img = img.resize((int(NODE_WIDTH/3), int(NODE_HEIGHT/3)))
            self._images[port] = ImageTk.PhotoImage(img)

    def get_image(self, node_type: str):
        return self._images[node_type]