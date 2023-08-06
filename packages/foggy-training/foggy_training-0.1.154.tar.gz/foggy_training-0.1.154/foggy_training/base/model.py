from typing import Union

import pytorch_lightning as pl
from attr import define, field
from torch import optim
from torchinfo import summary
from torchmetrics import MetricCollection

from foggy_training.base.lookups import get_loss_fun, get_metric_fun


@define
class ForwardResult:
    pred = field()
    true = field(default=None)
    loss = field(default=None)


class LightningExtended(pl.LightningModule):

    """

    The Lightning Extended Modules provides some defaults for training and validation sets. You may do the following:

    ```python
    from foggy_training import models
    x = [[1., 1.], [2., 2.], [3., 3.]]
    y = [1., 2., 3.]
    data = {'x': x, 'y': y}
    model = models.LinearRegression(n_inputs=2)
    model.fit(data, epochs=20)
    ```

    """
    def __init__(self, loss: Union[str, callable], lr: float = None, metrics=None):
        """

        loss: string or callable. if string, must match the name of torch.nn.functional losses
        lr: float, learning rate
        metrics: list of torchmetrics

        """
        super(LightningExtended, self).__init__()
        self.loss = get_loss_fun(loss)
        self.lr = lr if lr is not None else 1e-3
        metrics = [] if metrics is None else metrics
        assert isinstance(metrics, list), 'metrics must be list of metrics'
        metrics = [get_metric_fun(m) for m in metrics]
        metrics = MetricCollection(metrics)
        self.train_metrics = metrics.clone(prefix='train_')
        self.val_metrics = metrics.clone(prefix='val_')

    def shared_step(self, batch) -> ForwardResult:
        result = self(batch)
        return result

    def training_step(self, batch, batch_idx):
        result = self.shared_step(batch)
        loss = self.loss(result.pred, result.true)
        logs = dict(loss=loss)
        metrics = self.train_metrics(result.pred, result.true)
        logs = {**logs, **metrics}
        self.log_dict(logs, prog_bar=True, on_epoch=True)
        return loss

    def validation_step(self, batch, batch_idx):
        result = self.shared_step(batch)
        loss = self.loss(result.pred, result.true)
        logs = dict(val_loss=loss)
        metrics = self.val_metrics(result.pred, result.true)
        logs = {**logs, **metrics}
        self.log_dict(logs, prog_bar=True, on_step=False, on_epoch=True)

    def predict_step(self, batch, batch_idx, dataloader_idx=0):
        return self.shared_step(batch).pred

    def configure_optimizers(self):
        return optim.AdamW(filter(lambda p: p.requires_grad, self.parameters()), lr=self.lr)

    def summary(self, depth: int = 3,
                col_names=('num_params', 'trainable'),
                row_settings=('var_names', ), **kwargs):
        print(summary(self, depth=depth,
                      col_names=col_names,
                      row_settings=row_settings,
                      **kwargs))
