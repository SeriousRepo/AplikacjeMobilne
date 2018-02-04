drop table if exists Operator;
create table Operator (
	id integer primary key autoincrement,
	name varchar not null unique
);

drop table if exists Tarrif;
create table Tarrif (
	id integer primary key autoincrement,
	operator_id integer not null,
	name varchar not null unique,
	cost_per_minute float not null, 
	FOREIGN KEY(operator_id) REFERENCES Operator(id)
);

drop table if exists User; 
create table User (
	id integer primary key autoincrement,
   	login varchar not null unique,
	password varchar not null,
	phone_number varchar not null unique check(phone_number GLOB '[1-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]'),
	email varchar not null check(email like '%_@__%.__%'),
   	name varchar,
   	surname varchar,
   	birth_date varchar check(birth_date is strftime('%Y-%m-%d', birth_date)),
	sex varchar check(sex in ('M', 'W'))   
);

drop table if exists Call;
create table Call ( 
	id integer primary key autoincrement,
	user1_id integer not null,
	user2_id integer not null,
 	tarrif_id integer not null,
	call_date varchar not null check(call_date is strftime('%Y-%m-%d %H:%M:%S', call_date)),
	duration integer,
	quality integer check(quality > 0 and quality < 11),
	FOREIGN KEY(user1_id) REFERENCES User(id),
	FOREIGN KEY(user2_id) REFERENCES User(id),
	FOREIGN KEY(tarrif_id) REFERENCES Tarrif(id)
);
