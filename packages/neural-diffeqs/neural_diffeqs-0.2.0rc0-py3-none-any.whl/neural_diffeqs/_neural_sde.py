
__module_name__ = "_neural_sde.py"
__doc__ = """Neural SDE module. Contains API-facing NeuralSDE class."""
__author__ = ", ".join(["Michael E. Vinyard"])
__email__ = ", ".join(["vinyard@g.harvard.edu"])
__version__ = "0.0.2"


# -- import packages: --------------------------------------------------------------------
from torch_nets import TorchNet


from ._base._neural_diffeq import NeuralDiffEq


# -- configure potential function: -------------------------------------------------------
class ConfigurePotential:
    def __init__(
        self,
        state_size,
        mu_potential,
        sigma_potential,
        mu_output_bias,
        sigma_output_bias,
    ):

        self.__dict__.update(locals())

    def init_state_size(self):
        for net in ["mu", "sigma"]:
            for io in ["in", "out"]:
                attr = "{}_{}_features".format(net, io)
                setattr(self, attr, self.state_size)

    def update_state_size(self):
        if self.mu_potential:
            self.mu_out_features = 1
        if self.sigma_potential:
            self.sigma_out_features = 1

    def update_output_bias(self):
        if self.mu_potential:
            self.mu_output_bias = False
        if self.sigma_potential:
            self.sigma_output_bias = False

    def __call__(self):
        self.init_state_size()
        self.update_state_size()
        self.update_output_bias()


def configure_potential(
    state_size,
    mu_potential,
    sigma_potential,
    mu_output_bias,
    sigma_output_bias,
):
    """ """
    config_potential = ConfigurePotential(
        state_size=state_size,
        mu_potential=mu_potential,
        sigma_potential=sigma_potential,
        mu_output_bias=mu_output_bias,
        sigma_output_bias=sigma_output_bias,
    )
    config_potential()

    return config_potential


# -- main class: -------------------------------------------------------------------------
class NeuralSDE(NeuralDiffEq):
    def __init__(
        self,
        state_size=50,
        mu_hidden=[],
        sigma_hidden=[],
        mu_activation="LeakyReLU",
        sigma_activation="LeakyReLU",
        mu_dropout=0,
        sigma_dropout=0,
        mu_bias=True,
        sigma_bias=True,
        mu_output_bias=True,
        sigma_output_bias=True,
        mu_potential=False,
        sigma_potential=False,
        noise_type: str = "general",
        sde_type: str = "ito",
        brownian_size=1,
    ):
        """
        Instantiate a NeuralSDE.

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

        dropout
            type: float
            default: 0

        potential_net
            If True, overrides out_dim and output_bias, setting them to 1 and
            False, respectively. If potential_net = True, mu_potential_net is 
            set to True, but not sigma_potential_net. For finer control and 
            alternative setups, use the keyword args.
            type: bool
            default: False

        input_bias
            type: bool
            default: True

        output_bias
            type: bool
            default: True

        brownian_size
            type: int
            default: 1

        mu_init
            type: float
            default: None

        sigma_init
            type: float
            default: None

        noise_type
            type: str
            default: "general"

        sde_type
            type: str
            default: "ito"

        kwargs:
        -------
        state_size
            mu_in_dim, mu_out_dim, sigma_in_dim, sigma_out_dim

        hidden
            mu_hidden, sigma_hidden

        activation_function
            mu_activation_function, sigma_activation_function

        input_bias
            mu_input_bias, sigma_input_bias

        output_bias
            mu_output_bias, sigma_output_bias

        dropout
            mu_dropout, sigma_dropout
            
        potential_net
            mu_potential_net, sigma_potential_net

        Keyword arguments are used in sets to replace the simpler, default args. For
        example, if state_size is given, this overrides the more detailed state_size
        keyword arguments, [mu_in_dim, mu_out_dim, sigma_in_dim, sigma_out_dim]. For
        all keyword arguments, the type is consistent with the simpler argument. All
        complex arguments must be passed in order to diverge from using the simpler
        argument.

        Returns:
        --------
        None
        """
        super(NeuralSDE, self).__init__()

        config = configure_potential(
            state_size,
            mu_potential,
            sigma_potential,
            mu_output_bias,
            sigma_output_bias,
        )
        mu = TorchNet(
            in_features=config.mu_in_features,
            out_features=config.mu_out_features,
            hidden=mu_hidden,
            activation=mu_activation,
            dropout=mu_dropout,
            bias=mu_bias,
            output_bias=config.mu_output_bias,
        )

        sigma = TorchNet(
            in_features=config.sigma_in_features,
            out_features=config.sigma_out_features,
            hidden=sigma_hidden,
            activation=sigma_activation,
            dropout=sigma_dropout,
            bias=sigma_bias,
            output_bias=config.sigma_output_bias,
        )
        self.__setup__(kwargs=locals())

    def _view_g_state(self, y):
        return y.view(y.shape[0], y.shape[1], self.brownian_size)

    def f(self, t, y0):
        """
        Drift method (term) of the NeuralSDE.

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
        f(y0)
            drift: Tensor of same shape as y0.
            type: torch.Tensor

        Notes:
        ------
        (1) t required syntactically though not functionally.

        Examples:
        ---------
        >>> func = NeuralSDE(state_size)
        >>> x_hat_f = func.f(None, x)
        """
        return self.mu_forward(self.mu, y0)

    def g(self, t, y0):
        """
        Diffusion method (term) of the NeuralSDE.

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
        g(y0)
            diffusion: Tensor of same shape as y0.
            type: torch.Tensor

        Notes:
        ------
        (1) t required syntactically though not functionally.
        
        Examples:
        ---------
        >>> func = NeuralSDE(state_size)
        >>> x_hat_g = func.g(None, x)
        """
        return self._view_g_state(self.sigma_forward(self.sigma, y0))
