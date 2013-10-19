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

import dao.VisitDAO;
import entity_layer.GraphLink;
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
public class VisitMySQL implements VisitDAO {

    public LinkedList<PatientVisit> getPatientVisits() {
        LinkedList<PatientVisit> visits = new LinkedList<PatientVisit>();
        String query = "SELECT * FROM hospital.patientVisit;";

        try {

            MySQLConnection dbconn = new MySQLConnection();
            Connection conn = (Connection) dbconn.connects();
            Statement statement = (Statement) conn.createStatement();

            ResultSet rs = statement.executeQuery(query);

            while (rs.next()) {
                PatientVisit pvisit = new PatientVisit();
                pvisit.setVisit_id(rs.getInt("visitId"));
                pvisit.setPatientName(rs.getString("patient_name"));
                pvisit.setDoctorName(rs.getString("doctor_name"));
                pvisit.setDiagnosis(rs.getString("diagnosis"));
                pvisit.setTreatment(rs.getString("drug"));
                visits.add(pvisit);

            }
            rs.close();
            conn.close();
            rs = null;
            conn = null;
            return visits;


        } catch (SQLException ex) {
            ex.printStackTrace();
            System.out.println("Exception during SQL Query: " + ex);
            return null;
        }

    }

    @Override
    public LinkedList<GraphLink> getPatientVisitsGraph() {
        throw new UnsupportedOperationException("Not supported yet."); //To change body of generated methods, choose Tools | Templates.
    }
}
