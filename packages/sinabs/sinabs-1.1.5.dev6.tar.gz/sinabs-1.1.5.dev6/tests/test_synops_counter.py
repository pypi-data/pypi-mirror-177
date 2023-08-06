import numpy as np
import torch
from torch import nn

from sinabs import SNNAnalyzer, SynOpCounter
from sinabs.layers import IAFSqueeze, NeuromorphicReLU


class Model(torch.nn.Sequential):
    def __init__(self):
        super().__init__(
            torch.nn.Conv2d(
                in_channels=1, out_channels=8, kernel_size=(3, 3), bias=False
            ),
            NeuromorphicReLU(),
            torch.nn.AvgPool2d(kernel_size=(2, 2), stride=(2, 2)),
            torch.nn.Conv2d(
                in_channels=8, out_channels=12, kernel_size=(3, 3), bias=False
            ),
            NeuromorphicReLU(),
            torch.nn.AvgPool2d(kernel_size=(2, 2), stride=(2, 2)),
            torch.nn.Conv2d(
                in_channels=12, out_channels=12, kernel_size=(3, 3), bias=False
            ),
            NeuromorphicReLU(),
            torch.nn.AvgPool2d(kernel_size=(2, 2), stride=(2, 2)),
            torch.nn.Dropout(0.5),
            torch.nn.Flatten(),
            torch.nn.Linear(432, 10, bias=False),
            NeuromorphicReLU(fanout=0),
        )


class TinyModel(torch.nn.Module):
    def __init__(self, quantize):
        super().__init__()
        self.linear = torch.nn.Linear(5, 2, bias=False)
        self.relu = NeuromorphicReLU(fanout=2, quantize=quantize)

        self.linear.weight.data = torch.tensor(
            [[1.2, 1.0, 1.0, 3.0, -2.0], [1.2, 1.0, 1.0, 2.0, -10.0]]
        )

    def forward(self, x):
        return self.relu(self.linear(x))


def test_parsing():
    model = Model()
    loss = SynOpCounter(model.modules())

    assert len(loss.modules) == 3


def test_loss():
    model = TinyModel(quantize=False)
    criterion = SynOpCounter(model.modules())
    input = torch.tensor([[0.5, 0.5, 0.5, 0.5, 0.5]])
    model(input)
    loss = criterion()

    assert np.allclose(loss.item(), 4.2)


def test_loss_quantized():
    model = TinyModel(quantize=True)
    criterion = SynOpCounter(model.modules())
    input = torch.tensor([[0.5, 0.5, 0.5, 0.5, 0.5]])
    model(input)
    loss = criterion()

    assert np.allclose(loss.item(), 4.0)


def test_layer_synops():
    model = Model()
    criterion = SynOpCounter(model.modules(), sum_activations=False)
    input = torch.rand([1, 1, 64, 64])
    model(input)
    loss = criterion()

    assert len(loss) == 3


def test_snn_synops_counter():
    model = nn.Sequential(nn.Conv2d(1, 5, kernel_size=2), IAFSqueeze(batch_size=1))
    input_ = torch.tensor([[[[0, 0, 0], [0, 3, 0], [0, 0, 0]]]]).float()
    analyser = SNNAnalyzer(model)
    model(input_)
    model_stats = analyser.get_model_statistics()

    # 3 spikes, 2x2 kernel, 5 channels
    assert model_stats["synops"] == 60


def test_snn_analyser_statistics():
    batch_size = 3
    num_timesteps = 10
    model = nn.Sequential(
        nn.Conv2d(1, 2, kernel_size=2, bias=False),
        IAFSqueeze(batch_size=batch_size),
        nn.Conv2d(2, 3, kernel_size=2, bias=False),
        IAFSqueeze(batch_size=batch_size),
    )

    analyser = SNNAnalyzer(model)
    input_ = torch.rand((batch_size, num_timesteps, 1, 4, 4)) * 100
    input_flattended = input_.flatten(0, 1)
    output = model(input_flattended)
    layer_stats = analyser.get_layer_statistics()
    model_stats = analyser.get_model_statistics()

    # spiking layer checks
    assert (
        layer_stats["3"]["firing_rate"] == output.mean()
    ), "The output mean should be equivalent to the firing rate of the last spiking layer"
    assert (
        torch.cat(
            (
                layer_stats["1"]["firing_rate_per_neuron"].ravel(),
                layer_stats["3"]["firing_rate_per_neuron"].ravel(),
            )
        ).mean()
        == model_stats["firing_rate"]
    ), "Mean of layer 1 and 3 firing rates is not equal to calculated model firing rate."

    # parameter layer checks
    layer_stats["0"]["synops"] == input_.mean(0).sum() * np.product(
        model[0].kernel_size
    ) * model[0].out_channels
    assert layer_stats["0"]["num_timesteps"] == num_timesteps
    assert layer_stats["2"]["num_timesteps"] == num_timesteps
    assert (
        model_stats["synops"] == layer_stats["0"]["synops"] + layer_stats["2"]["synops"]
    )


def test_snn_analyser_does_not_depend_on_batch_size():
    batch_size_1 = 5
    num_timesteps = 10
    linear1 = nn.Linear(3, 4, bias=False)
    analyser = SNNAnalyzer(linear1)
    input_ = torch.ones((batch_size_1, num_timesteps, 3)) * 10
    linear1(input_)
    model_stats_batch_size_1 = analyser.get_model_statistics()

    batch_size_2 = 10
    linear2 = nn.Linear(3, 4, bias=False)
    analyser = SNNAnalyzer(linear2)
    input_ = torch.ones((batch_size_2, num_timesteps, 3)) * 10
    linear2(input_)
    model_stats_batch_size_2 = analyser.get_model_statistics()

    assert model_stats_batch_size_1["synops"] == model_stats_batch_size_2["synops"]
