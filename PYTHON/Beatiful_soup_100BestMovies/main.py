from bs4 import BeautifulSoup
import requests

response = requests.get("https://www.empireonline.com/movies/features/best-movies-2/")
yc_website = BeautifulSoup(response.text,"html.parser")

movie_dict = {int(item.getText().split(")")[0]):item.getText().split(")")[1] for item in yc_website.select(selector = ".listicle_listicle__item__OCDTx .listicleItem_listicle-item__title__hW_Kn")}
movie_dict_keys = list(movie_dict.keys())
movie_dict_keys.sort()
sorted_movie_dict = {i: movie_dict[i] for i in movie_dict_keys}

with open("movies.txt","w") as file:
  for key in sorted_movie_dict:
      file.write(str(key)+")"+sorted_movie_dict[key]+"\n")



