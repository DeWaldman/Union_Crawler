create database mangazada;
use mangazada;
create table teste
(
nome_usuario varchar(10) primary key,
nome_manga varchar (40)
)engine=InnoDB;

insert into teste(nome_usuario,nome_manga) values("gustavo","boku no hero");

select * from teste;