import * as _ from 'lodash'
import * as d3 from 'd3';
let template = `
    <div class="">
        <div class="col-md-12" ng-if="entities.length == 0">
            <h2>
                Loading {$ entityname $}...
            </h2>
        </div>
        
        <!--Left content-->
        <div class="col-md-9 entity-content mycontent-left" >
            <div ng-if="entities.length > 0">
                <!--Entity title-->
                <div class="col-md-12">
                    <h1 style="text-transform: uppercase"><span>{$ entityname $}</span><h1>
                </div>
                
                <!--Entity list-->
                <div
                    class="col-md-3 col-sm-3 col-xs-12 "
                    ng-repeat="entity in entities"
                    style="margin-bottom:1%; margin-top: 1%;"
                >
                    <div class="col-md-12 entity-list__box">
                        <entity-preview entity="entity" entityname="{$ entityname $}" entityid="{$ entity.link_id || entity.id $}"></entity-preview>
                    </div>
                </div>
            </div>

        </div>
    
        <!--Right sidebar-->
        <div class="col-md-3 entity-sidebar background--{$ entityname $}">
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
            profileid : '=',
            entityname : '@',
            slider : '@'
        },
        controller : ['$scope', '$http', 'toastr', function($scope, $http, toastr) {
            let url = ''
            $scope.entities = []
            $scope.slider_list = $scope.slider ? $scope.slider.split('-').filter(x => x): []
            $scope.get_data = (url) => {
                $http.get(url).then(res => {
                    $scope.entities = res.data.result || []
                    console.log(res);
                    //$scope.$apply(()=>$(window).trigger('resize'))
                })
            }
            let id = $scope.profileid? '/'+$scope.profileid : '/'
            $scope.get_data('/api/v1.4/' + $scope.entityname + id)

        }]
    }
}]



