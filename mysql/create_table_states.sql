CREATE TABLE states (
  id varchar(60) NOT NULL,
  created_at datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  name varchar(128) NOT NULL,
  PRIMARY KEY (id)
)
