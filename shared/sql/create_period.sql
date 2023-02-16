create table if not exists period (
id integer primary key,
start integer not null,
end integer not null,
activity_id integer not null,
foreign key (activity_id) references activity (id)
);
