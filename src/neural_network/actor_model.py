from typing import Callable

import tensorflow as tf
from tensorflow.python.keras import Model


class ActorModel(Model):

    def __init__(self, model: Model, critic_loss_function: Callable):
        self.critic_loss_function: Callable = critic_loss_function
        super().__init__(*args, **kwargs)

    def train_step(self, data):
        if self.critic_loss_function:

            # Unpack the data. Its structure depends on your model and
            # on what you pass to `fit()`.
            x, y = data

            with tf.GradientTape() as tape:
                y_pred = self(x, training=True)  # Forward pass
                # Compute the loss value
                # (the loss function is configured in `compile()`)
                loss = self.critic_loss_function(x)

            # Compute gradients
            trainable_vars = self.trainable_variables
            gradients = tape.gradient(loss, trainable_vars)
            # Update weights
            self.optimizer.apply_gradients(zip(gradients, trainable_vars))
            # Update metrics (includes the metric that tracks the loss)
            for metric in self.metrics:
                if metric.name == "loss":
                    metric.update_state(loss)
                else:
                    metric.update_state(y, y_pred)
            # Return a dict mapping metric names to current value
            return {m.name: m.result() for m in self.metrics}
        else:
            return super().train_step(data)
