from sklearn import pipeline, preprocessing
import numpy as np


class CallableFunctionTransformer(pipeline.FunctionTransformer):
    def __call__(self, X):
        return super(CallableFunctionTransformer, self).transform(X)


def make_transformer(f, *args, **kwargs):
    return CallableFunctionTransformer(f, *args, **kwargs)


@make_transformer
def read_tifffile(filename: str):
    try:
        from tifffile import imread
    except ModuleNotFoundError:
        raise ModuleNotFoundError(f'You must install tifffile (pip install tifffile) for this to work.')
    return imread(filename)


def _scale(array):
    shape = array.shape
    array = preprocessing.minmax_scale(array.reshape(-1, 1), feature_range=(0, 255)).astype(np.uint8)
    return array.reshape(*shape)


@make_transformer
def tiff_to_rgb(image):
    rgb = image[:, :, 2], image[:, :, 1], image[:, :, 0]
    rgb = [_scale(i) for i in rgb]
    return np.stack(rgb, axis=-1)


file = r'C:\Users\ta46kof\PycharmProjects\feedback-prize\data\train_images\a07b1847_S2_10.tif'

from torchvision.transforms import ToTensor, ToPILImage
pipe = pipeline.make_pipeline(read_tifffile, tiff_to_rgb,
                              pipeline.FunctionTransformer(ToTensor()),
                              pipeline.FunctionTransformer(ToPILImage()))


pipe.transform([file]).show()
pipe[:2]
