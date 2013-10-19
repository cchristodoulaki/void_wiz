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
package algorithms;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import util.SystemCommandExecutor;

public class BinaryBeliefPropagation {

    private Process p;

    public BinaryBeliefPropagation(String appRoot, String commandsFile) throws IOException, InterruptedException {
        System.out.println("woohoooo BBP baby!!!");
        String s = null;
        // determine the number of processes running on the current
        // linux, unix, or mac os x system.
    List<String> commands = new ArrayList<String>();
    // shell script that executes bbp_shelve.py by Christos Faloutos
    
System.out.println("Looking for "+commandsFile+" in "+appRoot+commandsFile); 
commands.add("chmod");
commands.add("755");
commands.add(appRoot+commandsFile);

    SystemCommandExecutor commandExecutor = new SystemCommandExecutor(commands);
    System.out.println("Going to execute the command");
    int result = commandExecutor.executeCommand();

    // stdout and stderr of the command are returned as StringBuilder objects
    StringBuilder stdout = commandExecutor.getStandardOutputFromCommand();
    StringBuilder stderr = commandExecutor.getStandardErrorFromCommand();
    System.out.println("The numeric result of the command was: " + result);
    System.out.println("\nSTDOUT:");
    System.out.println(stdout);
    System.out.println("\nSTDERR:");
    System.out.println(stderr);
    
    List<String> commands2 = new ArrayList<String>();
    commands2.add(appRoot+commandsFile);
    SystemCommandExecutor commandExecutor2 = new SystemCommandExecutor(commands2);
    System.out.println("Going to execute the command");
    int result2 = commandExecutor2.executeCommand();

    // stdout and stderr of the command are returned as StringBuilder objects
    stdout = commandExecutor.getStandardOutputFromCommand();
    stderr = commandExecutor.getStandardErrorFromCommand();
    System.out.println("The numeric result of the command was: " + result2);
    System.out.println("\nSTDOUT:");
    System.out.println(stdout);
    System.out.println("\nSTDERR:");
    System.out.println(stderr);
    }

    public Process getP() {
        return p;
    }
    
    
    
}
