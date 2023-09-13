CREATE SCHEMA IF NOT EXISTS "data";
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";


CREATE TABLE IF NOT EXISTS "data"."Submission" (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    x numeric NOT NULL,
    y numeric NOT NULL,
    author_id uuid,
    filename varchar,
    description varchar(250) NOT NULL,
    FOREIGN KEY(author_id)
    REFERENCES "user"."User"(id)
    ON DELETE SET NULL
);