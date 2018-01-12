drop table if exists User; 
create table User (
	id integer primary key autoincrement,
   	login varchar(20) not null unique,
	password varchar not null,
	phone_number varchar(9) not null unique,
	email varchar(20) not null,
   	name varchar(20), 
   	surname varchar(20),
   	birth_date varchar(10),
	sex varchar check(sex in ('M', 'W'))   
);

drop table if exists Call;
create table Call ( 
	id integer primary key autoincrement,
	user1_id integer not null,
	user2_id integer not null,
 	tarrif_id integer not null,
	call_date date not null,
	duration integer,
	quality integer check(quality > 0 and quality < 11),
	FOREIGN KEY(user1_id) REFERENCES User(id),
	FOREIGN KEY(user2_id) REFERENCES User(id),
	FOREIGN KEY(tarrif_id) REFERENCES Tarrif(id)
);

drop table if exists Tarrif;
create table Tarrif (
	id integer primary key autoincrement,
	operator_id integer not null,
	name varchar(20) not null unique,
	cost_per_minute float not null 
);

drop table if exists Operator;
create table Operator (
	id integer primary key autoincrement,
	name varchar(20) not null unique
);
