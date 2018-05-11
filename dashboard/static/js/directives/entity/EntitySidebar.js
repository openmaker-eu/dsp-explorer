import * as _ from 'lodash'
import * as d3 from 'd3';
let template = `
    <div class="entity-sidebar background-{$ entityname $}--light col-md-12">
        <div class="row" ng-repeat="slider_name in slider_list">
   
            <entity-carousel
                entityname="{$ slider_name $}"
                userid="{$ entityid $}"
                class="col-md-12 col-sm-12 margin-top-5-per margin-bottom-5-perc"
            ></entity-carousel>
            
        </div>
    </div>
`
export default [function(){
    return {
        template:template,
        scope: {
            entityname: '@',
            userid: '@',
            sidebartype:'@',
            slider : '@',
        },
        controller : ['$scope', '$http', 'toastr', '$rootScope', function($scope, $http, toastr, $rootScope) {
            $scope.sidebartype = $scope.sidebartype || 'entity'
            $scope.slider_list = $scope.slider ? $scope.slider.split('-').filter(x => x): []
        }]
    }
}]



