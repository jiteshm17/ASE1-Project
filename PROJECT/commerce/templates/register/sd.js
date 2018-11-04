        function Validate() {
        var password = document.getElementById("password").value;
        var confirmPassword = document.getElementById("password2").value;
        if (password != confirmPassword) {
            alert("Passwords do not match.");
            return false;
        }
        return true;
    }
function myValidateform(){
            var password = document.forms["myform"]["password"];
            var confirmPassword = document.forms["myform"]["pa"];

            alert('Checking');
            if(password != confirmPassword)
     {
                   alert("Sorry. Some Error");
                   return false;
            }
            return true;
    }
