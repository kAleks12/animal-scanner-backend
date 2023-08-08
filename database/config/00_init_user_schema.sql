CREATE SCHEMA IF NOT EXISTS "user";
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS "user"."User" (
    "id" uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    "username" VARCHAR(255) NOT NULL UNIQUE,
    "password" VARCHAR(255) NOT NULL,
    "email" VARCHAR(255) NOT NULL UNIQUE,
    "refresh_token" VARCHAR,
    "activated" BOOLEAN NOT NULL DEFAULT FALSE,
    "password_reset_code" VARCHAR,
    "activation_code" VARCHAR
);

