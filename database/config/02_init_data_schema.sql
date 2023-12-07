CREATE SCHEMA IF NOT EXISTS "data";
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";


CREATE TABLE IF NOT EXISTS "data"."Submission" (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    x numeric NOT NULL,
    y numeric NOT NULL,
    author_id uuid,
    description varchar(250),
    date timestamp NOT NULL,
    FOREIGN KEY(author_id)
    REFERENCES "user"."User"(id)
    ON DELETE SET NULL
);


CREATE TABLE IF NOT EXISTS "data"."Tag" (
    id bigint GENERATED ALWAYS AS  IDENTITY,
    value varchar NOT NULL,
    submission_id uuid NOT NULL,
    FOREIGN KEY(submission_id)
    REFERENCES "data"."Submission"(id)
    ON DELETE CASCADE
);