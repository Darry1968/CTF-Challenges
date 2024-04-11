<?php
// Check if the "user" cookie is set
if(isset($_COOKIE["Session"]) && $_COOKIE["Session"] != "") {
    $val = $_COOKIE["Session"];
    
    $db = new SQLite3("test.db");
    
    $qr = "SELECT cookieVal FROM users WHERE cookieVal = '" . $val ."'";

    $query = $db->prepare($qr);
    $result = $query->execute();
    $row = $result->fetchArray();

    // Check if the query returned any result
    if ($row) {
        echo "<p>Welcome, Sir!</p>";
    } else {
        echo "<p>Hatt bsdk</p>";
        header("Location: index.html");
        exit();
    }
} else {
    // Redirect to the login page if the cookie is not set
    header("Location: index.html");
    exit();
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Programmer's Blog</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f0f0f0;
            margin: 0;
            padding: 0;
        }
        .container {
            max-width: 800px;
            margin: 20px auto;
            padding: 20px;
            background-color: #fff;
            border-radius: 5px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }
        h1 {
            text-align: center;
            color: #333;
        }
        .blog-entry {
            margin-bottom: 30px;
        }
        .blog-title {
            font-size: 24px;
            margin-bottom: 10px;
            color: #333;
        }
        .blog-content {
            font-size: 16px;
            color: #555;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Drug Awareness Blog</h1>
        
        <div class="blog-entry">
            <h2 class="blog-title">The Evolution of a Coffee Addict</h2>
            <p class="blog-content">First, we learn to sip. Then, we learn to brew. Finally, we learn to ignore the sleepless nights.</p>
        </div>
        
        <div class="blog-entry">
            <h2 class="blog-title">Why Did the Caffeine Addict Go to Rehab?</h2>
            <p class="blog-content">Because he couldn't espresso himself properly anymore.</p>
        </div>
        
        <div class="blog-entry">
            <h2 class="blog-title">Debugging Code with a Coffee Buzz</h2>
            <p class="blog-content">The only buzz I want to feel at 3 AM is from caffeine.</p>
        </div>
        
        <div class="blog-entry">
            <h2 class="blog-title">Why Do Programmers Prefer Dark Roast?</h2>
            <p class="blog-content">More caffeine, fewer yawns.</p>
        </div>
        
        <div class="blog-entry">
            <h2 class="blog-title">Coffee Lover's Diet</h2>
            <p class="blog-content">Coffee, more coffee, and </p>
             <code>while(coffee === true){ caffeine = caffeine + 1 }</code>
        </div>
    </div>
</body>

</html>


