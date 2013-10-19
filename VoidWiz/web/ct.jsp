<%-- 
    Document   : ct.jsp
    Created on : Jul 5, 2013, 12:22:59 PM
    Author     : Christina Christodoulakis
    
    University of Toronto, Database Group
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
--%>

<%@page contentType="text/html" pageEncoding="UTF-8"%>
<!DOCTYPE html>
<!--[if lt IE 7]>      <html class="no-js lt-ie9 lt-ie8 lt-ie7"> <![endif]-->
<!--[if IE 7]>         <html class="no-js lt-ie9 lt-ie8"> <![endif]-->
<!--[if IE 8]>         <html class="no-js lt-ie9"> <![endif]-->
<!--[if gt IE 8]><!--> <html class="no-js"> <!--<![endif]-->
    <head>
        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
        <title>Fill the Void </title>
        <meta name="description" content="">
        <meta name="viewport" content="width=device-width">
        <link rel="stylesheet" href="css/bootstrap.css">
        <link rel="stylesheet" href="css/font-awesome/css/font-awesome.min.css">
        <link rel="stylesheet" href="css/main.css">
        <link rel="stylesheet" href="http://code.jquery.com/ui/1.10.3/themes/smoothness/jquery-ui.css" />
        <script src="./js/vendor/jquery-1.10.1.min.js"></script>
        <script type='text/javascript' src="http://code.jquery.com/ui/1.9.2/jquery-ui.js"></script>
        <script src="./js/vendor/bootstrap.js"></script>
        <script src="./js/d3.v3/d3.v3.js"></script>
        <script src="./js/dvjct.js"></script>
        <script src="./js/jquery.tablesorter/jquery.tablesorter.min.js"></script>
        <script src="js/mainct.js"></script>
        <script type="text/javascript" src="./js/jquery.tipsy.js"></script>
        <link href="./css/tipsy.css" rel="stylesheet" type="text/css" />

    </head>

    <body>
        <!--[if lt IE 7]>
            <p class="chromeframe">You are using an <strong>outdated</strong> browser. Please <a href="http://browsehappy.com/">upgrade your browser</a> or <a href="http://www.google.com/chromeframe/?redirect=true">activate Google Chrome Frame</a> to improve your experience.</p>
        <![endif]-->

        <!-- This code is taken from http://twitter.github.com/bootstrap/examples/hero.html -->
        <div class="navbar navbar-inverse navbar-fixed-top">
            <div class="navbar-inner">
                <div class="container">
                    <a class="brand" href="http://www.cs.utoronto.ca/~christina/apps/VoidWiz/">VoidWiz</a>
                    <div class="nav-collapse collapse">
                        <ul class="nav">
                            <li ><a href="http://www.cs.utoronto.ca/~christina/apps/VoidWiz/">Toy</a></li>
                            <li class="active"><a href="http://www.cs.utoronto.ca/~christina/apps/VoidWiz/ct.jsp">Clinical Trials</a></li>
                            <li><a href="http://graphics.tu-bs.de/static/teaching/seminars/ss13/CG/papers/Klose02.pdf">About BBP</a></li>
                        </ul>
                    </div><!--/.nav-collapse -->

                </div>
            </div>
        </div>

        <div class="container">
            <!-- Example row of columns -->
            <div class="row" style="margin-left: 0px;">
                <ul class="nav nav-tabs">
                    <li><a href="#Graph" data-toggle="tab">
                            <h2>Graph View</h2></a></li>
                    <li><a href="#Tabular" data-toggle="tab"><h2>Tabular View</h2></a></li>
                </ul>
                <div class="tab-content span12 nomargin">
                    <div class="tab-pane active span12 nomargin" id ="Graph">
                        <p>Displaying <strong>Clinical Trials</strong> as a hypergraph. 
                            <a href="#statsModal" role="button" class="btn" data-toggle="modal">Graph stats.</a>
                            <br>
                            <!--<br>Note to self: Must perform some clustering of sorts when hovering (or selecting) a node (figure out to do it from <a href="forcecluster.html">force cluster example</a>)-->
                        </p>
                        <p><div class="ui-widget">
                            <label>Find node: </label><input id="tags"></input>
                        </div></p>
                        <!--<p><a class="btn" href="#">Legend &raquo;</a></p>-->
                        <div id="graphViz" class="span11 nomargin"></div>
                        <div  class="span1 ">
                            <div id="toolbox"></div>
                            <div id="bbp_results"></div> 
                        </div>
                        <div class="span12 nomargin " id="filtered_data"></div>
                    </div>
                    <div class="tab-pane span12 nomargin"  id="Tabular" > 
                        <div id="tuple_preview"></div> 
                    </div>

                </div>
                <!-- Modal -->
                <div id="statsModal" class="modal hide fade" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
                    <div class="modal-header">
                        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">×</button>
                        <h3 id="myModalLabel">Graph statistics</h3>
                    </div>
                    <div class="modal-body">
                        <p><span id="graphStats"></span></p>
                    </div>
                    <div class="modal-footer">
                        <button class="btn" data-dismiss="modal" aria-hidden="true">Close</button>
                        <!--<button class="btn btn-primary">Save changes</button>-->
                    </div>
                </div>
                <div id="pop-up">
                    <div id="pop-up-title"></div>
                    <div id="pop-up-content">
                        <table> <tr>
                                <td><div id="pop-img"></div></td>
                                <td><div id="pop-desc"></div></td>
                            </tr> </table>
                    </div>
                </div>
            </div>
            <hr>

            <footer class="nomargin">
                <p>&copy; <a href="http://www.cs.utoronto.ca/~christina">Christina Christodoulakis</a>, 
                    <a href="http://web.cs.toronto.edu/">University of Toronto</a>, 2013 </p><embed src="img/uoftdb.svg" type="image/svg+xml" style="float:right;"/>
            </footer>

        </div> <!-- /container -->

        <script src="//ajax.googleapis.com/ajax/libs/jquery/1.10.1/jquery.min.js"></script>
        <script>window.jQuery || document.write('<script src="js/vendor/jquery-1.10.1.min.js"><\/script>')</script>

        <script src="js/vendor/bootstrap.min.js"></script>


        <script>
            (function(i, s, o, g, r, a, m) {
                i['GoogleAnalyticsObject'] = r;
                i[r] = i[r] || function() {
                    (i[r].q = i[r].q || []).push(arguments)
                }, i[r].l = 1 * new Date();
                a = s.createElement(o),
                        m = s.getElementsByTagName(o)[0];
                a.async = 1;
                a.src = g;
                m.parentNode.insertBefore(a, m)
            })(window, document, 'script', '//www.google-analytics.com/analytics.js', 'ga');

            ga('create', 'UA-31470236-4', 'utoronto.ca');
            ga('send', 'pageview');

        </script>
    </body>

</html>
