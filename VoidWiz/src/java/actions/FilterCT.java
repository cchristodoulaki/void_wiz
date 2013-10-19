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
import dao.ClinicalTrialDAO;
import dao.DAOfactory;
import entity_layer.ClinicalTrial;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.LinkedList;
import javax.servlet.ServletException;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;


public class FilterCT implements Action {

    private DAOfactory factory = DAOfactory.getDAOfactory("mysql");
    private ClinicalTrialDAO trial_dao = factory.getClinicalTrialDAO();
    
    @Override
    public boolean execute(HttpServletRequest req, HttpServletResponse res) throws ServletException, IOException {
        System.out.println("^^^^^^######### hello hello Filterrrr");
        int nodeid =  Integer.parseInt(req.getParameter("nodeid")); 
        String attrtype = req.getParameter("attrtype");
        String nodename =  req.getParameter("attrname"); 
        LinkedList<ClinicalTrial> trials = trial_dao.getClinicalTrials(nodename, attrtype);

        System.out.println("Request says node id is: "+nodeid+" "+attrtype+" "+nodename);
        String json = "{\"trials\":{";
       PrintWriter out = res.getWriter();
        for (int i = 0; i < trials.size(); i++) {
            json += "\"" + trials.get(i).getTupleid()+ "\":{";
            json += " \"ctid\" : \""+ trials.get(i).getCtid() +"\",";
            json += " \"country\" : \""+ trials.get(i).getCountry() +"\",";
            json += " \"source\" : \""+ trials.get(i).getSource()+"\",";
            json += " \"medcondition\" : \""+ trials.get(i).getCondition()+"\",";
            json += " \"drug\" : \""+ trials.get(i).getDrug()+"\"";
            json += "},";
        }
        if(json.endsWith(","))
            json = json.substring(0, json.length()-1);
        json = json + "}}";
        System.out.println("sending Json string:\n"+json);
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


        
