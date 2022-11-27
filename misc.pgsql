-- CLEAR DATA
DELETE FROM "Venue"
WHERE id=2;
-- Venues
INSERT INTO "Venue" (name, genres, address, city, state, phone, website, facebook_link, seeking_talent, seeking_description, image_link)
VALUES ('The Musical Hop', '{"Jazz", "Reggae", "Swing", "Classical", "Folk"}', '1015 Folsom Street', 'San Francisco', 'CA','123-123-1234','https://www.themusicalhop.com','https://www.facebook.com/TheMusicalHop', True, 'We are on the lookout for a local artist to play every two weeks. Please call us.','https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60' );
INSERT INTO "Venue" (name, genres, address, city, state, phone, website, facebook_link, seeking_talent, image_link)
VALUES ('The Dueling Pianos Bar','{"Classical", "R&B", "Hip-Hop"}', '335 Delancey Street', 'New York', 'NY', '914-003-1132', 'https://www.theduelingpianos.com','https://www.facebook.com/theduelingpianos', False, 'https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80' );
INSERT INTO "Venue" (name, genres, address, city, state, phone, website, facebook_link, seeking_talent, image_link)
VALUES ('Park Square Live Music & Coffee', '{"Rock n Roll", "Jazz", "Classical", "Folk"}', '34 Whiskey Moore Ave', 'San Francisco', 'CA', '415-000-1234', 'https://www.parksquarelivemusicandcoffee.com', 'https://www.facebook.com/ParkSquareLiveMusicAndCoffee', False, 'https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80');
INSERT INTO "Venue" (name, genres, address, city, state, phone, website, facebook_link, seeking_talent, image_link)
VALUES ('Pink Panther', '{"Rock n Roll", "Jazz", "Classical", "Folk"}', '34 Whiskey Moore Ave', 'Oakland', 'CA', '415-000-1234', 'https://www.parksquarelivemusicandcoffee.com', 'https://www.facebook.com/ParkSquareLiveMusicAndCoffee', False, 'https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80');

UPDATE "Venue"
SET genres = '{"Jazz", "Reggae", "Swing", "Classical", "Folk"}'
WHERE id=3;
UPDATE "Venue"
SET genres = '{"Classical", "R&B", "Hip-Hop"}'
WHERE id=4;
UPDATE "Venue"
SET genres = '{"Rock n Roll", "Jazz", "Classical", "Folk"}'
WHERE id=5;
UPDATE "Venue"
SET genres = '{"Hip-Hop"}'
WHERE id=6;


-- Artist
INSERT INTO "Artist" (name, genres, city, state, phone, website, facebook_link, seeking_venue, seeking_description, image_link)
VALUES ('Guns N Petals','{"Rock n Roll"}','San Francisco','CA','326-123-5000','https://www.gunsnpetalsband.com','https://www.facebook.com/GunsNPetals',True,'Looking for shows to perform at in the San Francisco Bay Area!','https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80');
INSERT INTO "Artist" (name, genres, city, state, phone, website, facebook_link, seeking_venue, image_link)
VALUES ('Matt Quevedo','{"Jazz"}','New York','NY','300-400-5000','https://www.mattquevedo.com','https://www.facebook.com/mattquevedo',False,'https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80');
INSERT INTO "Artist" (name, genres, city, state, phone, website, facebook_link, seeking_venue, image_link)
VALUES ('The Wild Sax Band','{"Jazz", "Classical"}','San Francisco','CA','432-123-5000','https://www.thewildsaxband.com','https://www.facebook.com/TheWildSaxBand',False,'https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80');
INSERT INTO "Artist" (name, genres, city, state, phone, website, facebook_link, seeking_venue, image_link)
VALUES ('The Hood Band','{"Hip Hop", "Classical"}','Los Angeles','CA','432-123-5000','https://www.thewildsaxband.com','https://www.facebook.com/TheWildSaxBand',False,'https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80');


-- Shows matt=2 sax=3 gun=1 parksquare=5 pink=6 hop=3 dualing=4
INSERT INTO "Show" (venue_id, artist_id, start_time)
VALUES (3, 1, '2019-05-21 13:30:00.00-00');
INSERT INTO "Show" (venue_id, artist_id, start_time)
VALUES (5, 2, '2019-06-15T23:00:00.00-00');

SET timezone = 'Asia/Calcutta';
UPDATE "Show"
SET start_time = '2019-05-22 21:30:00.00'
WHERE id=1;
SELECT timezone('America/Los_Angeles', start_time) FROM "Show";
SELECT * FROM "Show"
-- Check Data
SELECT * FROM "Venue"
GROUP BY id, state, city
ORDER BY state;

SELECT * FROM "Artist";
SELECT * FROM "Show"

SELECT timezone('America/New_York', '2020-06-22 19:10:25');

SELECT "Show".artist_id, "Show".start_time, "Artist".name, "Artist".image_link
FROM "Show"
INNER JOIN "Artist" ON "Show".artist_id = "Artist".id;