/**
 * Created by andreafspeziale on 03/05/17.
 */
import * as d3 from 'd3';
export default [ '$scope','$uibModal','$http', function ($scope,$uibModal,$http) {

    let root_node_size = 30;
    let child_node_size = 20;
    let data_nodes = [{id: 0, amount:root_node_size, name:"ARDUINO"},
        {id: 1, amount: root_node_size, name:"3D PRINTER"},
        {id: 2, amount: root_node_size, name:"RASPBERRY Pi"},
        {id: 3, amount: child_node_size, name:"Raspberry_Pi"},
        {id: 4, amount: child_node_size, name:"arduino"},
        {id: 5, amount: child_node_size, name:"make"},
        {id: 6, amount: child_node_size, name:"3dprintindustry"},
        {id: 7, amount: child_node_size, name:"3DPrintGirl"},
        {id: 8, amount: child_node_size, name:"3dersorg"},
        {id: 9, amount: child_node_size, name:"htpc_guides"},
        {id: 10, amount: child_node_size, name:"hackaday"},
    ];
    let data_links = [{'source': 0, 'target': 1},
        {'source': 0, 'target': 2},
        {'source': 1, 'target': 2},
        {'source': 0, 'target': 3},
        {'source': 0, 'target': 4},
        {'source': 0, 'target': 5},
        {'source': 1, 'target': 6},
        {'source': 1, 'target': 7},
        {'source': 1, 'target': 8},
        {'source': 2, 'target': 3},
        {'source': 2, 'target': 9},
        {'source': 2, 'target': 10}];
    createNetwork(data_links, '#theme_graph', '#DB4348', data_nodes)

}]

function createNetwork(data_links, svg_id, c, data_nodes){
    let svg = d3.select(svg_id);

    let simulation = d3.forceSimulation(data_nodes)
        .force('link', d3.forceLink(data_links).distance(50).strength(0.01))
        .force('charge', d3.forceManyBody())
        .force('center', d3.forceCenter(300, 300))
        .on('tick', tick);

    let links = svg.append("g")
        .attr("class", "links")
        .selectAll("line")
        .data(data_links)
        .enter()
        .append('line')
        .style('stroke', '#7A7378');

    let nodes = svg.selectAll(".node")
        .data(data_nodes)
        .enter().append("g")
        .attr("class", "node")
        .call(d3.drag()
            .on("start", dragstarted)
            .on("drag", dragged)
            .on("end", dragended))
        .on('mouseover', function(d){
            d3.select(this).select('text')
                .transition()
                .duration(200)
                .attr('opacity', 1)
        })
        .on("mouseout", function(d) {
            d3.select(this).select('text')
                .transition()
                .duration(200)
                .attr('opacity', function(d){
                    return get_opacity_for_node(d);
                })
        });

    let node = nodes.append('circle')
        .style('fill', function (d) {
            if(is_source_node(d)){
                return c;
            }else{
                return '#1CA4A4';
            }
        })
        .attr('r', (d) => d.amount);

    let nodeText = nodes.append("text")
        .attr('opacity', function(d){
            return get_opacity_for_node(d);
        })
        .text((d) => d.name);

    function is_source_node(d){
        return d.id == 0 || d.id == 1 || d.id == 2
    }

    function get_opacity_for_node(d){
        if(is_source_node(d)){
            return 1
        }
        return 0
    }

    function tick () {
        node.attr('cx', (d) => d.x)
            .attr('cy', (d) => d.y);
        links.attr('x1', (d) => d.source.x)
            .attr('y1', (d) => d.source.y)
            .attr('x2', (d) => d.target.x)
            .attr('y2', (d) => d.target.y);
        nodeText.attr('x', (d) => d.x)
            .attr('y', (d) => d.y)
    }

    function dragstarted(d) {
        if (!d3.event.active) simulation.alphaTarget(0.3).restart();
        d.fx = d.x;
        d.fy = d.y;
    }

    function dragged(d) {
        d.fx = d3.event.x;
        d.fy = d3.event.y;
    }

    function dragended(d) {
        if (!d3.event.active) simulation.alphaTarget(0);
        d.fx = null;
        d.fy = null;
    }

}