from .KerasNeuralNetwork import KerasNeuralNetwork
from .utils import Decoder_FEN, Tiler


def get_fen_from_image(image_path, end_of_row='/', black_view=False) -> str:
    decoder = Decoder_FEN()
    net = KerasNeuralNetwork()
    net.load_model('./saved_models/november_model')
    tiler = Tiler()
    tiles = tiler.get_tiles(image_path=image_path)
    predictions = net.predict(tiles=tiles)
    fen = decoder.fen_decode(figures=predictions, end_of_row=end_of_row, black_view=black_view)
    return fen