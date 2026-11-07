-- Lists all the shows of hbtn_0d_tvshows without a genre linked
-- Selects the show title and the NULL genre id of the shows without genre, sorted by title then genre id
SELECT tv_shows.title, tv_show_genres.genre_id FROM tv_shows LEFT JOIN tv_show_genres ON tv_shows.id = tv_show_genres.show_id WHERE tv_show_genres.genre_id IS NULL ORDER BY tv_shows.title ASC, tv_show_genres.genre_id ASC;
