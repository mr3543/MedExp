drop table if exists users;
create table users (
    user_id integer primary key autoincrement,
    username text not null unique,
    pw_hash text not null,
    time_created integer 
    );

drop table if exists articles;
create table articles (
    article_id integer primary key autoincrement,
    title text not null,
    url text not null unique,
    create_time integer 
    );

drop table if exists library;
create table library (
    lib_id integer primary key autoincrement,
    article_id integer not null,
    user_id integer not null,
    update_time integer not null,
    foreign key(user_id) references users(user_id),
    foreign key(article_id) references articles(article_id),
    unique (user_id,article_id)
    );

drop table if exists article_counts;
create table article_counts (
    num_articles integer not null
    );

create unique index idx_user_article on library(user_id,article_id);
create index idx_lib_user_id on library(user_id);
create index idx_lib_article_id on library(article_id);
create unique index idx_username on users(username);


