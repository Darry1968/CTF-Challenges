<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    
    $username = $_POST["username"];
    $password = $_POST["password"];

    // Check if inputs are empty
    if (empty($username) || empty($password)) {
        echo "<p>Please enter both username and password.</p>";
        exit;
    }

    $db = new SQLite3("D:\\xampp\htdocs\Challenge\user_login\\test.db");

    try {
        $qury = "SELECT * FROM users WHERE username = '{$username}' AND password = '{$password}'";
        $query = $db->prepare($qury);

        if (!$query) {
            throw new Exception("Error preparing query: " . $db->lastErrorMsg());
        }

        $result = $query->execute();

        if (!$result) {
            throw new Exception("Error executing query");
        }
        
        if ($result->fetchArray()) {
            // User is authenticated
            $query = $db->prepare("SELECT cookieVal FROM users WHERE username = :username");
            $query->bindValue(':username', $username, SQLITE3_TEXT);
            $result = $query->execute();
    
            $row = $result->fetchArray();
    
            // Check if the query returned any result
            if ($row) {
                $cookieValue = $row['cookieVal'];
                setcookie("Session", $cookieValue, time() + (86400 * 30), "/"); // Cookie expires in 30 days
                header("Location: welcome.php"); 
            } else {
                echo "User not found or no cookie value associated with the user.";
            }
    
        } else {
            echo "<p>Login failed. Please check your username and password.</p>";
        }
    } catch (Exception $e) {
        echo "No hacking please";
    }
    

    $db->close();
}
?>

<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login Page</title>
	<link rel="stylesheet" href="style.css">
</head>

<body>

    <div class="box">
		<form autocomplete="off" method="post" action="login.php">
			<h2>Sign in</h2>
			<div class="inputBox">
				<input type="text" name="username" required="required">
				<span>Userame</span>
				<i></i>
			</div>
			<div class="inputBox">
				<input type="password" name="password" required="required">
				<span>Password</span>
				<i></i>
			</div>
			<input type="submit" value="Login">
		</form>
	</div>

</body>

</html>