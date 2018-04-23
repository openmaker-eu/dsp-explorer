import * as _ from 'lodash'
import * as d3 from 'd3';

let template = `
    <div class="col-md-12"  >
        <div class="entity-carousel entity-carousel--{$ entityname $} entity--{$ entityname $}">
            <div class="entity-carousel__header">
                <h3><a href="/{$ entityname $}_list">{$ entityname $}</a></h3>
            </div>
            
            <entity-loading
                class="text-{$ entityname $} text-center"
                loading="entities.length == 0 "
                entityname="{$ entityname $}"
             ></entity-loading>
            
            <div class="entity-carousel__body" ng-if="entities.length > 0">
                <slick settings="slickConfig">
                    <div ng-repeat="entity in entities | limitTo: limit || undefined ">
                        <entity-preview entity="entity" entityname="{$ entityname $}" ></entity-preview>
                    </div>
                </slick>  
            <div>
        </div>
    </div>
`

export default [function(){
    return {
        template:template,
        transclude:false,
        scope: {
            profileid : '=',
            entityname : '@',
            slider : '@',
            limit: '='
        },
        controller : ['$scope', '$http', 'toastr', function($scope, $http, toastr) {
            let url = ''
            $scope.entities = []
            
            $scope.get_data = (url) => {
                $http.get(url).then(res => {
                    $scope.entities = res.data.result || []
                })
            }
            let id = $scope.profileid? '/'+$scope.profileid : '/'
            $scope.get_data('/api/v1.4/' + $scope.entityname + id)
    
    
            $scope.slickConfig ={
                slidesToShow: 1,
                slidesToScroll: 1,
                prevArrow: '<i class="glyphicon glyphicon-menu-left slick-arrow--custom prev"></i>',
                nextArrow: '<i class="glyphicon glyphicon-menu-right slick-arrow--custom next"></i>',
    
                //focusOnSelect: false,
                autoplay: false,
                draggable: true,
                infinite: true,
                pauseOnHover: true,
                swipeToSlide: true,
                arrows: true,
                //accessibility: true,
                adaptiveHeight: false
            }


        }]
    }
}]



