import * as _ from 'lodash'
import * as d3 from 'd3';

let template = `
    <div class="row">
        <svg id="bubble_container"></svg>
    </div>
    <style>
        
        .node {
          /*fill: rgb(31, 119, 180);*/
          /*fill-opacity: .0;*/
          /*stroke: rgb(31, 119, 180);*/
          /*stroke-width: 1px;*/
        }
        
        .leaf.node {
          fill-opacity: initial;
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
            tags: '=',
            standalone: '=',
            disablelinks: '=',
            maxtags: '=',
            themefilter: '=',
            themeid: '@'
        },
        controller : ['$scope','$http', 'UserSearchFactory', '$rootScope', function($scope, $http, UserSearchFactory,$rootScope){
            
            $scope.bubble = bubble.bind($scope)
            $scope.filter = UserSearchFactory.search_switch;
            $scope.factory = UserSearchFactory;
            $scope.results = ''
            console.log($scope.standalone)
            
            $scope.get_endpoint = ()=>$scope.themeid ?
                `/api/v1.3/hashtags/${$scope.themeid}/${$scope.themefilter}` :
                `/api/v1.1/get_hot_tags/${ $scope.maxtags || 20 }`
            
            $scope.get_data = ()=>
                $http.get($scope.get_endpoint()).then((results)=>{
                    $scope.results = _.get( results, 'data.result' )
                    console.log('get_data', results);
                }
            )
                    
            $scope.reload = ()=> $scope.results && jQuery('#bubble_container').html('') && $scope.bubble('#bubble_container', $scope.results)
            
            $rootScope.$on('user.search.results', $scope.reload)
            angular.element(window).on('resize', $scope.reload)
    
            // @TODO: remove pointer class on disablelinks
            $scope.$watch('themefilter',
                (new_data, old_data)=>{
                    old_data && old_data !== new_data && $scope.get_data().then( n=>console.log('0'))
                    console.log('new_data', new_data)
                    console.log('old_data', old_data)
                } )
            
            $scope.$watch('results', (new_data, old_data)=>$scope.reload())
            console.log('results sdgsd', $scope.results);
            !$scope.results && $scope.get_data()
    
        }]
    }
    
}]

let bubble = function(div_id, tags){
    console.log('rebuld bubble graph');
    var tag_default_color = this.standalone? '#db4348' : '#bbbbbb'
    // var tag_text_color = this.standalone? '#ffffff' : '#353535'
    var tag_text_color =  '#353535'

    
    var container =  $(div_id)
    var parent = container.parent()
    
    var diameter = parent.width()
    
    container.attr('width' , diameter)
    container.attr('height' , diameter)
    
    let sizes = _.map(tags, 'size')
    
    var svg = d3.select(div_id),
        g = svg.append("g")
            // .attr("transform", "translate(2,2)")
        ,
        format = d3.format(",d");
    
    var colorScale = d3.scaleQuantile()
        .domain([ 0 , (tags.length-1)/4, (tags.length-1)/2 , (tags.length-1)])
        .range([ '#efefef', '#db4348', '#ff97a1', '#bbbbbb'])
    ;
    
    var pack = d3.pack()
        .size([diameter - 4, diameter - 4]);
        var root = d3.hierarchy({name:'tags', children:tags})
            .sum(function(d) {return d.count; })
            .sort(function(a, b) { return b.value - a.value; });
        
        var node = g.selectAll(".node")
            .data(pack(root).descendants())
            .enter()
            .append("g")
            .attr("class", function(d) {
                let html_class = 'node'
                // !d.children && (html_class += ' leaf')
                !this.disablelinks && (html_class += ' pointer')
                return html_class
            })
            .attr("fill", (d) =>{
                if(d.children) return '#fff'
                return this.factory.search_filter.toLowerCase() === d.data.hashtag.toLowerCase() ? '#db4348' : tag_default_color
            })
            .attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; })
            .on('click', (d,i)=>{
                if(!this.disablelinks)
                    this.standalone ?
                    window.location = '/search/members/'+d.data.hashtag+'#tags' :
                    this.filter(d.data.hashtag, 'tags') || jQuery("html,body").animate({scrollTop: 100}, 1000)
            })
    
        node.append("title")
        
        // !this.disablelinks && node.attr("class", 'pointer')
    
        node
            .append("circle")
            .attr("r", function(d) { return d.r; } )
            // .attr("fill", (d,i)=> colorScale(Math.floor(Math.random() * (10 - 0 + 1)) + 0))
            // .attr("fill", (d,i)=> colorScale(i))
    
    function getSize(d, i ,a) {
        let bbox = this.getBBox(),
            cbbox = this.parentNode.getBBox(),
            scale = Math.max(cbbox.width/bbox.width, cbbox.height/bbox.height)*1.3;
        d.scaleFontSize = scale;
    }

    node.filter(function(d) { return !d.children; })
        .append("text")
        .attr("dy", "0.3em")
        .text(function(d) {
            if(d.data.hashtag && d.data.hashtag.length > 16){
                // return _.reduce(d.data.hashtag.match(/.{1,12}/g), (acc, el)=>  acc+'\n'+el )
                return d.data.hashtag.substring(0,12)+'...'
            }
            else return d.data.hashtag
        })
        
        .each(getSize)
        .style("font-size", function(d) { return d.scaleFontSize + "px"; })
        .style("font-weight", 900 )
        .style("fill", tag_text_color)
        .append('title')
        .text(d=>d.data.hashtag)
    
    
}



