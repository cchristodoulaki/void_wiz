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
/**
 * @author Christina Christodoulakis
 * @email christina'@'cs.toronto.edu 
 * Computer Science, University of Toronto 2013
 */
package actions;

import controlLayer.Action;
import dao.DAOfactory;
import dao.VisitDAO;
import entity_layer.PatientVisit;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.LinkedList;
import javax.servlet.ServletException;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

public class GetPatientVisits implements Action {

    private DAOfactory factory = DAOfactory.getDAOfactory("mysql");
    private VisitDAO visit_dao = factory.getVisitDAO();

    @Override
    public boolean execute(HttpServletRequest req, HttpServletResponse res) throws ServletException, IOException {
                System.out.println("In GetPatientVisits");
        String json = "{\"patientVisits\":{";
        LinkedList<PatientVisit> visits = visit_dao.getPatientVisits();
        PrintWriter out = res.getWriter();
        for (int i = 0; i < visits.size(); i++) {
            json += "\"" + visits.get(i).getVisit_id() + "\":{";
            json += " \"patientName\" : \""+ visits.get(i).getPatientName() +"\",";
            json += " \"doctorName\" : \""+ visits.get(i).getDoctorName() +"\",";
            json += " \"diagnosis\" : \""+ visits.get(i).getDiagnosis()+"\",";
            json += " \"treatment\" : \""+ visits.get(i).getTreatment() +"\"";
            json += "},";
        }
        if(json.endsWith(","))
            json = json.substring(0, json.length()-1);
        json = json + "}}";
        System.out.println(json);
        out.print(json);
        return true;
    }

    @Override
    public String getView() {
        return null;
    }

    @Override
    public Object getModel() {
        return null;
    }
}
