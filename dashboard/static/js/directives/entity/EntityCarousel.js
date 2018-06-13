let template = `
    <div class="col-md-12">
        <div class="entity-carousel entity-carousel--{$ entityname $} entity--{$ entityname $}">
        
            <div class="entity-carousel__header">
                <h3 ng-if="!title"><a href="/entity/{$ entityname $}">{$ entityname $}</a></h3>
                <h3 ng-if="title" ng-bind-html="title"></h3>
            </div>
            
            <entity-loading
                class="text-{$ entityname $} text-center"
                loading="entity_list.loading"
                entityname="{$ entityname $}"
                error="entity_list && !entity_list.loading && entity_list.data && entity_list.data.length===0"
             ></entity-loading>
            
            <div class="entity-carousel__body" ng-if="entity_list && !entity_list.loading && entity_list.data.length!==0">
                <slick settings="slickConfig">
                    <div ng-repeat="entity in entity_list.data | limitTo: (limit || 20)" style="width: 90%;">
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
            entityid : '@',
            entityname : '@',
            userid : '@',
            slider : '@',
            limit: '=',
            entityperslide: '@',
            title : '@'
        },
        controller : ['$scope', '$http', '$timeout', 'EntityProvider', function($scope, $http, $timeout, EntityProvider) {
            
            $scope.entity_list = EntityProvider.make($scope.entityname, $scope.entityid, $scope.userid)
            $scope.entity_list.get()
            
            $scope.$watch('entity_list.data',  (a, b)=>{
                $scope.reload = true;
                $timeout(function(a){ $scope.reload=false, $scope.nodata= !a || a.length===0 },1000);
            })
    
            $scope.slickConfig ={
                slidesToShow: $scope.entityperslide || 1,
                slidesToScroll: 1,
                prevArrow: '<i class="fas fa-chevron-left slick-arrow--custom prev"></i>',
                nextArrow: '<i class="fas fa-chevron-right slick-arrow--custom next"></i>',
    
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



