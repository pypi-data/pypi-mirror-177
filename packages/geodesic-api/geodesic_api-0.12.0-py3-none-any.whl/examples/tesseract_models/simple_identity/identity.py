import logging
import numpy as np
from geodesic.tesseract.models import serve


def inference(assets: dict, logger: logging.Logger) -> dict:
    # get the numpy array
    array = assets['viirs']

    # get the element count
    n = array.size

    return {
        'identity': array.copy(),
        'count': np.array([n]).reshape((1, 1, 1, 1))
    }


if __name__ == '__main__':
    serve(inference)
