import logging
from geodesic.tesseract.models import serve
import numpy as np
import time


class Model:
    def __init__(self):
        self.parameter = 20.0

    def inference(self, assets: dict, logger: logging.Logger) -> dict:
        logger.info("Starting inference")
        array_one = assets['test-input-one'].copy()
        array_two = assets['test-input-two'].copy()

        array_one[array_one >= 0.5] = 0
        array_two[array_two < 0.5] = 0

        array_three = array_one * array_two * self.parameter
        array_three = array_three.astype(np.uint8)
        time.sleep(2)  # just so the messages in the validator done fly by so quickly
        logger.info("inference completed")

        return {
            'test-output-one': array_one,
            'test-output-two': array_two,
            'test-output-three': array_three
        }

    def get_model_info(self):
        return {
            'inputs': [
                {
                    'name': 'test-input-one',
                    'dtype': '<f4',
                    'shape': [1, 4, 1024, 1024]
                },
                {
                    'name': 'test-input-two',
                    'dtype': '<f4',
                    'shape': [1, 1, 1024, 1024]
                }
            ],
            'outputs': [
                {
                    'name': 'test-output-one',
                    'dtype': '<f4',
                    'shape': [1, 4, 1024, 1024]
                },
                {
                    'name': 'test-output-two',
                    'dtype': '<f4',
                    'shape': [1, 1, 1024, 1024]
                },
                {
                    'name': 'test-output-three',
                    'dtype': '|u2',
                    'shape': [1, 4, 1024, 1024]
                }
            ]
        }


if __name__ == '__main__':
    model = Model()
    serve(model.inference, model.get_model_info)
