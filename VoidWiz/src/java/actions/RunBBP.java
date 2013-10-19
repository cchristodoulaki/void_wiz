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
 * @email christina at cs.toronto.edu Computer Science, University of Toronto 2013
 */
package actions;

import algorithms.BinaryBeliefPropagation;
import controlLayer.Action;
import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.logging.Level;
import java.util.logging.Logger;
import javax.servlet.ServletContext;
import javax.servlet.ServletException;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

public class RunBBP implements Action {

    @Override
    public boolean execute(HttpServletRequest req, HttpServletResponse res) throws ServletException, IOException {
        System.out.println("In RunBBP");
         PrintWriter out = res.getWriter();String appRoot="";
        try {
            ServletContext ctx = req.getServletContext();
            appRoot = ctx.getRealPath("/");
            appRoot = System.getProperty("catalina.home")+"/webapps/VoidWiz/BBP/";
            new BinaryBeliefPropagation(appRoot, "belief.sh");
            
        } catch (InterruptedException ex) {
            Logger.getLogger(RunBBP.class.getName()).log(Level.SEVERE, null, ex);
        }
        String json = getProbJson(appRoot);
//        System.out.println(json);
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
    
    /**
     * Reads from bbpresults.csv and creates json file that 
     * looks like this:
     * {probableNodes:{
     *      {id:1,prob:0.71},
     *      {id:5,prob:0.53},
     *      {id:15,prob:0.6}
     * }}
     */
    public String getProbJson(String appRoot) {
        System.out.println("---> Read the results of bbp");
        String csvFile = appRoot+"bbpresults.csv";
        String json = "{\"probableNodes\":[";
        BufferedReader br = null;
        String line = "";
        String cvsSplitBy = "\\|";

        try {

            br = new BufferedReader(new FileReader(csvFile));
            while ((line = br.readLine()) != null) {
                // use comma as separator
//                System.out.println(line);
                String[] suggestion = line.split(cvsSplitBy);
//                System.out.println();
//                System.out.println("{\"id\":\"" + suggestion[0] + "\",\"prob\":\"" + suggestion[1] + "\"},");
//                
                json += "{\"id\":\"" + suggestion[0] + "\",\"prob\":\"" + suggestion[1] + "\"},";
            }
            if (json.endsWith(",")) {
                json = json.substring(0, json.length() - 1);
            }
        } catch (FileNotFoundException e) {
            System.out.println("File not found");
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
        json += "]}";
System.out.println("json Prob object is: "+json);
        return json;

    }
}
