import movie
import fresh_tomatoes
toy_story = movie.Movie("Toy Story",
						"Story of a boy and his toys that come to life",
						"https://upload.wikimedia.org/wikipedia/en/1/13/Toy_Story.jpg",
						"https://www.youtube.com/watch?v=KYz2wyBy3kc")


movies = [toy_story]
#fresh_tomatoes.open_movies_page(movies)
print(movie.Movie.__doc__)
print(movie.Movie.__name__)
print(movie.Movie.__module__)
