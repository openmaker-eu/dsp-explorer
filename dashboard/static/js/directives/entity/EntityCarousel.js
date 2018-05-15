let template = `
    <div class="col-md-12">
        <div class="entity-carousel entity-carousel--{$ entityname $} entity--{$ entityname $}">
            <div class="entity-carousel__header">
                <h3 ng-if="!['loved', 'lovers'].includes(entityname)"><a href="/{$ entityname $}_list">{$ entityname $}</a></h3>
                <h3 ng-if="entityname == 'loved'">You <i class="far fa-heart"></i></h3>
                <h3 ng-if="entityname == 'lovers'">who <i class="far fa-heart"></i> you</h3>
            </div>
            
            <entity-loading
                class="text-{$ entityname $} text-center"
                loading="entities.loading"
                entityname="{$ entityname $}"
                error="!entities.loading && entities && entities.data && entities.data.length===0"
             ></entity-loading>
            
            <div class="entity-carousel__body" ng-if="!entities.loading && entities && entities.data.length > 0">
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
            entityid : '@',
            entityname : '@',
            userid : '@',
            slider : '@',
            limit: '='
        },
        controller : ['$scope', '$http', '$timeout', 'EntityProvider', async function($scope, $http, $timeout, EntityProvider) {
            
            $scope.entities = EntityProvider.make($scope.entityname, $scope.entityid, $scope.userid)
            $scope.entities.get()
            
            $scope.$watch('entities.data',  (a, b)=>{
                $scope.reload = true;
                $timeout(function(){$scope.reload=false, $scope.nodata=a.length===0},500);
            })
    
            $scope.slickConfig ={
                slidesToShow: 1,
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



