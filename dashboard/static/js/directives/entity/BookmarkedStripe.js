let _ = require('lodash')
let template = `
        <div
            ng-show="is_visible"
            class="col-md-12 entity-content stripe-full--{$ entityname $}"
        >
            <div class="row">
                <div class="col-md-12">
                    <entity-loading
                        loading="entities.length==0 && !nodata"
                        error="nodata"
                        entityname="{$ entityname $}"
                        errormessage="You have no bookmarked {$ entityname $}"
                    ></entity-loading>
                </div>
                <div ng-if="entities.length > 0">
                
                        <div
                            class="col-lg-4 col-md-6 col-sm-12 col-xs-12"
                            ng-repeat="entity in entities | limitTo : 3"
                            style="margin-bottom:2%; margin-top: 2%;"
                        >
                            <div class="entity-list__box">
                                <entity-detail
                                    entity="entity"
                                    entityname="{$ entityname $}"
                                    entityid="{$ entity.link_id || entity.id $}"
                                    preview="true"
                                ></entity-detail>
                            </div>
                        </div>
                   
                        <!--<slick settings="slickConfig"  >-->
                             <!--<entity-detail-->
                                    <!--ng-repeat="entity in entities"-->
                                        <!--entity="entity"-->
                                        <!--entityname="{$ entityname $}"-->
                                        <!--entityid="{$ entity.link_id || entity.id $}"-->
                                       <!--preview="true"-->
                             <!--&gt;</entity-detail>-->
                        <!--</slick>-->
                    
                    
                </div>
            </div>
        </div>
`

export default function(){
    return {
        template:template,
        scope: {
            entityname : '@',
        },
        controller : ['$scope', '$http', '$rootScope', function($scope, $http, $rootScope) {
            let url = ''
            $scope.entities = []
            $scope.nodata = false
            $scope.is_visible =  false
            $scope.event_name = 'bookmarked.' + $scope.entityname + '.visibility'
            
            let requests = [$http.get('/api/v1.4/interest/' + $scope.entityname + '/')]
            $scope.entityname === 'projects' && requests.push($http.get('/api/v1.4/interest/challenges/'))
    
            $scope.get_data = () => {
                
                $scope.nodata = false;
                
                Promise.all(requests).then(
                    (res)=>{
                        $scope.entities = _(res)
                                .map('data')
                                .zip()
                                .flattenDepth(2)
                                .value()
                            || []
                        $scope.nodata = false
                        $scope.$apply()
                    },
                    err => $scope.nodata = true
                )
            }
    
            $scope.get_data()
            
            $rootScope.$on($scope.event_name, (n,a)=> { $scope.is_visible = a.visible ;}  )
    
            $scope.slickConfig ={
                slidesToShow: 3,
                slidesToScroll:  1,
                // prevArrow: '<i class="fas fa-chevron-left slick-arrow--custom prev"></i>',
                // nextArrow: '<i class="fas fa-chevron-right slick-arrow--custom next"></i>',
        
                //focusOnSelect: false,
                autoplay: false,
                draggable: true,
                swipeToSlide: true,
                arrows: true,
                //accessibility: true,
                // adaptiveHeight: true
            }

        }]
    }
}



