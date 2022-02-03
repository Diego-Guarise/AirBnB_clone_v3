CREATE TABLE cities (
  id varchar(60) NOT NULL,
  created_at datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  name varchar(128) NOT NULL,
  state_id varchar(60) NOT NULL,
  PRIMARY KEY (id),
  KEY state_id (state_id),
  CONSTRAINT cities_ibfk_1 FOREIGN KEY (state_id) REFERENCES states (id)
)
