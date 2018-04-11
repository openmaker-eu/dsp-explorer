import * as _ from 'lodash'
import * as d3 from 'd3';

let template = `
    <div class="col-md-12" ng-if="entities.length > 0">
       <slick
            class="entity-carousel"
            settings="slickConfig"
       >
          <div ng-repeat="entity in entities" class="entity-slider__item">
             <img src="{$ entity.im $}" ng-if="entity.im" alt="" style="width:100%;">
             <img src="{$ entity.cover $}" ng-if="entity.cover" style="width:100%;">
          </div>
       </slick>
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
            
            $scope.get_data = (url) => {
                $http.get(url).then(res => {
                    $scope.entities = res.data.result || []
                    console.log(res.data.result);
                    //$scope.$apply(()=>$(window).trigger('resize'))
                })
            }
            let id = $scope.profileid? '/'+$scope.profileid : '/'
            $scope.get_data('/api/v1.4/' + $scope.entity + id)
    
    
            $scope.slickConfig ={
                slidesToShow: 1,
                slidesToScroll: 1,
                prevArrow: '<i class="fa fa-arrow-circle-left slick-arrow--custom prev"></i>',
                nextArrow: '<i class="fa fa-arrow-circle-right slick-arrow--custom next"></i>',
    
                focusOnSelect: false,
                autoplay: false,
                draggable: true,
                infinite: true,
                pauseOnHover: true,
                swipeToSlide: true,
                arrows: true,
                accessibility: true,
                adaptiveHeight: true
            }


        }]
    }
}]



