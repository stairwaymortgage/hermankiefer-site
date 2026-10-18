-- HermanKiefer.com database. Visitors may only INSERT; nothing private is ever readable
-- by the public. Only the admin (Jim's signed-in email) can read and moderate.
create table if not exists members (
  id uuid primary key default gen_random_uuid(), created_at timestamptz default now(),
  name text not null, email text not null, phone text, relation text, branch text, knows text,
  has_items boolean default false, item_details text,
  dir_ok boolean default false, digest_ok boolean default false, business_ok boolean default false);
create table if not exists contributions (
  id uuid primary key default gen_random_uuid(), created_at timestamptz default now(),
  kind text not null default 'item' check (kind in ('item','hello','story')),
  title text, story text, people text, year text, name text not null, email text not null, credit_name text,
  visibility text not null default 'family' check (visibility in ('public','family','jim')),
  file_path text, file_type text,
  status text not null default 'pending' check (status in ('pending','approved','archived','rejected')));
create table if not exists comments (
  id uuid primary key default gen_random_uuid(), created_at timestamptz default now(),
  page text not null, name text not null, email text not null, body text not null check (length(body) < 5000),
  status text not null default 'pending' check (status in ('pending','approved','read')));
create table if not exists tree_suggestions (
  id uuid primary key default gen_random_uuid(), created_at timestamptz default now(),
  person_id text, person_name text, kind text, details text not null, name text not null, email text not null,
  status text not null default 'pending');

alter table members enable row level security;
alter table contributions enable row level security;
alter table comments enable row level security;
alter table tree_suggestions enable row level security;

create or replace function is_admin() returns boolean language sql stable security definer set search_path = public as
$$ select coalesce(auth.jwt() ->> 'email', '') = 'jjb161728@gmail.com' $$;

-- public may insert, but only in the pending state
create policy "anyone can join" on members for insert to anon, authenticated with check (true);
create policy "anyone can share" on contributions for insert to anon, authenticated with check (status = 'pending');
create policy "anyone can comment" on comments for insert to anon, authenticated with check (status = 'pending');
create policy "anyone can suggest" on tree_suggestions for insert to anon, authenticated with check (status = 'pending');
-- admin full access
create policy "admin members" on members for all to authenticated using (is_admin()) with check (is_admin());
create policy "admin contributions" on contributions for all to authenticated using (is_admin()) with check (is_admin());
create policy "admin comments" on comments for all to authenticated using (is_admin()) with check (is_admin());
create policy "admin suggestions" on tree_suggestions for all to authenticated using (is_admin()) with check (is_admin());

-- public views expose only approved, public items and never emails
create or replace view public_album with (security_invoker = false) as
  select id, created_at, kind, title, story, people, year, coalesce(credit_name, name) as name, credit_name, file_path, file_type
  from contributions where status = 'approved' and visibility = 'public';
create or replace view public_comments with (security_invoker = false) as
  select id, created_at, page, name, body from comments where status = 'approved' and page not like '%private%';
grant select on public_album, public_comments to anon, authenticated;

-- storage: 'uploads' is private (anyone may add; only admin reads); 'album' is public (admin copies approved files in)
insert into storage.buckets (id, name, public, file_size_limit) values ('uploads', 'uploads', false, 52428800) on conflict (id) do nothing;
insert into storage.buckets (id, name, public, file_size_limit) values ('album', 'album', true, 52428800) on conflict (id) do nothing;
create policy "anyone can upload" on storage.objects for insert to anon, authenticated with check (bucket_id = 'uploads');
create policy "admin reads uploads" on storage.objects for select to authenticated using (bucket_id in ('uploads','album') and is_admin());
create policy "admin writes album" on storage.objects for insert to authenticated with check (bucket_id = 'album' and is_admin());
