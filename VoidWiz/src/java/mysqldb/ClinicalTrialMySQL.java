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

import dao.ClinicalTrialDAO;
import entity_layer.ClinicalTrial;
import entity_layer.PatientVisit;
import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.LinkedList;

/**
 *
 * @author Christina Christodoulakis
 * @email christina'@'cs.toronto.edu 
 * Computer Science, University of Toronto 2013
 */
public class ClinicalTrialMySQL implements ClinicalTrialDAO {
    
    public LinkedList<ClinicalTrial> getClinicalTrials(String value, String type) {
        LinkedList<ClinicalTrial> trials = new LinkedList<ClinicalTrial>();
        String query = "SELECT * FROM hospital.clinicalTrial where "+type.toLowerCase()+"='"+value+"' and country = 'Canada';";
        System.out.println("query run is: " +query);
        try {

            MySQLConnection dbconn = new MySQLConnection();
            Connection conn = (Connection) dbconn.connects();
            Statement statement = (Statement) conn.createStatement();
            ResultSet rs = statement.executeQuery(query);

            while (rs.next()) {
                ClinicalTrial ctrial = new ClinicalTrial();
                ctrial.setTupleid(rs.getInt("tupleid"));
                ctrial.setCtid(rs.getString("CTID"));
                ctrial.setCountry(rs.getString("country"));
                ctrial.setSource(rs.getString("source"));
                ctrial.setCondition(rs.getString("medcondition"));
                ctrial.setDrug(rs.getString("drug"));

                trials.add(ctrial);

            }
            rs.close();
            conn.close();
            rs = null;
            conn = null;
            return trials;


        } catch (SQLException ex) {
            ex.printStackTrace();
            System.out.println("Exception during SQL Query: " + ex);
            return null;
        }

    }
}
