#conexion.py:
<?php
header('Content-Type: application/json');

$hostname = 'localhost';
$database = 'usuarios_db';
$username = 'root';
$password = '';

$conexion = mysqli_connect($hostname, $username, $password, $database);

if (mysqli_connect_errno()) {
    echo json_encode(["success" => false, "message" => "Fallo la conexión: " . mysqli_connect_error()]);
} else {
    echo json_encode(["success" => true, "message" => "Conexión exitosa a la base de datos."]);
}
?>
