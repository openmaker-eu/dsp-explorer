import * as _ from 'lodash'
import * as d3 from 'd3';

let template = `
    <div class="row">
        <svg id="bubble_container"></svg>
    </div>
    <style>
        
        circle {
          /*fill: rgb(31, 119, 180);*/
          fill-opacity: .0;
          /*stroke: rgb(31, 119, 180);*/
          /*stroke-width: 1px;*/
        }
        
        .leaf circle {
          /*fill: #ff7f0e;*/
          fill-opacity: 1;
        }
        
        text {
          font: 10px sans-serif;
          text-anchor: middle;
        }
    </style>
`

// TODO want to pass to the directive the Angular search function instead of reloading the page
export default [function(){
    
    return {
        template:template,
        scope: {
            tags: '='
        },
        controller : ['$scope','$http', 'UserSearchFactory', function($scope, $http, UserSearchFactory){
            
            $scope.bubble = bubble.bind($scope)
            $scope.filter = UserSearchFactory.search;
            
            $http.get('/api/v1.1/get_hot_tags/20/').then((results)=>{
                $scope.bubble('#bubble_container', _.get( results, 'data.tags' ))
            })
            
        }]
    }
    
}]

let bubble = function(div_id, tags){
    
    var container =  $(div_id)
    var parent = container.parent()
    
    var diameter = parent.width()
    
    container.attr('width' , diameter)
    container.attr('height' , diameter)
    
    let sizes = _.map(tags, 'size')
    
    var svg = d3.select(div_id),
        g = svg.append("g")
            .attr("transform", "translate(2,2)")
        ,
        format = d3.format(",d");
    
    var colorScale = d3.scaleQuantile()
        .domain([ 0 , (tags.length-1)/4, (tags.length-1)/2 , (tags.length-1)])
        .range([ '#efefef', '#db4348', '#ff97a1', '#bbbbbb'])
    ;
    
    var pack = d3.pack()
        .size([diameter - 4, diameter - 4]);
        var root = d3.hierarchy({name:'tags', children:tags})
            .sum(function(d) {return d.size; })
            .sort(function(a, b) { return b.value - a.value; });
        
        var node = g.selectAll(".node")
            .data(pack(root).descendants())
            .enter()
            .append("g")
            .attr("class", function(d) { return d.children ? "node" : "leaf node"; })
            .attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; })
            .attr("class", "pointer")
            .on('click', (d,i)=>{  this.filter(d.data.name, 'tags') });
            // .attr('xlink:href', d=> '/search/members/'+d.data.name+'/')
        
        node.append("title")
            .text(function(d) { return d.data.name + "\n" + format(d.value); })

        node
            .append("circle")
            .attr("r", function(d) { return d.r; } )
            .attr("fill", (d,i)=> colorScale(Math.floor(Math.random() * (10 - 0 + 1)) + 0))
            //.attr("fill", (d,i)=> colorScale(i))
    
    function getSize(d, i ,a) {
        let bbox = this.getBBox(),
            cbbox = this.parentNode.getBBox(),
            scale = Math.max(cbbox.width/bbox.width, cbbox.height/bbox.height)*1.3;
        d.scaleFontSize = scale;
    }

    node.filter(function(d) { return !d.children; })
        //.append("a")
        //.style("font-size", function(d) { return d.scaleFontSize + "px"; })
        //.attr('href', d=> '/search/members/'+d.data.name+'/')
        .append("text")
        .attr("dy", "0.3em")
        .text(function(d) { return d.data.name })
        .each(getSize)
        .style("font-size", function(d) { return d.scaleFontSize + "px"; })
        .style("font-weight", 900 )
        .style("fill", '#353535')
    
    
}



