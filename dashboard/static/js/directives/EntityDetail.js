import * as _ from 'lodash'
import * as d3 from 'd3';
let template = `
    <div class="entity--{$ entity $}">
        <div class="col-md-8 col-md-offset-1 entity-content mycontent-left">
            
            <div class="col-md-12">
                <h1 style="text-transform: uppercase">
                    <span>{$ entityname $}</span>
                    <span class="pull-right">
                        <bookmark-button entity="{$ entity $}" entityid="{$ entityid $}"></bookmark-button>
                    </span>
                <h1>
                <h2><span>test</span></h2>
            </div>
            
            <div class="col-md-3 col-sm-3 col-xs-12" style="margin-bottom:1%; margin-top: 1%;">
                <!--detail here-->
                
                
                
            </div>
        </div>
    
        <div class="col-md-3 entity-sidebar" style="background:#bbb;">
            <div ng-repeat="slider_name in slider_list" style="margin-top:5%;">
                <entity-carousel entityname="{$ slider_name $}"></entity-carousel>
            </div>
        </div>
        
    </div>
`

export default [function(){
    return {
        template:template,
        scope: {
            entityname: '@',
            entityid : '@',
            slider: '@'
        },
        controller : ['$scope', '$http', 'toastr', '$rootScope', function($scope, $http, toastr, $rootScope) {
            let url = ''
            $scope.entities = []
            $scope.slider_list = $scope.slider ? $scope.slider.split('-').filter(x => x): []
            
            $scope.get_data = (url) => {
                $http.get(url).then(res => {
                    $scope.entities = res.data.result || []
                })
            }
            $scope.get_data('/api/v1.4/' + $scope.entityname + '/' + $scope.entityid + '/')
            
        }]
    }
}]



