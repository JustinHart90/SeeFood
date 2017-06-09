# SeeFood

Evolving the idea from Silicon valley of an image recognizer that will return micro nutrient counts for food logging.

The overall frame work will be one neural net to predict the label of an overall dish. Having chicken/ beef for example then this will be handed off to another model trained specially for the first label. This will return the label that is the closest match to a recipe image. Using this label  and the recipe we will then pull the mico-nutrient counts for the user.


# Data
I scraped images from fork-to-table API after requesting the micro nutrient data for categorized recipes.


<p align="center">
  <img src="src/img/0.jpg" width="350"/>
  <img src="src/img/2.jpg" width="350"/>
</p>

# Data Engineering

Flip those IMAGES!!!!!!!!!!

# Evoulition Theory Training

I started with 100 randomly generated models and went through 100 generations.

Here when the models didn’t correctly identify the food they became sick and died.
Not before they reproduced though.

So when the models reproduce they randomly switch there DNA sequence between the mates making a new model.

There is also random mutation involved in the DNA copy sequence.

Image of Family tree:
<p align="center">
  <img src="src/img/family.gif" width="350"/>

</p>


# Results
Here are where the results go for the best model

# API

I worked with the web-dev team to build them an API to return the micro nutrient counts for and image they provided.

# Web App
The web app is currently live at: https://dsi-seefood.herokuapp.com/

References:

Project:
http://dl.acm.org/citation.cfm?id=2654970

Evolution Theory:
https://arxiv.org/abs/1703.01041
