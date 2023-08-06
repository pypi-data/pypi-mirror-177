
__module_name__ = "_neural_ode.py"
__doc__ = """Neural ODE module. Contains API-facing NeuralODE class."""
__author__ = ", ".join(["Michael E. Vinyard"])
__email__ = ", ".join(["vinyard@g.harvard.edu"])
__version__ = "0.0.2"


# -- import packages: --------------------------------------------------------------------
from torch_nets import TorchNet
from typing import Union


# -- import local dependencies: ----------------------------------------------------------
from ._base._neural_diffeq import NeuralDiffEq


# -- API-facing class: -------------------------------------------------------------------
class NeuralODE(NeuralDiffEq):
    """note: forward is a required method for torchdiffeq.odeint"""
    def __init__(
        self,
        state_size: int,
        hidden: list = [],
        activation: str = "LeakyReLU",
        dropout: Union[float, list] = 0,
        bias: bool = True,
        output_bias: bool = True,
        potential_net: bool = False,
    ):
        """
        Instantiate a NeuralODE.

        Parameters:
        -----------
        state_size
            type: int

        hidden
            type: dict
            default: {1: [200, 200]}

        activation_function:
            type: 'torch.nn.modules.activation.<func>'
            default: torch.nn.Tanh,

        potential_net
            If True, overrides out_dim and output_bias, setting them to 1 and False, respectively.
            type: bool
            default: False

        dropout
            type: float
            default: 0

        input_bias
            type: bool
            default: True

        output_bias
            type: bool
            default: True

        Returns:
        --------
        None
        
        Notes:
        ------
        """
        
        super(NeuralODE, self).__init__()
        
        if potential_net:
            out_features, output_bias = 1, False
        else:
            out_features = state_size
        
        self.mu = TorchNet(
            in_features=state_size,
            out_features=out_features,
            hidden=hidden,
            activation=activation,
            dropout=dropout,
            bias=bias,
            output_bias=output_bias,
        )
        self.__setup__(kwargs=locals())

    def forward(self, t, y0):
        """
        Forward (drift, deterministic) method, core to NeuralODE.

        Parameters:
        -----------
        t
            time tensor of shape: (t,)
            type: torch.Tensor
            default: None

        y0
            state vector
            type: torch.Tensor

        Returns:
        --------
        forward(y0)
            drift: Tensor of same shape as y0.
            type: torch.Tensor

        Notes:
        ------
        (1) t required syntactically though not functionally.

        Examples:
        ---------
        >>> func = NeuralODE(state_size)
        >>> x_hat_f = func.forward(None, x)
        """
        return self.mu_forward(self.mu, y0)