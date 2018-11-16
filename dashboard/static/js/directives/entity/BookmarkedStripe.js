let _ = require('lodash')
let template = `
        <!--<div-->
            <!--ng-show="is_visible"-->
            <!--class="col-md-12 entity-content stripe-full&#45;&#45;{$ entityname $}"-->
        <!--&gt;-->
        
        <div ng-if="is_visible" class="col-md-12 entity-content stripe-full--{$ entityname $}">
            <div class="row">
               
                <div class="col-md-12">
                    <entity-loading
                        loading="entities.length==0 && !nodata"
                        error="nodata"
                        entityname="{$ entityname $}"
                        errormessage="'You have no bookmarked'+entityname"
                    ></entity-loading>
                </div>
                
                <div ng-if="entities.length > 0" style="padding-top:2%; padding-bottom:2%;">
                    
                    <div style="position:relative; display: inline-block; max-width: 100%; width:100%;">
                     
                         <slick settings="slickConfig" class="slick_stripe" >
      
                                <div class="col-md-4" ng-repeat="entity in entities">
                                    
                                    <div class="entity-list__box">
                                        <entity-detail
                                            entity="entity"
                                            entityname="{$ entityname=='projects' && entity.hasOwnProperty('company')? 'challenges' : entityname $}"
                                            entityid="{$ entity.link_id || entity.id $}"
                                            preview="true"
                                        ></entity-detail>
                                    </div>
                                    
                                </div>
       
                        </slick>
                    </div>
         
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
                        $scope.nodata = $scope.entities.length === 0 || false
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
                prevArrow: '<h2 style="position:absolute; top: 46%; left: 2%; z-index:1; color:red;"><i class="fas fa-chevron-left" ></i></h2>',
                nextArrow: '<h2 style="position:absolute; top: 46%; right: 2%; z-index:1; color:red;"><i class="fas fa-chevron-right" ></i></h2>',
        
                //focusOnSelect: false,
                autoplay: false,
                draggable: true,
                swipeToSlide: true,
                arrows: true,
                // accessibility: true,
                // adaptiveHeight: true
            }

        }]
    }
}



