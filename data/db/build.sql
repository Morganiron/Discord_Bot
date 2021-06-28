CREATE TABLE IF NOT EXISTS exp (
  userid integer PRIMARY KEY,
  XP integer DEFAULT 0,
  Level integer DEFAULT 0,
  XPLock text DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS user (
  UserID integer PRIMARY KEY,
  username VARCHAR2 NOT NULL
);
CREATE TABLE IF NOT EXISTS chunkdata (
  id integer AUTO DEFAULT 0001 PRIMARY KEY,
  chunkname VARCHAR2(45) NOT NULL,
  x1 integer(10) NOT NULL,
  x2 integer(10) NOT NULL,
  z1 integer(10) NOT NULL,
  z2 integer(10) NOT NULL,
  userid integer NOT NULL
);
CREATE TABLE IF NOT EXISTS savecoord (
  id integer AUTO DEFAULT 001 PRIMARY KEY,
  coordname VARCHAR2(45) NOT NULL,
  xcoord integer(10) NOT NULL,
  zcoord integer(10) NOT NULL,
  userid integer NOT NULL
);