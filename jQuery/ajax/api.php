<?php
   $GET_arg = $_GET['arg']; 
   $POST_arg = $_POST['arg']; 

   if (isset($GET_arg))
       echo "GET: $GET_arg";
   if (isset($POST_arg))
       echo "POST: $POST_arg";
?>
