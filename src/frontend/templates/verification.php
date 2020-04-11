<!DOCTYPE html>
<html lang="en">
<head>
    <title>Verification</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link href="{{ url_for('static', filename='css/style.css') }}" type="text/css" rel="stylesheet" />
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css" integrity="sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO" crossorigin="anonymous">
    <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.3/umd/popper.min.js" integrity="sha384-ZMP7rVo3mIykV+2+9J3UJ46jBk0WLaUAdn689aCwoqbBJiSnjAK/l8WvCWPIPm49" crossorigin="anonymous"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/js/bootstrap.min.js" integrity="sha384-ChfqqxuZUCnJSK3+MXmPNIyE6ZbWh2IMqE241rYiqJxyMiZ6OW/JmZQ5stwEULTy" crossorigin="anonymous"></script>
  </head>
<body>
<?php

      //generate code
      $code = substr(md5(uniqid(rand(), true)),6, 6);
      
      //format message
      $greetingText = "Your unique verifcation code is:\n";      
      $msg = $greetingText.$code;
      
    
      // send email
      if (!empty($_POST["email"])) {
        //fields
        $address = strval($_POST["email"]);
        $name = "book store";
        $sender = "tylerrosen97@gmail.com";
        $title = "Bookstore verification code";

        //db connection
        $servername = "192.168.1.79";
         $user= 'foo';
         $pass = "team";
         $dbname = 'bookstore';
        if ($conn = new mysqli($servername, $user, $pass, $dbname))
          echo "<p>connected</p>";
        else
          echo "<p>could not connect</p>";
        $sql = "UPDATE profile SET verificationCode = '".$code."' WHERE email='".$address."'";
        $conn->query($sql);
        $conn->close();

        
        $ch = curl_init();
        $headers = array(
          "Authorization: Bearer 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", 'Content-Type: application/json'
        );
        
        $data = array(
          "personalizations" => array(
            array (
              "to" => array(
                array(
                  "email" => $address,
                  "name" => $name
                )
              )
            )
          ),
          "from" => array(
            "email" => "tylerrosen97@gmail.com"
          ),
          "subject" => $title,
          "content" => array(
            array(
              "type" => "text/html",
              "value" => $msg
            )
          )
        );
        curl_setopt($ch, CURLOPT_URL, "https://sendgrid.com/v3/mail/send");
        curl_setopt($ch, CURLOPT_POST, 1);
        curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($data));
        curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
        curl_setopt($ch, CURLOPT_FOLLOWLOCATION, 1);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
        $response = curl_exec($ch);
        curl_close($ch);
        
      }  
      else {  
        
      }
       if (!empty($_POST["code"])) { //code verification against user input
         $inputCode = strval($_POST["code"]);
         $dbCode = 'aaaaa'; //temp code; never valid
         //retrieve code from database
         $servername = "192.168.1.79";
         $user= 'foo';
         $pass = "team";
         $dbname = 'bookstore';
         $conn = new mysqli($servername, $user, $pass, $dbname);
         $sql = "SELECT verificationCode FROM profile WHERE email='".$address."'";
         $result = $conn->query($sql);
         if ($result->num_rows > 0) {
          while($row = $result->fetch_assoc()) {
              $dbCode= $row["verificationCode"];
          }
         }
         
         
        
         if ($inputCode == $dbCode) {
          // $csql = "UPDATE profile p JOIN RegisteredUser"
           echo '<script type="text/javascript">';
           echo ' alert("Account successfully verified")'; 
           echo '</script>';
           
         }
         else {
           echo '<script type="text/javascript">';
           echo ' alert("Entered code was incorrect.")'; 
           echo '</script>';
         }
         $conn->close();
       }
      
    ?>
    
    
    <div class="topBar">
        
        <ul style="list-style-type: none;">    
        <li class="nav-item dropdown">
            <a class="nav-lifnk dropdown-toggle" data-toggle="dropdown" href="#" role="button" aria-haspopup="true" aria-expanded="false">Profile</a>
            <div class="dropdown-menu">
              <a class="dropdown-item" href="#">Edit Payment Info</a>
              <a class="dropdown-item" href="#">Edit Information</a>
              <a class="dropdown-item" href="#">Order History</a>
              <div class="dropdown-divider"></div>
              <a class="dropdown-item" href="#">Logout</a>
            </div>
          </li>
       </ul> 
    </div>

    <div class="jumbotron">
      <div class="container">
        <h1 class="display-2">Promotion/News</h1>
        <p class="lead">This is where we can advertise promos and stuff</p>
      </div>
          <hr class = "my-4">
          <div class="input-group mt-3 mb-3">
            <div class="input-group-prepend">
              <button type="button" class="btn btn-outline-secondary dropdown-toggle" data-toggle="dropdown">
                Apply Filter
              </button>
              <div class="dropdown-menu">
                <a class="dropdown-item" href="#">Subject</a>
                <a class="dropdown-item" href="#">Title</a>
                <a class="dropdown-item" href="#">Author</a>
                <a class="dropdown-item" href="#">ISBN</a>
                <a class="dropdown-item" href="#">None</a>
              </div>
            </div>
            <input type="text" class="form-control" placeholder="Enter keyword...">
            <div class="input-group-append">
              <button class="btn btn-outline-secondary" type="button" id="button-addon2">Search</button>
            </div>
          </div>
         
          <hr class = "my-4"> 
          <ul class="nav nav-pills nav-justified">
            <li class="nav-item">
              <a class="nav-link" href="#">Account</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="#">Manage Orders</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="#">Link</a>
            </li>
            <li class="nav-item">
              <a class="nav-link disabled" href="#" tabindex="-1" aria-disabled="true">Disabled</a>
            </li>
        </ul>
    </div>

    <!--Veridication-->
    <div class="container">
        <h2>Email Verification</h2>
        <h6>Almost there! Please enter the verification code that was sent to your email.</h6>
        <p>Didn't receive a code? <a>Click here to resend code</a></p>
      <form method="POST">
          <div class="form-group">
            <input class="form-control" placeholder="Verification Code" id="code" name="code">
          </div>
          
          <button type="submit" class="btn btn-primary">Verify Account</button>
      </form>
<br>
<br>
</body>
</html>

