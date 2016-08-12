USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM "file:///artist.csv" AS row
CREATE (:artist {name: row.name, id: row.id, area: row.area, begin_area: row.begin_area, end_area: row.end_area, begin_date_year: row.begin_date_year, end_date_year: row.end_date_year});

# Create area
USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM "file:///area.csv" AS row
CREATE (:area {name: row.name, id: row.id, type: row.type, begin_date_year: row.begin_date_year, end_date_year: row.end_date_year});

# Create label
USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM "file:///label.csv" AS row
CREATE (:label {name: row.name, id: row.id, begin_date_year: row.begin_date_year, end_date_year: row.end_date_year, area: row.area});

# Create release_group
USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM "file:///release_group.csv" AS row
CREATE (:release_group {name: row.name, id: row.id, artist_credit: row.artist_credit, artist_name: row.artist_name, type: row.type_name});



CREATE INDEX ON :artist(name);
CREATE INDEX ON :artist(id);

CREATE INDEX ON :area(id);
CREATE INDEX ON :area(name);

CREATE INDEX ON :label(name);
CREATE INDEX ON :label(id);

CREATE INDEX ON :release_group(name);
CREATE INDEX ON :release_group(id);
CREATE INDEX ON :release_group(type);

USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM "file:///artist.csv" AS row
MATCH (artist: artist {id: row.id})
MATCH (area: area {id: row.area})
MERGE (artist)-[:IS_FROM]->(area);

USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM "file:///release_group.csv" AS row
MATCH (artist: artist {id: row.artist_credit})
MATCH (release_group: release_group {id: row.id})
MERGE (artist)-[:RELEASED]->(release_group);

USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM "file:///label.csv" AS row
MATCH (label: label {id: row.id})
MATCH (area: area {id: row.area})
MERGE (label)-[:LOCATED_IN]->(area);

USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM "file:///release_group-label.csv" AS row
MATCH (release_group: release_group {id: row.rg_id})
MATCH (label: label {id: row.l_id})
MERGE (release_group)-[:RELEASED_ON]->(label);

USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM "file:///l_artist_release-release_group.csv" AS row
MATCH (contributor: artist {id: row.artist_id})
MATCH (release_group: release_group {id: row.release_group})
MERGE (contributor)-[:CONTRIBUTED_TO {role: row.link_type_name}]->(release_group);

# We decided not to use this cypher query builder
entities = {'area': {
                    'properties': ['id', 'name', 'type', 'begin_date_year', 'end_date_year'],
                    'indices': ['name'],
                    'relationships': []},
            'artist': {
                    'properties': ['id', 'name', 'begin_date_year', 'end_date_year', 'type', 'area','begin_area', 'end_area'],
                    'indices': ['name'],
                    'relationships': [{'filename': 'artist', 'node1': 'artist', 'node2': 'area', 'merge_name':'IS_FROM' }]},
            'release': {
                    'properties': ['id', 'name', 'artist_credit', 'release_group'],
                    'indices': ['name'],
                    'relationships': [{'filename': 'release', 'node1': 'artist_credit', 'node2': 'name', 'merge_name':'RELEASED' }]}
            }

# Prints cypher commands to build all entities(nodes) and corresponding properties
for entity, props_indices_rels in entities.items():

    node = "(:{entity} {{".format(entity=entity)
    props = ''

    for idx, prop in enumerate(props_indices_rels['properties']):
        if idx == len(props_indices_rels['properties']) -1:
            props += '{prop}: row.{prop}}});'.format(prop=prop)
        else:
            props += '{prop}: row.{prop}, '.format(prop=prop)

    node_and_props = node + props

    print("USING PERIODIC COMMIT\nLOAD CSV WITH HEADERS FROM 'file:///{filename}.csv' AS row\nCREATE {node_and_props}\n".format(filename=entity, node_and_props=node_and_props))


# Prints cypher commands to create indices in neo4j
for entity, props_indices_rels in entities.items():

    for prop in props_indices_rels['indices']:
        print('CREATE INDEX ON :{node}({prop});'.format(node=entity, prop=prop))

# Prints cypher commands to create relationships between nodes

for entity, props_indices_rels in entities.items():

    for idx, relationship in enumerate(props_indices_rels['relationships']):

        print("\nUSING PERIODIC COMMIT\nLOAD CSV WITH HEADERS FROM 'file:///{filename}.csv' AS row\nMATCH ({node1}: {node1} {{{node1}: row.{node1}}})\nMATCH ({node2}: {node2} {{{node2}: row.{node2}}})\nMERGE ({node1})-[:{merge_name}]->({node2})".format(filename=relationship['filename'], node1=relationship['node1'], node2=relationship['node2'],merge_name=relationship['merge_name']))
