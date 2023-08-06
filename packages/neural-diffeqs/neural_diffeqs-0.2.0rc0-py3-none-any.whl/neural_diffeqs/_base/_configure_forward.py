
__module_name__ = "_configure_forward.py"
__doc__ = """
          Define whether a the forward function should be handled by a potential forward
          integration or regular forward
          """
__author__ = ", ".join(["Michael E. Vinyard"])
__email__ = ", ".join(["vinyard@g.harvard.edu"])
__version__ = "0.0.2"


# -- import packages: --------------------------------------------------------------------
import torch


# -- API-facing supporting functions: ----------------------------------------------------
def is_potential_net(net):
    """
    Indicate if a neural network is a 'potential net'.
    
    Parameters:
    -----------
    net
        type: torch.nn.Module
        
    Returns:
    --------
    indicator
        type: bool
    """
    return list(net.parameters())[-1].shape[0] == 1


def is_forward_net(net):
    """
    Indicate if a neural network is a 'forward net'.
    
    Parameters:
    -----------
    net
        type: torch.nn.Module
        
    Returns:
    --------
    indicator
        type: bool
    """
    in_features = net[0][0].in_features
    out_features = net[-1][-1].out_features
    return in_features == out_features


# -- hidden supporting functions: --------------------------------------------------------
def _set_forward_net_pass(module: torch.nn.Module, network: str):
    """"""
    setattr(module, "{}_network_type".format(network), "forward")
    setattr(module, "{}_forward".format(network), getattr(module, "_forward"))


def _set_potential_net_pass(net: torch.nn.Sequential, module: torch.nn.Module, network: str):
    """"""
    if is_potential_net(net):
        setattr(module, "{}_network_type".format(network), "potential")
    else:
        setattr(module, "{}_network_type".format(network), "unspecified_potential")

    setattr(module, "{}_forward".format(network), getattr(module, "potential_gradient"))


# -- main module function: ---------------------------------------------------------------
def configure_forward(module: torch.nn.Module, network: str):
    """based on the passed network, forward function is defined as a module attribute"""
    if hasattr(module, network):
        net = getattr(module, network)
        if is_forward_net(net):
            _set_forward_net_pass(module, network)
        else:
            _set_potential_net_pass(net, module, network)
