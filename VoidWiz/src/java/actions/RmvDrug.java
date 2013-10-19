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
 * @email christina at cs.toronto.edu
 Computer Science, University of Toronto
 * 2013
 */
package actions;

import controlLayer.Action;
import java.io.IOException;
import java.io.PrintWriter;
import javax.servlet.ServletException;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

public class RmvDrug implements Action {

    @Override
    public boolean execute(HttpServletRequest req, HttpServletResponse res) throws ServletException, IOException {
PrintWriter out = res.getWriter();
out.print("Server has not done anything yet. Supposed to remove drug from the graph csv file that bbp will read from");
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
