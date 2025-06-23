-- Create the database if it does not exist
DO $$  
BEGIN  
    IF NOT EXISTS (SELECT FROM pg_database WHERE datname = 'users_DB') THEN  
        CREATE DATABASE "users_DB" WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'en-US';  
    END IF;  
END $$;

-- Connect to the database
\connect "users_DB"

-- Create the roles table
CREATE TABLE public.roles (
    id integer NOT NULL,
    role text NOT NULL
);

ALTER TABLE public.roles OWNER TO postgres;

-- Create the users table
CREATE TABLE public.users (
    id integer NOT NULL,
    first_name text NOT NULL,
    last_name text NOT NULL,
    email text NOT NULL,
    password_hash text NOT NULL,
    role_id integer
);

ALTER TABLE public.users OWNER TO postgres;

-- Create sequence for users ID
CREATE SEQUENCE public.users_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE public.users_id_seq OWNER TO postgres;

-- Set sequence as default for users.id
ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);

-- Make the sequence owned by the users.id column
ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;

-- Insert role data
INSERT INTO public.roles VALUES (1, 'admin');
INSERT INTO public.roles VALUES (0, 'user');

-- Insert user data (matching the dump)
INSERT INTO public.users OVERRIDING SYSTEM VALUE VALUES (1, 'Alice', 'Adams', 'alice.adams@gmail.com', '$2b$12$T5Cp.D.5HrZ5PT53riSmUuG5yc9SPjSjZBjAOmrsG9bpHowHPb5G2', 1);
INSERT INTO public.users OVERRIDING SYSTEM VALUE VALUES (2, 'Bob', 'Bobbins', 'bob.bobbins@gmail.com', '$2b$12$dy21Zc5gVDtuKMek3.TG7u8Co5L02emziFmEoCad.sBQbad3ZcwfS', 1);
INSERT INTO public.users OVERRIDING SYSTEM VALUE VALUES (3, 'Charlie', 'Charleston', 'charlie.charleston@gmail.com', '$2b$12$k9aQGUvb/Jci0hNxp.SBbuDlDEZDGW6sIqptQ/s2K2W3/5yikiPJy', 1);
INSERT INTO public.users OVERRIDING SYSTEM VALUE VALUES (4, 'David', 'Davidson', 'david.davidson@gmail.com', '$2b$12$74edA6DxlDt86olTebet4OqYpAQN9iNzaZPO.0yLOxoml0V848R9O', 0);
INSERT INTO public.users OVERRIDING SYSTEM VALUE VALUES (8, 'aa', 'bb', 'aabb@cc.nl', '$2b$12$mhpq0Q3ng8vQvp0zWzIRmekDkXEE7lppXHl1o95bYuAqFErMLt6AG', 0);

-- Set the sequence to the correct next value
SELECT pg_catalog.setval('public.users_id_seq', 8, true);

-- Set primary keys
ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_pkey PRIMARY KEY (id);

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);

-- Add foreign key constraint
ALTER TABLE ONLY public.users
    ADD CONSTRAINT role_id FOREIGN KEY (role_id) REFERENCES public.roles(id) NOT VALID;