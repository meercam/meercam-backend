drop table if exists cctv_table; 


create table cctv_table(
    id medium int not null auto_increment,
    name char(30) not null, 


    primary key (id)
);

create table 