import * as _ from 'lodash'
import * as d3 from 'd3';

let template = `
    <div style="width:100%;">
        <svg id="pie_container"></svg>
    </div>
    <style>
    </style>
`

export default [function(){
    
    return {
        template:template,
        controller : ['$scope','$http', '$element', 'UserSearchFactory', function($scope, $http, $element, UserSearchFactory){
            $scope.pie = pie.bind($scope)
            $scope.filter = UserSearchFactory.search_switch;
            $http.get('/api/v1.1/get_sectors').then( (results)=>{
                results = _.get( results, 'data.sectors' )
                results.length === 0 ? $('.sector-bar-container').hide() : $scope.pie('#pie_container', results )
            })
        }]
    }
    
}]

let pie = function(div_id, sectors){
    
    console.log('SEctoris : ', sectors);
    
    var container =  $(div_id)
    var parent = container.parent()
    
    var width  = parent.width()
    var height = width
    
    container.attr('width' , width)
    container.attr('height' , width)
    
    let bar_margin = 5;
    let bar_height = height/(sectors.length)-(bar_margin*2);
    
    var data = _.orderBy(sectors, (n,m)=>n<m)
    
    var maxValue = _.maxBy(data,n=>Number(n.size)).size
    
    console.log((maxValue/4)*3, (maxValue/4)*2)
    
    var colorScale = d3.scaleQuantile()
        .domain([ maxValue/4, maxValue ])
        .range([ '#efefef', '#bbbbbb', '#ff97a1', '#db4348'])
    
    var svg = d3.select(div_id).append("g")
    
    var x = d3.scaleLinear()
        .range([0, width])
        .domain([0, d3.max(data, (d) => d.size)]);
    
    var y = d3.scaleBand([height, 0], .1)
        .domain(data.map((d)=>d.name));
    
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
        .attr("fill",  (d, i) => colorScale(d.size) )
        .attr("class", "pointer")
        .on('click', (d,i)=>{  this.filter(d.name, 'sectors') })
    
    
    bars.append('text')
        .each((d)=>{
            if(maxValue/d.size > 2) { d.x = x(d.size)+bar_margin*2;  d.is_small = true}
            else { d.x = (x(d.size)/2 || bar_height/2); d.is_small = false}
        })
        .attr("y", function(d, i){
            return (i * bar_height)+(i * bar_margin)+bar_height/2
        })
        .attr("x",(d, i)=>d.x)
        .attr("font-family", "Arial Black")
        .attr("font-size", "20px")
        .attr("fill", "#222")
        .attr("style", 'font-weight:900;')
        .style("text-anchor", d=>d.is_small ? 'start' : 'middle')
        .text(function(d, i){ return d.name+' ('+ d.size +')'})
        .attr("class", "pointer")
        .on('click', (d,i)=>{  this.filter(d.name, 'sectors') })
    
}



