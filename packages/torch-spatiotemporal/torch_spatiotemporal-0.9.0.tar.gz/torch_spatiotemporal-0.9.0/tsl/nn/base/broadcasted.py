import math
from typing import Union

import torch
from einops import rearrange
from torch import nn, Tensor
from torch.nn import init, functional as F
from tsl.nn.utils import maybe_cat_exog, get_layer_activation


class NodeWiseLinear(nn.Module):

    def __init__(self, in_channels: int, out_channels: int, n_nodes: int,
                 bias: bool = True,
                 device=None, dtype=None) -> None:
        factory_kwargs = {'device': device, 'dtype': dtype}
        super(NodeWiseLinear, self).__init__()
        self.in_channels = in_channels
        self.out_channels = out_channels
        self.n_nodes = n_nodes
        self.weight = nn.Parameter(
            torch.empty((n_nodes, in_channels, out_channels), **factory_kwargs)
        )
        if bias:
            self.bias = nn.Parameter(
                torch.empty(n_nodes, out_channels, **factory_kwargs)
            )
        else:
            self.register_parameter('bias', None)
        self.reset_parameters()

    def reset_parameters(self) -> None:
        node_weight = torch.Tensor(self.in_channels, self.out_channels)
        init.kaiming_uniform_(node_weight, a=math.sqrt(5))
        with torch.no_grad():
            self.weight[:] = node_weight
        if self.bias is not None:
            fan_in, _ = init._calculate_fan_in_and_fan_out(node_weight)
            bound = 1 / math.sqrt(fan_in) if fan_in > 0 else 0
            node_bias = torch.Tensor(self.out_channels)
            node_bias = node_bias.uniform_(-bound, bound)
            with torch.no_grad():
                self.bias[:] = node_bias

    def extra_repr(self) -> str:
        return 'in_channels={}, out_channels={}, n_nodes={}'.format(
            self.in_channels, self.out_channels, self.n_nodes
        )

    def forward(self, input: Tensor) -> Tensor:
        out = torch.einsum('btnf,nfc->btnc', input, self.weight)
        if self.bias is not None:
            out = out + self.bias
        return out


class NodeWiseConv1D(nn.Module):
    def __init__(self, in_channels: int, out_channels: int, n_nodes: int,
                 kernel_size: int,
                 stride: int = 1,
                 padding: Union[str, int] = 0,
                 dilation: int = 1,
                 bias: bool = True,
                 device=None, dtype=None):
        factory_kwargs = {'device': device, 'dtype': dtype}
        super(NodeWiseConv1D, self).__init__()

        self.in_channels = in_channels
        self.out_channels = out_channels
        self.n_nodes = n_nodes
        self.kernel_size = kernel_size

        self.stride = stride
        self.padding = padding
        self.dilation = dilation

        self.weight = nn.Parameter(
            torch.empty((n_nodes * out_channels, in_channels, kernel_size),
                        **factory_kwargs)
        )
        if bias:
            self.bias = nn.Parameter(
                torch.empty(n_nodes, out_channels, **factory_kwargs)
            )
        else:
            self.register_parameter('bias', None)
        self.reset_parameters()

    def reset_parameters(self) -> None:
        init.kaiming_uniform_(self.weight, a=math.sqrt(5))
        if self.bias is not None:
            fan_in, _ = init._calculate_fan_in_and_fan_out(self.weight)
            if fan_in != 0:
                bound = 1 / math.sqrt(fan_in)
                init.uniform_(self.bias, -bound, bound)

    def extra_repr(self) -> str:
        return f'{self.in_channels}, {self.out_channels}, ' \
               f'kernel_size={self.kernel_size}, n_nodes={self.n_nodes}'

    def forward(self, x):
        x = rearrange(x, 'b t n f -> b (n f) t')

        out = F.conv1d(x, weight=self.weight, bias=None, stride=self.stride,
                       dilation=self.dilation, groups=self.n_nodes,
                       padding=self.padding)

        out = rearrange(out, 'b (n f) t -> b t n f', n=self.n_nodes)

        if self.bias is not None:
            out = out + self.bias

        return out


class NodeWiseMLP(nn.Module):
    r"""Node-wise Multi-layer Perceptron encoder with optional linear readout.

    Args:
        input_size (int): Input size.
        hidden_size (int): Units in the hidden layers.
        output_size (int, optional): Size of the optional readout.
        exog_size (int, optional): Size of the optional exogenous variables.
        n_layers (int, optional): Number of hidden layers. (default: 1)
        activation (str, optional): Activation function. (default: `relu`)
    """
    def __init__(self, input_size: int, n_nodes: int, hidden_size: int,
                 output_size=None,
                 exog_size=None,
                 n_layers=1,
                 activation='relu'):
        super(NodeWiseMLP, self).__init__()
        self.activation = get_layer_activation(activation)
        if exog_size is not None:
            input_size += exog_size
        # first transformation with shared parameters
        layers = [nn.Linear(input_size, hidden_size), self.activation()]
        for _ in range(n_layers - 1):
            layers.append(NodeWiseLinear(hidden_size, hidden_size, n_nodes))
            layers.append(self.activation())
        layers.append(NodeWiseLinear(hidden_size,
                                     output_size or hidden_size, n_nodes))
        self.mlp = nn.Sequential(*layers)

    def forward(self, x, u=None):
        """"""
        x = maybe_cat_exog(x, u)
        out = self.mlp(x)
        return out
