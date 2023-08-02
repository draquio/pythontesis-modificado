instructions = [
    'SET FOREIGN_KEY_CHECKS=0;',
    'DROP TABLE IF EXISTS rol;',
    'DROP TABLE IF EXISTS user;',
    'DROP TABLE IF EXISTS receta;',
    'DROP TABLE IF EXISTS carnes;',
    'DROP TABLE IF EXISTS tipocarne;',
    'DROP TABLE IF EXISTS codigoqr;',
    'DROP TABLE IF EXISTS almacen;',
    'DROP TABLE IF EXISTS almacencarnessobra;',
    'DROP TABLE IF EXISTS cortecarne;',
    'SET FOREIGN_KEY_CHECKS=1;',
    """
    CREATE TABLE rol(
        id INT PRIMARY KEY AUTO_INCREMENT,
        nombrerol VARCHAR(50) NOT NULL,
        descripcion VARCHAR(500) NOT NULL,
        privilegio int
        );
    """,
    """
    CREATE TABLE user(
        id INT PRIMARY KEY AUTO_INCREMENT,
        username VARCHAR(50) UNIQUE NOT NULL,
        idrol INT,
        password VARCHAR(100) NOT NULL,
        FOREIGN KEY (idrol) REFERENCES rol (id)
        );
    """,
    """
    CREATE TABLE cortecarne(
        id INT PRIMARY KEY AUTO_INCREMENT,
        nombre VARCHAR(150) NOT NULL,
        estado int
        );
    """,
    """
    CREATE TABLE tipocarne(
        id INT PRIMARY KEY AUTO_INCREMENT,
        nombre VARCHAR(50) NOT NULL
        );
    """,
    """
    CREATE TABLE receta(
        id INT PRIMARY KEY AUTO_INCREMENT,
        iduser INT,
        id_v VARCHAR(50) NOT NULL,
        title VARCHAR(250),
        thumbnail VARCHAR(300) NOT NULL,
        date datetime NOT NULL,
        FOREIGN KEY (iduser) REFERENCES user (id)
        );
    """,
    """
    CREATE TABLE carnes(
        id INT PRIMARY KEY AUTO_INCREMENT,
        idtipocarne int,
        idcortecarne int,
        iduser int,
        cantidad decimal(5,2),
        date datetime NOT NULL,
        tipo int,
        FOREIGN KEY (idtipocarne) REFERENCES tipocarne (id),
        FOREIGN KEY (idcortecarne) REFERENCES cortecarne (id),
        FOREIGN KEY (iduser) REFERENCES user (id)
        );
    """,
    """
    CREATE TABLE almacen(
        id INT PRIMARY KEY AUTO_INCREMENT,
        nombre VARCHAR(150),
        date datetime NOT NULL,
        estado int
        );
    """,
    """
    CREATE TABLE almacencarnessobra(
        id INT PRIMARY KEY AUTO_INCREMENT,
        idalmacen int,
        idcarne int,
        date datetime NOT NULL,
        FOREIGN KEY (idalmacen) REFERENCES almacen (id),
        FOREIGN KEY (idcarne) REFERENCES carnes (id)
        );
    """,
    """
    CREATE TABLE codigoqr(
        id INT PRIMARY KEY AUTO_INCREMENT,
        img VARCHAR(150) NOT NULL unique,
        texto VARCHAR(150) NOT NULL,
        idalmacen int,
        FOREIGN KEY (idalmacen) REFERENCES almacen (id)
        );
    """
    
    
    
    
    
    
]