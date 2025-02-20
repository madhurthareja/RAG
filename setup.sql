create extension if not exists vector;

create table documents (
    id uuid default gen_random_uuid() primary key,
    file_name text,  -- Add this line
    content text,
    embedding vector(1536)
);