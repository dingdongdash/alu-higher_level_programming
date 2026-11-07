-- Lists all the genres of the show Dexter in hbtn_0d_tvshows
-- Selects the names of the genres linked to Dexter, sorted by name
SELECT tv_genres.name FROM tv_genres INNER JOIN tv_show_genres ON tv_genres.id = tv_show_genres.genre_id INNER JOIN tv_shows ON tv_show_genres.show_id = tv_shows.id WHERE tv_shows.title = 'Dexter' ORDER BY tv_genres.name ASC;
