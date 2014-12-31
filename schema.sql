drop table if exists users;
create table users (
	id integer primary key autoincrement,
	mail text not null,
	value integer not null,
	last_sent integer not null
);

drop table if exists data;
create table data (
	id integer primary key autoincrement,
	url text not null,
	checks integer not null,
	size integer not null,
	time integer not null
);