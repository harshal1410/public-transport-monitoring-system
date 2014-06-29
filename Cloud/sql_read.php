    <?php
    require("access.php");
     
    // Opens a connection to a MySQL server
    $connection=mysql_connect ($dbhost, $dbuser, $dbpass);
    if (!$connection) {
    die('Not connected : ' . mysql_error());
    }
     
    // Set the active MySQL database
    $db_selected = mysql_select_db('sql340295', $connection);
    if (!$db_selected) {
    die ('Can\'t use db : ' . mysql_error());
    }
     
    // Select all the rows in the markers table
    $query = "SELECT * FROM busdata order by busdate desc LIMIT 1";
    $result = mysql_query($query);
    if (!$result) {
    die('Invalid query: ' . mysql_error());
    }
     
    header("Content-type: text/xml");
     
    // Start XML file, echo parent node
    echo '<busdata>';
     
    // Iterate through the rows, printing XML nodes for each
    while ($row = @mysql_fetch_assoc($result)){
    // ADD TO XML DOCUMENT NODE
    echo '<businfo ';
    echo 'busno="' . $row['busno'] . '" ';
    echo 'lat="' . $row['lat'] . '" ';
    echo 'lon="' . $row['lon'] . '" ';
    echo 'speed="' . $row['speed'] . '" ';
    echo 'stop="' . $row['stop'] . '" ';
    echo '/>';
    }
     
    // End XML file
    echo '</busdata>';
     
    ?>