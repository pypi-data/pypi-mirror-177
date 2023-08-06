
__module_name__ = "_neural_diffeq.py"
__doc__ = """Base classes for all neural diffeq models."""
__author__ = ", ".join(["Michael E. Vinyard"])
__email__ = ", ".join(["vinyard@g.harvard.edu"])
__version__ = "0.0.2"


# -- import packages: --------------------------------------------------------------------
from abc import ABC
import torch


# -- import local dependencies: ----------------------------------------------------------
from ._configure_forward import configure_forward


# -- main module class: ------------------------------------------------------------------
class NeuralDiffEq(ABC, torch.nn.Module):
    """
    Abstract base class for NeuralDiffEq. Most shared common ancestor class.
    Common to all NDE functions.
    Note: When you subclass this, call self.__setup__(locals) within __init__
    """    
    def __parse__(self, kwargs, ignore=["self", "__class__"]):
        """automatically parse locals() passed to the kwargs argument."""
        for k, v in kwargs.items():
            if not k in ignore:
                setattr(self, k, v)

    def __configure__(self):
        """
        configure the forward function for one or more neural networks
        (base case: mu, sigma). If not a potential_net, simply pass the
        torch.nn.Module through the network.
        """
        for network in ["mu", "sigma"]:
            configure_forward(self, network)

    def __setup__(self, kwargs, ignore=["self", "__class__"]):
        """Call from within __init__"""
        self.__parse__(kwargs, ignore)
        self.__configure__()

    def potential(self, net, x):
        """Pass through potential net"""
        x = x.requires_grad_()
        return net(x)

    def _forward(self, net, x):
        """Pass through forward net"""
        return net(x)

    def potential_gradient(self, net, x):
        """
        Pass through the potential net to calculate the empirically-derived potential
        and subsequently calculate the gradient of the potential with respect to the
        input points.
        """
        ψ = self.potential(net, x)
        return torch.autograd.grad(ψ, x, torch.ones_like(ψ), create_graph=True)[0]
