/* 
# Author: Christina Christodoulakis
# 
#    Copyright 2013 Christina Christodoulakis
# 
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
# 
#        http://www.apache.org/licenses/LICENSE-2.0
# 
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
 */
package mysqldb;


import java.sql.Connection;
import java.sql.DatabaseMetaData;
import java.sql.DriverManager;
import java.sql.SQLException;


/**
 *
 * @author Christina Christodoulakis
 * @email christina'@'cs.toronto.edu 
 * Computer Science, University of Toronto 2013
 */
public class MySQLConnection {
    
	public Connection connects() throws SQLException
	{
		try
		{   Class.forName("com.mysql.jdbc.Driver");  }
		catch(Exception e)
		{   e.printStackTrace();  }

		//Define URL of connection
		String host = "localhost";
		String dbName = "hospital";
	//	int port = 3306;
                int port= 40415; // mysql server running on colony
		String mysqlURL = "jdbc:mysql://"+host+":"+port+"/"+dbName+"?characterEncoding=utf-8&useUnicode=true";
		//Setup the connection
		String username = "your_username";
		String password = "your_password";

		Connection conn = DriverManager.getConnection(mysqlURL,username,password);
		//Usefull information about connection
		DatabaseMetaData dbMetadata = conn.getMetaData();
		String productName = dbMetadata.getDatabaseProductName();
		//System.out.println("Database: "+ productName);
		String productVersion = dbMetadata.getDatabaseProductVersion();
		//System.out.println("Version: "+ productVersion);
		String myURL = dbMetadata.getURL();
		//System.out.println("URL: " + myURL);
                System.out.println("database visited");

		return conn;
	}
}
