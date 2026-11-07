-- Converts the database hbtn_0c_0, its table first_table and the field name to UTF8 (utf8mb4, utf8mb4_unicode_ci)
-- Converts the database hbtn_0c_0 to utf8mb4 with the utf8mb4_unicode_ci collation
ALTER DATABASE hbtn_0c_0 CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
-- Converts the table first_table and its field name to utf8mb4 with the utf8mb4_unicode_ci collation
ALTER TABLE hbtn_0c_0.first_table CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
