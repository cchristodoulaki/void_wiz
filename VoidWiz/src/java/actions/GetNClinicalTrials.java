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
package actions;

import controlLayer.Action;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.LinkedList;
import javax.servlet.ServletException;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

/**
 *
 * @author Christina Christodoulakis
 * University of Toronto, Database Group
 */
public class GetNClinicalTrials implements Action {

//    String csvFile = "/Users/christina/millerSVN/christinashared/scripts/reducedTrials.csv";
    String   csvFile = System.getProperty("catalina.home")+"/webapps/VoidWiz/data/reducedTrials.csv";

    BufferedReader br = null;
    String line = "";
    String cvsSplitBy = "\\|";

    @Override
    public boolean execute(HttpServletRequest req, HttpServletResponse res) throws ServletException, IOException {
        LinkedList<String[]> trials = new LinkedList<String[]>();
        // following is a hack
        try {
            br = new BufferedReader(new FileReader(csvFile));
            while ((line = br.readLine()) != null) {
                // use | as separator
                String[] trial = line.split(cvsSplitBy);
                trials.add(trial);
            }

        } catch (FileNotFoundException e) {
            System.out.println("File wasn't found :(");
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        } finally {
            if (br != null) {
                try {
                    br.close();
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }
        String json = "{\"trials\":{";
        PrintWriter out = res.getWriter();
        for (int i = 0; i < trials.size(); i++) {
            json += "\"" + i + "\":{";
            json += " \"ctid\" : \"" + trials.get(i)[0].replace("\"","") + "\",";
            json += " \"country\" : \"" + trials.get(i)[1].replace("\"","") + "\",";
            json += " \"source\" : \"" + trials.get(i)[2].replace("\"","") + "\",";
            json += " \"medcondition\" : \"" + trials.get(i)[3].replace("\"","") + "\",";
            json += " \"drug\" : \"" + trials.get(i)[4].replace("\"","") + "\"";
            json += "},";
        }
        if (json.endsWith(",")) {
            json = json.substring(0, json.length() - 1);
        }
        json = json + "}}";
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
