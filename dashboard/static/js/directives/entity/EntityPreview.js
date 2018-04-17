import * as _ from 'lodash'
import * as d3 from 'd3';
let template = `
    <div class="entity--{$ entityname $} entity-preview " style="padding:4%;">
        <h3 class="text--{$ entityname $}">
            <span>{$ entity.title || entity.name | limitTo: 20 $}</span>
            <span ng-if="entity.title.length > 20">...</span>
        </h3>
        <br>
        <div class="limit-line fade-container">
            <div ng-if="entity.full_text">{$ entity.full_text $}</div>
            
            <div class="fade">
                <!--EVENT ONLY: Event details with icons-->
                <div ng-if="entityname == 'events'" style="z-index:10000;">
                    <p><i class="fa fa-calendar"></i>&nbsp;&nbsp;{$ entity.start_time |  date : 'd MMMM yyyy,EEEE'  $}</p>
                    <p><i class="fa fa-map-marker"></i>&nbsp;&nbsp;{$ entity.place $}</p>
                    <a href="{$ entity.link $}" target="_blank">
                        <p><i class="fa fa-plus-square"></i>&nbsp;&nbsp;REGISTER</p>
                    </a>
                </div>
                <!--Read more-->
                <a ng-if="entityid" href="/{$ entityname $}/{$ entityid $}" class="read-more"><h4>READ MORE </h4></a>
            </div>
        </div>

    </div>
`
export default [function(){
    return {
        template:template,
        scope: {
            entity: '=',
            entityname: '@',
            entityid : '@',
        },
        controller : ['$scope', '$http', 'toastr', '$rootScope', function($scope, $http, toastr, $rootScope) {
            
            // $scope.get_data = (url) => {
            //     $http.get(url).then(res => {
            //         $scope.entity = res.data.result[0] || []
            //         $scope.$apply(()=>$(window).trigger('resize'))
            //     })
            // }
            
            //$scope.get_data('/api/v1.4/' + $scope.entityname + '/details/' + $scope.entityid + '/')
            //$scope.get_data('/api/v1.4/' + $scope.entityname + '/details/' + $scope.entityid + '/')
            
        }]
    }
}]



