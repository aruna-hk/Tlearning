         <h1>learnplus</h1>
<div>
 <a href=mailto:kiptooharon.hk@gmail.com>Email: kiptooharon.hk@gmail.com</a>
 <a href=tel:0714261231>Phone:0714261231</a>
</div>
         <h2>COMMANDLINE</h2>
<h3>SET UP DATABASE AND DATABASE USER</h3>
This is used by sqlalchemy in connection to database i hardcoded it in the code<br/>
Run database.sql script in project directory<br/>
<code>sudo mysql < databse.sql </code>
above code should create database and database user specified in the script<br/>
tables and database schemy build by sqlalchemy</br>

<h3>SET UP THE SERVER</h3>
clone the repository first<br/>
set-up and start gunicorn wsgi--make sure to change directorires in config files<br/>
<code>sudo cp learnplus.service /etc/systemd/system</code><br/>
start the server<br/>
<code>sudo service learnplus start</code><br/>
setup web server(nginx)<br\>
edit nginx.conf file add the following line include /path/to/this/directory/\*.conf<br\>
then run
<code>sudo service nginx restart</code><br/>
now nginx server running at port 8080 (can change in serverblock.conf file in project directory and reload)<br\>
gunicorn at 8081 as per gunicorn.conf.py <br\>
nginx proxy passes to gunicorn which is managing flask instance specified in conf file<br/>

<ol>
<li>
<h3>CREATE ACCOUNT</h3>
<code> curl -X POST -H "Content-Type":"application/json" -d '{"name":"nice", "username":"nice", "email":"nice@gmail.com", "phone":"778", "password":"Aa48904890plmn$"}' localhost:8080/learnplus/home/learners</code><br/><div> provides login link as return if registration sucess error if integrity issues occur in database(409 conflict)</div></li>
<li>
<h3>LOGIN</h3>
login with redirection link username and password as querystring<br/>
lets use our created user to login
<code>
curl localhost:8080/learnplus/home/login?username=nice\&password=Aa48904890plmn$ </code>
ensure to escape ampersand with \ not to be interpreted by shell <br/>
on login user is redirected to dynamic page generated by flask web app follow the link<br/>
</li>
<li>
<h3>VISIT HOME PAGE</h3>
<div>
follow the redirection link <br/>on redirection user password passed as query string can't be in browsers search bar
<div>
<code>curl http://localhost:8080/learnplus/home/<idreturned>
</code>
<br/>
above code should display user home screen
</li><br/>
<li>
<h3>UNIT ENROLLMENT</h3>
First create dummy unit/s<br\>
user sudo/user having privileges on learnplus database(learnplus user created by .sql file)<br/>
<code>sudo mysql learnplus;</code>
<code>insert into units values("Unix networking", "jane", "001", NULL, NULL);</code>
first try to get courses enrolled by user with<br>
<code>curl http://localhost:8080/learnplus/home/<useridreturned>/unit</code>
should return No content 204<br/>
now enroll user post request to same get api endpoint(dummy course above)<br/>
<code>curl -X POST -H "Content-Type":"application/json" -d '{"unitId":"001"}' 
localhost:8081/learnplus/home/<idreturned>/unit</code><br/>
Above code should enroll user as taking course 001<br/>
check it out by listing units is enrolled in<br/>
<code>curl http://localhost:8080/learnplus/home/{user_id}/units</code>
Should return list of dict course and progress<br/>
</li>
<li>
<h3>UNIT DELETION</h3>
demo user sends a delete request<br/>
<code>curl -X DELETE -H "Content-Type":"application/json" -d '["001", "002"]' 
http://localhost:8080/learnplus/home/{user_id}/unit</code>
delete takes a list of course id to unenroll<br/>
Check<br/>
<code>curl http://localhost:8080/learnplus/home/{user_id}/units</code>
should return Nothing<br/>
</li>
<div>OTHER API ON APP.PY FILE</div>
