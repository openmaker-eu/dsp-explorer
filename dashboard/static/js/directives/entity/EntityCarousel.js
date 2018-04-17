import * as _ from 'lodash'
import * as d3 from 'd3';

let template = `
    <div class="col-md-12" ng-if="entities.length > 0">
        <div class="entity-carousel entity-carousel--{$ entityname $}">
            <div class="entity-carousel__header">
                <h3 class="">{$ entityname $}</h3>
            </div>
            <div class="entity-carousel__body">
                <slick settings="slickConfig">
                    <div ng-repeat="entity in entities">
                        <entity-preview entity="entity" entitiyname="{$ entityname $}" ></entity-preview>
                    </div>
                </slick>  
            <div>
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
            
            $scope.get_data = (url) => {
                $http.get(url).then(res => {
                    $scope.entities = res.data.result || []
                    console.log(res.data.result);
                    //$scope.$apply(()=>$(window).trigger('resize'))
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



