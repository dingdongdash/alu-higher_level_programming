-- Lists all shows without the genre Comedy, sorted ascending by show title
-- Lists show titles that are not linked to Comedy
SELECT tv_shows.title FROM tv_shows WHERE tv_shows.id NOT IN (SELECT tv_show_genres.show_id FROM tv_show_genres INNER JOIN tv_genres ON tv_show_genres.genre_id = tv_genres.id WHERE tv_genres.name = 'Comedy') ORDER BY tv_shows.title ASC;
