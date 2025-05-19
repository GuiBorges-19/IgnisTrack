create database Drone_project;

use Drone_project;

truncate drone;






create table OperacaoArea(
id int auto_increment primary key,
operacao_id int,
area_id int,
foreign key (operacao_id) references DataOperacao(id),
foreign key (area_id) references Areas(id)
);

create table Areas(

id int auto_increment primary key,
nome_area varchar(100)
);

create table DataOperacao(

id int auto_increment primary key,
operador_id int,
drone_id int,
coordenadas_id int,
clima_id int,
foreign key(operador_id) references Operador(id),
foreign key(drone_id) references Drone(id),
foreign key(coordenadas_id) references CoordenadasOperacao(id),
foreign key(clima_id) references Clima(id)
);
ALTER TABLE DataOperacao ADD COLUMN data DATETIME;


create table Drone(
id int auto_increment primary key,
modelo varchar(100),
marca varchar(100),
autonomia int
);

create table Operador(
id int auto_increment primary key,
nome varchar(100)
);

create table CoordenadasOperacao(
id int auto_increment primary key,
latitude float,
longitude float,
altitude float
);

create table Clima(
id int auto_increment primary key,
temperatura_media float,
vento float,
humidade float,
pressao float,
ultravioleta float,
sensacao_termica float,
ponto_orvalho float,
qualidade_ar float
);

-- Inserir um operador
INSERT INTO Operador (nome) VALUES ('Guilherme');

-- Inserir um drone
INSERT INTO Drone (modelo, marca, autonomia) VALUES ('DJI Phantom 4', 'DJI', 30);

-- Inserir coordenadas da operação
INSERT INTO CoordenadasOperacao (latitude, longitude, altitude) VALUES (40.7128, -74.0060, 120);

-- Inserir dados climáticos
INSERT INTO Clima (temperatura_media, vento, humidade, pressao, ultravioleta, sensacao_termica, ponto_orvalho, qualidade_ar) 
VALUES (25.5, 12.3, 60.2, 1013, 5.5, 26, 14, 80);

-- Inserir a operação na tabela DataOperacao
INSERT INTO DataOperacao (operador_id, drone_id, coordenadas_id, clima_id) 
VALUES (1, 1, 1, 1);

-- Inserir uma área de operação
INSERT INTO Areas (nome_area) VALUES ('Zona Industrial');

-- Relacionar a operação com a área
INSERT INTO OperacaoArea (operacao_id, area_id) VALUES (1, 1);



