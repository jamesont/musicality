COPY (SELECT * FROM artist) TO '/Users/yeshewingerd/Galvanize/q3_project/musicbrainz_database/import/artist.csv' WITH CSV header;
COPY (SELECT * FROM area) TO '/Users/yeshewingerd/Galvanize/q3_project/musicbrainz_database/import/area.csv' WITH CSV header;
COPY (SELECT * FROM label) TO '/Users/yeshewingerd/Galvanize/q3_project/musicbrainz_database/import/label.csv' WITH CSV header;

-- Joins release_group type name (album,EP, etc.) from release_group_primary_type table with release_group table
-- COPY (SELECT release_group.*, release_group_primary_type.name AS type_name FROM release_group
--       JOIN release_group_primary_type ON release_group.type = release_group_primary_type.id) TO '/Users/yeshewingerd/Galvanize/q3_project/musicbrainz_database/import/release_group.csv' WITH CSV header;

-- does same as above but adds artist name as a column
COPY (SELECT release_group.*, release_group_primary_type.name AS type_name, artist.name AS artist_name FROM release_group
      JOIN release_group_primary_type ON release_group.type = release_group_primary_type.id
      JOIN artist ON release_group.artist_credit = artist.id) TO '/Users/yeshewingerd/Galvanize/q3_project/musicbrainz_database/import/release_group.csv' WITH CSV header;

-- Joins release_group to label to allow us not to use the release node since there are too many repetitive nodes created from the release table
COPY (select artist.id as a_id, artist.name as a_name, release_group.id as rg_id, release_group.name as rg_name, label.id as l_id, label.name as l_name
      from release
      join artist on release.artist_credit = artist.id
      join release_label on release_label.release = release.id
      join release_group on release.release_group = release_group.id
      join label on release_label.label = label.id) TO '/Users/yeshewingerd/Galvanize/q3_project/musicbrainz_database/import/release_group-label.csv' WITH CSV header;

-- Joins l_artist_release to corresponding release_group so that we can create a relationship between contributors besides primary artist to a release_group
  COPY(select artist.id as artist_id, link_type.id as link_type_id, link_type.name as link_type_name, release.id as release_id, release.release_group
      from l_artist_release lar
      join artist on lar.entity0 = artist.id
      join release on lar.entity1 = release.id
      join link on lar.link = link.id
      join link_type on link.link_type = link_type.id) TO '/Users/yeshewingerd/Galvanize/q3_project/musicbrainz_database/import/l_artist_release-release_group.csv' WITH CSV header;
