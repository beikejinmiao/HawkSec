CREATE TABLE crawlstat (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    origin     	TEXT NOT NULL,
    origin_name TEXT,
    origin_from TEXT,
    resp_code 	INT,
    [desc]      TEXT,
    create_time DATETIME DEFAULT (datetime('now', 'localtime'))
);



CREATE TABLE extractor (
    id             INTEGER  PRIMARY KEY AUTOINCREMENT,
    origin         TEXT     NOT NULL,
    sensitive_type INT      NOT NULL,
    sensitive_name VARCHAR (128) NOT NULL,
    content        TEXT     NOT NULL,
    count          INT      DEFAULT 1,
    [desc]         TEXT,
    create_time    DATETIME DEFAULT (datetime('now', 'localtime') )
);


CREATE TABLE sensitives (
    id             INTEGER       PRIMARY KEY AUTOINCREMENT,
    content        TEXT          NOT NULL,
    content_name   TEXT,
    sensitive_type INT           NOT NULL,
    sensitive_name VARCHAR (128) NOT NULL,
    origin         TEXT          NOT NULL,
    [desc]         TEXT,
    create_time    DATETIME      DEFAULT (datetime('now', 'localtime') )
);


CREATE TABLE whitelist (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    white_type 	INT NOT NULL,
    ioc     	TEXT NOT NULL,
    [desc]      TEXT,
    create_time DATETIME DEFAULT (datetime('now', 'localtime'))
);


CREATE TABLE filetype (
    id          INTEGER      PRIMARY KEY AUTOINCREMENT,
    category    VARCHAR (32) NOT NULL,
    suffix      VARCHAR (32) NOT NULL,
    mime_type   TEXT,
    create_time DATETIME     DEFAULT (datetime('now', 'localtime') )
);
