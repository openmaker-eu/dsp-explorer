import * as _ from 'lodash'
import * as d3 from 'd3';
let template = `
    <div class="col-md-12" ng-if="entities.length == 0">
        <h2>
            No Entities
        </h2>
    </div>
    <div class="col-md-8 col-md-offset-1 mycontent-left">
        <div class="col-md-3 col-sm-3 col-xs-12"
            ng-repeat="entity in entities"
            style="margin-bottom:1%; margin-top: 1%;">
            <div class="card margin-bottom-20">

                <a href="/news/{$entity.link_id$}" class="card-image" style="border-bottom:solid 1px rgba(160, 160, 160, 0.2);">
                    <div class="card-image" style="border-bottom:solid 1px rgba(160, 160, 160, 0.2);">
                        <img style="min-width:100%;" ng-src="" class="img-responsive">
                    </div>
                </a>
                <div class="card-content"><h5>{$ entity.title $}</h5></div>
                <div class="card-action" style="height: auto;">
                    <div class="row">
                        <div class="col-md-12">
                        </div>
                        <div class="col-md-12">
                            <hr>
                        </div>
                        <div class="col-md-12 text-right">
                            <a href="/news/{$entity.link_id$}"><p>Read more <i class="glyphicon glyphicon-new-window"></i></p></a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <div class="col-md-3 entity-sidebar" style="background:#bbb;">
        <entity-carousel 
            ng-repeat="slider_name in slider_list" 
            entityname="{$ slider_name $}"
            class=""
        >
        </entity-carousel>
    </div>
`

export default [function(){
    return {
        template:template,
        scope: {
            profileid : '=',
            entity : '@',
            slider : '@'
        },
        controller : ['$scope', '$http', 'toastr', function($scope, $http, toastr) {
            let url = ''
            $scope.entities = []
            $scope.slider_list = $scope.slider ? $scope.slider.split('-').filter(x => x): []
            console.log($scope.slider_list);
            $scope.get_data = (url) => {
                $http.get(url).then(res => {
                    $scope.entities = res.data.result || []
                    //$scope.$apply(()=>$(window).trigger('resize'))
                })
            }
            let id = $scope.profileid? '/'+$scope.profileid : '/'
            $scope.get_data('/api/v1.4/' + $scope.entity + id)


        }]
    }
}]



