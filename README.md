         <h1>learnplus</h1>
<div>
 <a href=mailto:kiptooharon.hk@gmail.com>Email: kiptooharon.hk@gmail.com</a>
 <a href=tel:0714261231>Phone:0714261231</a>
</div>
         <h2>COMMANDLINE</h2>
<h3>SET UP THE SERVER</h3>
clone the repository first<br/>
start gunicorn server--make sure to change directorires in config files<br/>
<code>sudo cp learnplus.service /etc/systemd/system</code><br/>
start the server<br/>
<code>sudo service learnplus start</code><br/>
setup web server nginx<br\>
edit nginx.conf add the include /path/to/this/directory/\*.conf<br\>
then run
<code>sudo service nginx restart</code><br/>
nginx server running at port 8080 -- nginx<br\>
gunicorn at 8081 <br\>
nginx proxy passes to 8081 -- redirection link shown on output
<ol>
  <li>
      <h3>CREATE ACCOUNT</h3>
      <code> curl -X POST -H "Content-Type":"application/json" -d '{"name":"nice", "username":"nice", "email":"nice@gmail.com", 
           "phone":"778", "password":"Aa48904890plmn$"}' localhost:8080/learnplus/home/learners
       </code><br/>
      <div> provides login link as return if registration sucess error if integrity issues occur in database</div>
   </li>
   <li>
       <h3>LOGIN</h3>
      login with output link replacing inserting username and password<br/>
      lets use our created user to login
       <code> curl localhost:8081/learnplus/home/login?username=nice\&password=Aa48904890plmn$ </code>
       ensure to escape ampersand with \ not to be interpreted by shell <br/>
       on login user is dericted to dynamic page generated by flask web app<br/>
    </li>
    <li>
        <h3>VISIT HOME PAGE</h3>
        <div>
            follow the redirection link <br/> on redirection user password passed as query string can't be
            in browsers search bar
        <div>
         <code><br/>
              curl http://localhost:8081/learnplus/home/32677c8e-25b3-45c2-bd50-5e2b6ef3339a
         </code><br/>
         above code should display user home screen
     </li><br/>
    <div>OTHER API ON APP.PY FILE</div>
</li>
