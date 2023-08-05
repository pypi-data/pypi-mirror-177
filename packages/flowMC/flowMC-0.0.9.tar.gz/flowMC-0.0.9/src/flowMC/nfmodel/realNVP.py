from typing import Sequence, Callable
import jax
import jax.numpy as jnp
from flax import linen as nn
import numpy as np


class MLP(nn.Module):

    """
    Multi-layer perceptron in Flax.

    Parameters
    ----------
    features : list of int
        The number of features in each layer.
    activation : callable
        The activation function at each level
    use_bias : bool
        Whether to use bias in the layers.
    init_weight_scale : float
        The initial weight scale for the layers.
    kernel_init : callable
        The kernel initializer for the layers.
        We use a gaussian kernel with a standard deviation of `init_weight_scale` by default.
    """

    features: Sequence[int]
    activation: Callable = nn.relu
    use_bias: bool = True
    init_weight_scale: float = 1e-4
    kernel_i: Callable = jax.nn.initializers.variance_scaling

    def setup(self):
        self.layers = [
            nn.Dense(
                feat,
                use_bias=self.use_bias,
                kernel_init=self.kernel_i(self.init_weight_scale, "fan_in", "normal"),
            )
            for feat in self.features
        ]

    def __call__(self, x):
        for l, layer in enumerate(self.layers[:-1]):
            x = self.activation(layer(x))
        x = self.layers[-1](x)
        return x


class AffineCoupling(nn.Module):

    """
    Affine coupling layer. (Defined in the RealNVP paper https://arxiv.org/abs/1605.08803)
    We use tanh as the default activation function.

    Parameters
    ----------
    n_features : int
        The number of features in the input.
    n_hidden : int
        The number of hidden units in the MLP.
    mask : ndarray
        Alternating mask for the affine coupling layer.
    dt : float
        Scaling factor for the affine coupling layer.
    """

    n_features: int
    n_hidden: int
    mask: jnp.array
    dt: float = 1

    def setup(self):
        self.scale_MLP = MLP([self.n_features, self.n_hidden, self.n_features])
        self.translate_MLP = MLP([self.n_features, self.n_hidden, self.n_features])

    def __call__(self, x):
        s = self.mask * self.scale_MLP(x * (1 - self.mask))
        s = jnp.tanh(s)
        t = self.mask * self.translate_MLP(x * (1 - self.mask))
        s = self.dt * s
        t = self.dt * t
        log_det = s.reshape(s.shape[0], -1).sum(axis=-1)
        outputs = (x + t) * jnp.exp(s)
        return outputs, log_det

    def inverse(self, x):
        s = self.mask * self.scale_MLP(x * (1 - self.mask))
        s = jnp.tanh(s)
        t = self.mask * self.translate_MLP(x * (1 - self.mask))
        s = self.dt * s
        t = self.dt * t
        log_det = -s.reshape(s.shape[0], -1).sum(axis=-1)
        outputs = x * jnp.exp(-s) - t
        return outputs, log_det


class RealNVP(nn.Module):

    """

    RealNVP mode defined in the paper https://arxiv.org/abs/1605.08803.
    MLP is needed to make sure the scaling between layers are more or less the same.

    Parameters
    ----------
    n_layer : int
        The number of affine coupling layers.
    n_features : int
        The number of features in the input.
    n_hidden : int
        The number of hidden units in the MLP.
    dt : float
        Scaling factor for the affine coupling layer.
    base_mean : ndarray
        Mean of Gaussian base distribution
    base_cov : ndarray
        Covariance of Gaussian base distribution
    """

    n_layer: int
    n_features: int
    n_hidden: int
    dt: float = 1

    def setup(self):
        affine_coupling = []
        for i in range(self.n_layer):
            mask = np.ones(self.n_features)
            mask[int(self.n_features / 2) :] = 0
            if i % 2 == 0:
                mask = 1 - mask
            mask = jnp.array(mask)
            affine_coupling.append(
                AffineCoupling(self.n_features, self.n_hidden, mask, dt=self.dt)
            )
        self.affine_coupling = affine_coupling

        self.base_mean = self.variable(
            "variables", "base_mean", jnp.zeros, ((self.n_features))
        )
        self.base_cov = self.variable(
            "variables", "base_cov", jnp.eye, (self.n_features)
        )

    def __call__(self, x):
        log_det = jnp.zeros(x.shape[0])
        for i in range(self.n_layer):
            x, log_det_i = self.affine_coupling[i](x)
            log_det += log_det_i
        return x, log_det

    def inverse(self, x):
        x = (x-self.base_mean.value)/jnp.sqrt(jnp.diag(self.base_cov.value))
        log_det = jnp.zeros(x.shape[0])
        for i in range(self.n_layer):
            x, log_det_i = self.affine_coupling[self.n_layer - 1 - i].inverse(x)
            log_det += log_det_i
        return x, log_det

    def sample(self, rng_key, n_samples):
        gaussian = jax.random.multivariate_normal(
            rng_key, jnp.zeros(self.n_features), jnp.eye(self.n_features), shape=(n_samples,)
        )
        samples = self.inverse(gaussian)[0]
        samples = samples * jnp.sqrt(jnp.diag(self.base_cov.value)) + self.base_mean.value
        return samples # Return only the samples 

    def log_prob(self, x):
        x = (x-self.base_mean.value)/jnp.sqrt(jnp.diag(self.base_cov.value))
        y, log_det = self.__call__(x)
        log_det = log_det + jax.scipy.stats.multivariate_normal.logpdf(
            y, jnp.zeros(self.n_features), jnp.eye(self.n_features)
        )
        return log_det
