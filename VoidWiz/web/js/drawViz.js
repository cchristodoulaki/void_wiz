/* 
 * @author Christina Christodoulakis
 * @email christina'@'cs.toronto.edu
 */
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


// get the data
d3.csv("data/patientVisitGraph.csv", function(error, links) {

    var incomplete = [];
    var nodes = {};

    // Compute the distinct nodes from the links.
    //You have an array of connections links. Afterwards you extract the distinct nodes from this array by these lines:
    // http://stackoverflow.com/questions/13361214/how-to-change-the-circles-style-using-d3-js
    links.forEach(function(link) {
        if (link.target === "") {
            incomplete.push(link.source);
        }
        link.source = nodes[link.source] || (nodes[link.source] = {name: link.source});
        link.target = nodes[link.target] || (nodes[link.target] = {name: link.target});
        link.value = +link.value;
    });

    var width = 860, height = 400;
    var force = d3.layout.force()
            .nodes(d3.values(nodes))
            .links(links)
            .size([width, height])
            .linkDistance(60)
            .charge(-300)
            .size([300, 300])
            .on("tick", tick)
            .start();

    var svg = d3.select("#graphViz").append("svg")
            .attr({
        "width": "100%",
        "height": height
    })//start pan and zoom code
            .attr("pointer-events", "all")
            .append('svg:g')
            .call(d3.behavior.zoom().on("zoom", redraw))
            .append('svg:g');

    svg.append('svg:rect')
            .attr('width', width)
            .attr('height', height)
            .attr('fill', 'white');

    function redraw() {
        //console.log("here", d3.event.translate, d3.event.scale);
        svg.attr("transform",
                "translate(" + d3.event.translate + ")"
                + " scale(" + d3.event.scale + ")");
    }
/////end allow pan and zoom

    // build the arrow.
    svg.append("svg:defs").selectAll("marker")
            .data(["end"])      // Different link/path types can be defined here
            .enter().append("svg:marker")    // This section adds in the arrows
            .attr("id", String)
            .attr("viewBox", "0 -5 10 10")
            .attr("refX", 15)
            .attr("refY", -1.5)
            .attr("markerWidth", 6)
            .attr("markerHeight", 6)
            .attr("orient", "auto")
            .append("svg:path")
            .attr("d", "M0,-5L10,0L0,5");

    // add the links and the arrows
    var path = svg.append("svg:g").selectAll("path")
            .data(force.links())
            .enter().append("svg:path")
            //    .attr("class", function(d) { return "link " + d.type; })
            .attr("class", "link")
            .attr("marker-end", "url(#end)");

    // define the nodes
    var node = svg.selectAll(".node")
            .data(force.nodes())
            .enter().append("g")
            .attr("class", function(d) {
        var c = "node";
        if (incomplete.indexOf(d.name) > -1)
        {
            c = c + " incompleteTupleKey";
            alertNulls("ahoy!!! "+d.name);
        }
        return c;
    }).attr("id", function(d) {
        console.log("node id is id_" + d.name);
        if (incomplete.indexOf(d.name) > -1)
            return "incomplete";
        return "id_" + d.name;
    })// cc added this to give the nodes an id
            .call(force.drag);

    // looks for nodes with id="id_", and removes them from the graph
    //todo: instead of id it should be a class 'nullNode'
    //todo: remove links
    svg.selectAll(".node#id_").data([]).exit().remove();//this is gold do NOT change unless sure

    svg.selectAll(".node#incomplete").style("fill", "red");
    // add the nodes
    node.append("circle").attr("r", 5);



    // add the text 
    node.append("text")
            .attr("x", 10)
            .attr("dy", ".65em")
            .text(function(d) {return d.name;
    });

    // add the curvy lines
    function tick() {
        path.attr("d", function(d) {
            var dx = d.target.x - d.source.x,
                    dy = d.target.y - d.source.y,
                    dr = Math.sqrt(dx * dx + dy * dy);
            return "M" +
                    d.source.x + "," +
                    d.source.y + "A" +
                    dr + "," + dr + " 0 0,1 " +
                    d.target.x + "," +
                    d.target.y;
        });

        node
                .attr("transform", function(d) {
            return "translate(" + d.x + "," + d.y + ")";
        });
    }

});

