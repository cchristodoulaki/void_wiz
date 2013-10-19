/* 
 * @author Christina Christodoulakis
 * @email christina'@'cs.toronto.edu


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
var maxLinks = 4;
var w = 600, h = 400;
var vis;
var incomplete = [];
var force, path, node;
var dnodes = [];
var dlinks = [];
d3.json("data/visitswithnulls.json", function(error, data) {
    dnodes = data.nodes;
    dlinks = data.links;
    vis = d3.select("#graphViz").append("svg")
            .attr("width", w)
            .attr("height", h)
            //start pan and zoom code
            .attr("pointer-events", "all")
            .append('svg:g')
            .call(d3.behavior.zoom().on("zoom", redraw))
            .append('svg:g');
    // this is so that I dont have to drag the graph specifically, i can just drag the area
    vis.append('svg:rect')
            .attr('width', w)
            .attr('height', h)
            .attr('fill', 'white');
    //this is to support zoom
    function redraw() {
        //console.log("here", d3.event.translate, d3.event.scale);
        vis.attr("transform",
                "translate(" + d3.event.translate + ")"
                + " scale(" + d3.event.scale + ")");
    }
    // build the arrow.
    vis.append("svg:defs").selectAll("marker")
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

    $.each(dnodes, function(index, value) {
        // are we looking at a tuple identifier? figure out if tuple has null values
        if (value.type === "tupleId") {
            linksofNode = $.grep(dlinks, function(v) {
                return v.source === index;
            });
            if (linksofNode.length < maxLinks)
                incomplete.push(index);
        }
    });

    force = self.force = d3.layout.force()
            .nodes(dnodes)
            .links(dlinks)
            .distance(100)
            .charge(-1000)
            .size([w, h])
            //.start()
            .on("tick", tick);

    path = vis.selectAll("path");
    node = vis.selectAll("g.node");
    start();
});

function start() {
    path = path.data(dlinks);
    path.enter()
            .append("svg:path")
            .attr("class", function(d) {return "link " + d.age;})
            .attr("marker-end", "url(#end)");
    path.exit().remove();
    
    node = node.data(dnodes);
    node.enter().append("svg:g").attr("class", function(d) {
        var c = "node";
        if (incomplete.indexOf(dnodes.indexOf(d)) > -1)
        {
            c = c + " incompleteTupleKey";
            alertNulls(d.name);
        }
        return c;
    }).attr("id", function(d) {
        if (incomplete.indexOf(dnodes.indexOf(d)) > -1)
            return "incomplete";
    }).call(force.drag);

    node.append("circle")
            .attr("class", function(d) {return "node " + d.type;})
            .attr("r", 5).call(force.drag);
    
    //give the nodes an icon
    node.append("svg:image")
            .attr("class", "circle")
            .attr("xlink:href", function(d) {return d.img_href;})
            .attr("x", "-16px")
            .attr("y", "-16px")
            .attr("width", "32px")
            .attr("height", "32px");

//add the text/name of nodes
    node.append("svg:text")
            .attr("x", 5)//how far on x axis the text will appear (from the node)
            .attr("class", "nodetext")
            .attr("dx", 16)
            .attr("dy", ".25em")
            .text(function(d) {return d.name;});
    
    node.exit().remove();
    vis.selectAll(".node#incomplete").style("fill", "red").attr("r", 20);
    force.start();
}


function tick() {
    node.attr("transform", function(d) {
        return "translate(" + d.x + "," + d.y + ")";
    });
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
}


