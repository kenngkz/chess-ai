from tensorflow import keras

class ActorCriticAI:
    
    def __init__(self, actor_model: keras.Model, critic_model: keras.Model):
        self.actor = actor_model
        self.critic = critic_model

    def predict(self, obs):
        return {"actor": self.actor.predict(obs), "critic": self.critic.predit(obs)}