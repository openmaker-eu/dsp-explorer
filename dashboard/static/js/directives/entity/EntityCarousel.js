let template = `
    <div class="col-md-12"  >
        <div class="entity-carousel entity-carousel--{$ entityname $} entity--{$ entityname $}">
            <div class="entity-carousel__header">
                <h3><a href="/{$ entityname $}_list">{$ entityname $}</a></h3>
            </div>
            
            <entity-loading
                class="text-{$ entityname $} text-center"
                loading="reload || entities.data.length === 0"
                entityname="{$ entityname $}"
             ></entity-loading>
            
            <div class="entity-carousel__body" ng-if="!reload">
                <slick settings="slickConfig" ng-cloak>
                    <div ng-repeat="entity in entities.data | limitTo: (limit || 20) || undefined" style="width: 90%;">
                        <entity-detail entity="entity" entityname="{$ entityname $}" preview="true"></entity-detail>
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
        controller : ['$scope', '$http', '$timeout', 'EntityProvider', async function($scope, $http, $timeout, EntityProvider) {
            
            $scope.reload = 0;
            $scope.entities = EntityProvider.make($scope.entityname)
            $scope.nodata = !$scope.entities.get()
            
            $scope.$watch('entities.data',  (a, b)=>{
                $scope.reload = true;
                $timeout(function(){$scope.reload=false},500);
            })
    
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



