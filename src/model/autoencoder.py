import numpy as np
import torch
from pytorch_lightning import LightningModule
from tsa import TimeSeriesDataset
from tsa.model import AutoEncForecast

from src.transformations import extract_shot_series, resample_shot_series


class ShotsAutoEncForecast(AutoEncForecast, LightningModule):
    def __init__(self, dataset, config):
        self.dataset = dataset

        input_size = len(self.dataset.feature_cols)
        super().__init__(config, input_size)

        self.criterion = torch.nn.MSELoss()

        self.hparams.update(config)

    def training_step(self, batch, batch_nb):
        feature, y_hist, target = batch
        feature = torch.nan_to_num(feature)
        output = self.forward(feature, y_hist)

        loss = self.criterion.forward(output, target)
        self.log("loss", loss)
        # self.log_dict(logs, prog_bar=True, logger=True)
        return loss

    def validation_step(self, batch, batch_nb):
        feature, y_hist, target = batch
        feature = torch.nan_to_num(feature)
        output = self.forward(feature, y_hist)

        loss = self.criterion.forward(output, target)
        self.log("val_loss", loss)
        # self.log_dict(logs, prog_bar=True, logger=True)
        return loss

    def test_step(self, batch, batch_nb):
        feature, y_hist, target = batch
        feature = torch.nan_to_num(feature)
        output = self.forward(feature, y_hist)

        loss = self.criterion.forward(output, target)
        self.log("test_loss", loss)
        # self.log_dict(logs, prog_bar=True, logger=True)
        return loss

    def train_dataloader(self):
        self.train_iter, self.test_iter, n_features = self.dataset.get_loaders(
            batch_size=self.hparams["batch_size"], num_workers=4)
        return self.train_iter

    def val_dataloader(self):
        self.train_iter, self.test_iter, n_features = self.dataset.get_loaders(
            batch_size=self.hparams["batch_size"], num_workers=4)
        return self.test_iter

    def test_dataloader(self):
        self.train_iter, self.test_iter, n_features = self.dataset.get_loaders(
            batch_size=self.hparams["batch_size"], num_workers=4)
        return self.test_iter

    def get_n_params(self):
        model_parameters = filter(lambda tup: tup[1].requires_grad and "embedding" not in tup[0],
                                  self.named_parameters())

        params = sum([np.prod(p.size()) for name, p in model_parameters])
        return params

    def configure_optimizers(self):
        param_optimizer = list(self.named_parameters())
        no_decay = ['bias', 'alpha_activation', 'batchnorm', 'layernorm', "activation", "embedding",
                    'LayerNorm.bias', 'LayerNorm.weight',
                    'BatchNorm.bias', 'BatchNorm.weight']

        optimizer_grouped_parameters = [
            {'params': [p for name, p in param_optimizer \
                        if not any(key in name for key in no_decay) \
                        and "embeddings" not in name],
             'weight_decay': self.hparams['weight_decay']},
            {'params': [p for name, p in param_optimizer if any(key in name for key in no_decay)],
             'weight_decay': 0.0},
        ]

        optimizer = torch.optim.Adam(optimizer_grouped_parameters, lr=self.hparams["lr"])
        scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=self.hparams['lrs_step_size'], gamma=0.5)

        return {"optimizer": optimizer, 'lr_scheduler': scheduler, "monitor": "val_loss"}
