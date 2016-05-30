drop table if exists entries;
create table users (
  	id integer primary key autoincrement,
  	username text not null,
  	password text not null
);

drop table if exists groups;
create table groups (
	id integer primary key autoincrement,
	groupname text not null,
	groupowner text not null,
	groupmember text not null
);