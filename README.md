# SeeFood

Evolving the idea from Silicon valley of an image recognizer that will return micro nutrient counts for food logging.

The overall frame work will be one neural net to predict the label of an overall dish. Having chicken/ beef for example then this will be handed off to another model trained specially for the first label. This will return the label that is the closest match to a recipe image. Using this label  and the recipe we will then pull the mico-nutrient counts for the user.

# Training

I will be training the neural nets by not touching any of the hyperparameters and only using the models that survive. Using evolution theory to keep only the models who correctly identify images that wont destroy them.


References:
http://dl.acm.org/citation.cfm?id=2654970
