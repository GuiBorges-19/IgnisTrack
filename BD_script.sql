create database Drone_Data;

use Drone_Data;


CREATE TABLE OperacaoArea (
    id INT AUTO_INCREMENT PRIMARY KEY,
    operacao_id INT,
    area_id INT,
    FOREIGN KEY (operacao_id) REFERENCES DataOpracao(id),
    FOREIGN KEY (area_id) REFERENCES Areas(id)
);
create table Areas (
id int AUTO_INCREMENT PRIMARY KEY,
nome_area varchar(100),
geometria geometry,
tipo_area varchar(100),
data_criacao Datetime

);

create table DataOpracao(
id INT AUTO_INCREMENT PRIMARY KEY,
operador_id INT,
drone_id INT,
coordenadas_id int,
foreign key (operador_id) references Operador(id),
foreign key (drone_id) references Drone(id),
foreign key (coordenadas_id) references CoordenadasOperacao(id)
);

Create table Drone (

id INT AUTO_INCREMENT PRIMARY KEY,
modelo varchar(100),
marca varchar(100),
autonomia int
);

create table Operador(
id int AUTO_INCREMENT PRIMARY KEY, 
nome varchar(100)
);

create table CoordenadasOperacao(
id int AUTO_INCREMENT PRIMARY KEY ,
latitude float,
longitude float,
altitude float,
temperatura_media float,
velocidade_vento float
);

create table Temperatura(
id int AUTO_INCREMENT PRIMARY KEY,
coordenadas_id int,
data_temp date,
valor float,
foreign key (coordenadas_id) references CoordenadasOperacao(id)
);

create table Clima(
id int AUTO_INCREMENT PRIMARY KEY,
coordenadas_id int,
qualidade_ar float,
humidade float,
vento float,
pressao float,
ponto_orvalho float,
sensacao_termica float,
ultravioleta float,
foreign key (coordenadas_id) references CoordenadasOperacao(id)
);


