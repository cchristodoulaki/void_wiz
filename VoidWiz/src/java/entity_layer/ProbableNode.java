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
package entity_layer;

/**
 *
 * @author Christina Christodoulakis
 * @email christina'@'cs.toronto.edu 
 * Computer Science, University of Toronto 2013
 */
public class ProbableNode {
    
    private int nodeid;
    private float probability;

    public ProbableNode(int nodeid, float probability) {
        this.nodeid = nodeid;
        this.probability = probability;
    }

    public int getNodeid() {
        return nodeid;
    }

    public void setNodeid(int nodeid) {
        this.nodeid = nodeid;
    }

    public float getProbability() {
        return probability;
    }

    public void setProbability(float probability) {
        this.probability = probability;
    }
    
    
    
}
