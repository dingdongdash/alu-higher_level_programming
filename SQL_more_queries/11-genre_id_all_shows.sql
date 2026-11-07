-- Lists all the shows of hbtn_0d_tvshows with their genre ids, NULL when a show has no genre
-- Selects the show title and the genre id of every show, sorted by title then genre id
SELECT tv_shows.title, tv_show_genres.genre_id FROM tv_shows LEFT JOIN tv_show_genres ON tv_shows.id = tv_show_genres.show_id ORDER BY tv_shows.title ASC, tv_show_genres.genre_id ASC;
