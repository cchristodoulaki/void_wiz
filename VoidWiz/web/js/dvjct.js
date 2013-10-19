/* 
 * @author Christina Christodoulakis
 * @email christina at cs.toronto.edu
 * University of Toronto, Database Group

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
var maxLinks = 3; // if I add country it will be 4
var w = 920, h = 650;
//var w = 4000,
//    h = 2000;
var vis, loading, loadingText;
var incomplete = [];
var tagNames = [];
var drag;
var force, path, node, graphdata, focusednode, selected = -1;
var dnodes = [];
var dlinks = [];
var zoomFactor = 4, zoom = d3.behavior.zoom();
var trans = [0, 0];
var scale = 1;
var centerX = w / 2;
var centerY = h / 2;

var linkedByIndex = {};

function isNodeConnected(a, b) {
    return linkedByIndex[a.index + "," + b.index] || linkedByIndex[b.index + "," + a.index] || a.index == b.index;
}


function getNeighbors(d) {

    var neigh = [];
    $.each(dlinks, function(index, value) {
        if (value.source === d)
            neigh.push(value.target);
        if (value.target === d)
            neigh.push(value.source);
    });
    return neigh;
}

function printNeighbors(d) {
    var neigh = getNeighbors(d);
    var neighInfo = "";
    $.each(neigh, function(index, value) {
        neighInfo = neighInfo + value.name + ", (" + value.type + ")<br>";
    });
    return neighInfo;
}

d3.json("data/newCanada_ctgraph.json", function(error, data) {
//d3.json("data/US_ctgraph.json", function(error, data) {
    graphdata = data;
    dnodes = data.nodes;
    dlinks = data.links;
    dlinks.forEach(function(d) {
        linkedByIndex[d.source + "," + d.target] = 1;
    });

    magic();
    loadingSvg = vis.append('svg').attr('width', 550).attr('height', 150).attr("x", (w / 2) - 300).attr("y", h / 2);
    loadingBox = loadingSvg.append("rect")
//            .attr("x", (w / 2) - 300).attr("y", h / 2)
            .attr("rx", 20).attr("ry", 20)
            .attr("width", 550).attr("height", 150)
            .attr("class", "loadingbox")
    loadingText = loadingSvg.append("text")
            .attr("class", "loading")
            .attr("x", (550 / 2) - 220)
            .attr("y", 80)
            .text("Loading");
});
function magic() {
    $("#graphViz").empty();

    numtrials = dnodes.filter(function(element) {
        return (element.type === "ctid");
    }).length;
    numsources = dnodes.filter(function(element) {
        return (element.type === "source");
    }).length;
    numconditions = dnodes.filter(function(element) {
        return (element.type === "medcondition");
    }).length;
    numdrugs = dnodes.filter(function(element) {
        return (element.type === "drug");
    }).length;

    stats = "<strong>" + dnodes.length + "</strong> nodes"
            + "<ul>\n\
<li>" + numtrials + " trials</li>\n\
<li>" + numsources + " sources</li>\n\
<li>" + numconditions + " conditions</li>\n\
<li>" + numdrugs + " drugs</li>\n\
</ul>"
            + "<br><strong>" + dlinks.length + "</strong> links.";

    $("#graphStats").append(stats);

    vis = d3.select("#graphViz").append("svg")
            .attr("class", "span11 graphviz nomargin")
            //.attr('fill', '#eaf7f9')
            .attr('fill', '#fff')
            //start pan and zoom code
            .attr("pointer-events", "all")
            .attr("perserveAspectRatio", "xMinYMid") //dunno why/if this is needed, do not erase
            .append('svg:g')
            .call(zoom.on("zoom", redraw))
            .append('svg:g');
    // this is so that I dont have to drag the graph specifically, i can just drag the area
    vis.append('svg:rect')
            .attr('width', 10 * w)
            .attr('height', 10 * h);
//            .attr('fill', '#eaf7f9');//this makes the dragable rect blue, proves there is a bug.. :/

    //this is to support zoom
    function redraw() {
        trans = d3.event.translate;
        scale = d3.event.scale;
        vis.attr("transform",
                "translate(" + trans + ")"
                + " scale(" + scale + ")");
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
    /**
     * for each node (value) find all his links and count how many different types of links it has*/
    $.each(dnodes, function(index, value) {
        tagNames.push(value.name);
        var conditions = 0;
        var sources = 0;
        var drugs = 0;
        // are we looking at a tuple identifier? figure out if tuple has null values
        if (value.type === "ctid") {
            linksofNode = $.grep(dlinks, function(v) {
                return v.source === index;
            });
// add this in back later
//            if (existsLink(linksofNode, "COUNTRY")) {
//                nlinktype = nlinktype + 1;
//            }
            $.each(linksofNode, function(index, value) {
                if (dnodes[value.target].type === "source") {
                    sources = sources + 1;
                }
                if (dnodes[value.target].type === "medcondition") {
                    conditions = conditions + 1;
                }
                if (dnodes[value.target].type === "drug") {
                    drugs = drugs + 1;
                }
            });

            if (sources === 0 || conditions === 0 || drugs === 0)
                incomplete.push(index);
        }
    });

    jQuery.noConflict();
    $("#tags").autocomplete({
        source: tagNames,
        select: function(event, ui) {
            //remove focus from old node (MUST go back to old color, not blue!! :/)
            vis.selectAll(focusednode).attr("r", 5).style("fill", "blue");
            focusednode = "#circle-" + findid(ui.item.value); //must replace , as well
            var transx = (-parseInt(vis.selectAll(focusednode).data()[0].x) * zoomFactor + centerX),
                    transy = (-parseInt(vis.selectAll(focusednode).data()[0].y) * zoomFactor + centerY);// alert("(x, y) = ("+vis.selectAll(nodeId).data()[0].x+", "+vis.selectAll(nodeId).data()[0].y+")\n(transx, transy) = ("+transx+", "+transy+")")
            vis.transition().attr("transform", "translate(" + transx + "," + transy + ")scale(" + zoomFactor + ")");
            vis.selectAll(focusednode).attr("r", 15).style("fill", "yellow"); 
            toggledetail(vis.selectAll(focusednode).data()[0], vis.selectAll(focusednode).attr()[0]);
            zoom.scale(zoomFactor);
            zoom.translate([transx, transy]);
        }
    });

    force = self.force = d3.layout.force()
            .nodes(dnodes)
            .links(dlinks)
            .linkDistance(100)// length of edges between connected nodes
            .charge(-300)//increassing negative charge makes nodes repulse each other
            .gravity(0.2)
            .size([w, h])
            .on("tick", tick);
    path = vis.selectAll("path");
    node = vis.selectAll("g.node");
    start();
}

function findid(name) {
    for (var n in dnodes) {
        if (dnodes[n].name === name)
            return dnodes[n].nodeid;
    }
}

function start() {
    path = path.data(dlinks);
    path.enter()
            .append("svg:path")
            .attr("class", function(d) {
        return "link " + d.age;
    }).attr("marker-end", "url(#end)");

    path.exit().remove();
    node = node.data(dnodes);
    node.enter().append("svg:g").attr("class", function(d) {
        var c = "node";
        if (incomplete.indexOf(dnodes.indexOf(d)) > -1)
        {
            c = c + " incompleteTupleKey";
            //alertNulls(d.name);
        }
        return c;
    });

    node.append("circle").attr("id", function(d) {
        return "circle-" + d.nodeid;
    }).attr("class", function(d) {
        return "node " + d.type;
    }).attr("toggled", "off")
            .attr("r", function(d) {
        if (d.type === "tuple_identifier")
            return 2;

        else {
            var neigh = getNeighbors(d.nodeid);
            return 5 + Math.sqrt(neigh.length);
        }
    }).on("click", function(d) {
        toggledetail(d, this);
    }).append("title")
            .text(function(d) {
        return d.name;
    }).call(force.drag);

    $('svg circle').tipsy({
        gravity: 'w',
        html: true,
        title: function() {
            var d = this.__data__;
            var html = "<table ><col align=\"left\"><tr><td>Node name: " + d.name + " </td></tr>\n\
<tr><td>Node type: " + d.type +
                    "</td></tr><tr><td>Connected to: " + getNeighbors(d).length+" nodes.</td></tr>"+
                    "<tr><td>Select node for details.</td></tr></table>";
            return html;
        }
    });

//add the text/name of nodes
    node.append("svg:text")
            .attr("x", 5)//how far on x axis the text will appear (from the node)
            .attr("class", "nodetext")
            .attr("dx", 16)
            .attr("dy", ".25em")
            .text(function(d) {
        return d.name;
    });
    node.exit().remove();
    vis.selectAll(".node#incomplete").attr("r", 50).style("fill", "red");
    force.start();
}
function toggledetail(d, n) {
        if (n.getAttribute("toggled") === "off") {
            n.setAttribute("toggled", "on");
            fade(d, .2, d.nodeid);
            //displayTuples(d);
        } else {
            n.setAttribute("toggled", "off");
            fade(d, 1, -1);
        }
    }
    // fade code adapted from https://gist.github.com/christophermanning/1625629
    function fade(d, opacity, select) {
        console.log("d=" + d.name);
        node.style("fill-opacity", function(o) {
            var isNodeConnectedBool = isNodeConnected(d, o);
            var thisOpacity = isNodeConnectedBool ? 1 : opacity;
            if (!isNodeConnectedBool) {
                this.setAttribute('style', "stroke-opacity:" + opacity + ";fill-opacity:" + opacity + ";");
            }
            return thisOpacity;
        });
        selected = select;
        
        path.style("stroke-opacity", function(o) {
            return o.source === d || o.target === d ? 1 : opacity;
        });
        if(selected!==-1){
        populateCTTable();
        addBBPtools();
    }else{ $("#filtered_data").empty();    $("#toolbox").empty(); $("#bbp_results").empty();}

    }
function tick(e) {
//        if (selected === -1) {
//            console.log("attempting to focus");
//            var k = .1 * e.alpha;
//            dnodes.forEach(function(o, i) {
//                var isNodeConnectedBool = isNodeConnected(selected, o);
//
//                if (isNodeConnectedBool) {
//                    o.y += (vis.selectAll("#circle-" + selected).data()[0].y - o.y) * k;
//                    o.x += (vis.selectAll("#circle-" + selected).data()[0].x - o.x) * k;
//                }
//            });
//
//        
//        }
//do not render initialization frames because they are slow and distracting
    if (e.alpha < 0.01) {
        vis.select(".loadingbox").remove();
        vis.select(".loading").remove();

        node.attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; });

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
    } else {
        if (e.alpha < 0.015) {
            node.attr("transform", function(d) {  return "translate(" + d.x + "," + d.y + ")";  });

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
        loadingText.text(function() {
            return "Calculating Optimum Layout: " + Math.round((1 - (e.alpha * 10 - 0.1)) * 100) + "%";
        });
    }
}





