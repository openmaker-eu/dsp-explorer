import * as _ from 'lodash'
import * as d3 from 'd3';

let template = `
    <div class="row">
        <svg id="pie_container"></svg>
    </div>
    <style>
    </style>
`

export default [function(){
    
    return {
        template:template,
        scope: {
            tags: '='
        },
        controller : ['$scope','$http', function($scope, $http){
            $http.get('/api/v1.1/get_sectors').then( (results)=>{
                pie('#pie_container', _.get( results, 'data.sectors' ) );
            })
        }]
    }
    
}]

let pie = (div_id, sectors) => {
    
    let bar_height = 50;
    let bar_margin = 5;
    
    var container =  $(div_id)
    var parent = container.parent()
    var diameter = parent.width()
    
    var width = diameter;
    var height = (sectors.length * bar_height)+(sectors.length * bar_margin);
    
    container.attr('width' , width)
    container.attr('height' , height)
    
    var data = _.orderBy(sectors, 'size', 'desc')
    var colorScale = d3.scaleQuantile()
        .domain([ 0 , (data.length-1)/4, (data.length-1)/2 , (data.length-1)])
        .range([ '#efefef', '#db4348', '#ff97a1', '#bbbbbb'])
    
    
    var svg = d3.select(div_id).append("g")
    
    var x = d3.scaleLinear()
        .range([0, width])
        .domain([0, d3.max(data, function (d) {
            return d.size;
        })]);
    
    var y = d3.scaleBand([height, 0], .1)
        .domain(data.map(function (d) {return d.name;}));
    
    var bars = svg.selectAll(".bar")
        .data(data)
        .enter()
        .append("g")
    
    //append rects
    bars.append("rect")
        .attr("class", "bar")
        .attr("y", (d, i)=> (i * bar_height)+(i*bar_margin)  )
        .attr("height", bar_height)
        .attr("x", 0)
        .attr("width", function (d) { return x(d.size); })
        .attr("fill",  (d, i) => colorScale( Math.floor(Math.random() * (10 - 0 + 1)) + 0) )
    
    //
    bars.append('text')
        .attr("y", function(d, i){
            return (i * bar_height)+(i * bar_margin)+bar_height/2
        })
        .attr("x", function(d, i){
            return x(d.size)/2 || bar_height/2
        })
        .attr("font-family", "Arial Black")
        .attr("font-size", "20px")
        .attr("fill", "#222")
        .attr("style", 'font-weight:900;')
        .style("text-anchor", "middle")
        .text(function(d, i){ return d.name+' ('+ d.size +')'});
    
}



