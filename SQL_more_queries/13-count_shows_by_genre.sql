-- Lists all the genres of hbtn_0d_tvshows with the number of shows linked to each
-- Selects each genre that has shows and its number of shows, sorted by number of shows descending then genre id
SELECT tv_genres.name AS genre, COUNT(*) AS number_of_shows FROM tv_genres INNER JOIN tv_show_genres ON tv_genres.id = tv_show_genres.genre_id GROUP BY tv_genres.id, tv_genres.name ORDER BY number_of_shows DESC, tv_genres.id ASC;
