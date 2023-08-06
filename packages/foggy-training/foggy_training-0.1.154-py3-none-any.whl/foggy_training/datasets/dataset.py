from typing import Union

from attr import define
from sklearn.pipeline import Pipeline, FeatureUnion
from torch.utils.data import Dataset


class FTDataset(Dataset):
    def __init__(self, items,
                 get_x: Union[callable, Pipeline, FeatureUnion],
                 get_y: Union[callable, Pipeline, FeatureUnion]):
        self.items = items
        self.get_x = get_x
        self.get_y = get_y

    def __len__(self):
        return len(self.items)

    def __getitem__(self, idx):
        item = self.items[idx]

        if isinstance(self.get_x, (Pipeline, FeatureUnion)):
            x = self.get_x.transform([item])
        else:
            x = self.get_x(item)
        if isinstance(self.get_y, (Pipeline, FeatureUnion)):
            y = self.get_y.transform([item])
        else:
            y = self.get_y(item)

        return x, y


@define
class DatasetBlueprint:
    get_x: Union[callable, Pipeline, FeatureUnion]
    get_y: Union[callable, Pipeline, FeatureUnion]

    def __call__(self, items):
        return FTDataset(items, self.get_x, self.get_y)
