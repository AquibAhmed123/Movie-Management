from flask import Flask, render_template, request, redirect, flash, url_for
from flask_mysqldb import MySQL
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = ""
app.config['MYSQL_DB'] = "movie_database"

mysql = MySQL(app)

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/register', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        title = request.form['title']
        release_year = request.form['release_year']
        genre = request.form['genre']
        plot = request.form['plot']
        cast = request.form['cast']
        director = request.form['director']
        user_rating = request.form['user_rating']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO movie (title, release_year, genre,plot,cast,director,user_rating) VALUES(%s, %s, %s, %s, %s,%s,%s)", (title, release_year, genre,plot,cast,director,user_rating))
        mysql.connection.commit()
        cur.close()
        flash('New Movie added successfully!')
        return redirect(url_for('home'))

    return render_template('add_movie.html')

@app.route('/movies', methods=['GET','POST'])
def movies():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM movie")
    movieDetails = cur.fetchall()
    cur.close()
    return render_template('movies.html', movieDetails=movieDetails)

@app.route('/movie/<int:movie_id>', methods=['GET','POST'])
def movie_details(movie_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM movie WHERE id = %s", (movie_id,))
    movie = cur.fetchone()
    cur.close()

    if movie:
        # Return details for the selected movie
        return render_template('movie_details.html', movie=movie)
    
@app.route('/delete', methods=['GET', 'POST'])
def del_movies():
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, title, genre FROM movie")
    movies = cur.fetchall()
    cur.close()

    if request.method == 'POST':
        # If a movie is selected for deletion
        movie_id = request.form['movie_id']
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM movie WHERE id = %s", (movie_id,))
        mysql.connection.commit()
        cur.close()
        flash('Movie deleted successfully')
        return redirect(url_for('home'))

    return render_template('delete_movie.html', movies=movies)




if __name__ == '__main__':
    app.run(debug=True)