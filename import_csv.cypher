USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM "file:///artist.csv" AS row
CREATE (:Artist {name: row.name, id: row.id, area: row.area, begin_area: row.begin_area, end_area: row.end_area, begin_date_year: row.begin_date_year, end_date_year: row.end_date_year});

// Create products
USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM "file:area.csv" AS row
CREATE (:Area {name: row.name, id: row.id, type: row.type});

CREATE INDEX ON :Artist(id);
CREATE INDEX ON :Artist(name);
CREATE INDEX ON :Area(id);
CREATE INDEX ON :Area(name);

USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM "file:///artist.csv" AS row
MATCH (artist: Artist {area: row.area})
MATCH (area: Area {: row.id})
MERGE (artist)-[:IS_FROM]->(area)
