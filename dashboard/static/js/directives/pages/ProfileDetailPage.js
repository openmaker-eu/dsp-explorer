import * as _ from 'lodash'
let template = `
    <div class="container">
        <div class="row">
        
            <!--Entity Heading-->
            <div class="col-md-12 entity-heading margin-bottom-1-perc">
                <div class="row">
                   <h1 class="col-md-9 col-sm-9 col-sm-offset-0">
                       <span ng-if="!is_my_profile" class="pull-right">
                           <interest-button
                               entityname="{$ entityname $}"
                               entityid="{$ entityid $}"
                           ></interest-button>
                       </span>
                   <h1>
                </div>
            </div>
            
            <div class="col-md-9 user-detail">
                
                <div class="user-detail__header">
                    <div>
                        <div class="col-md-2 col-md-offset-5">
                            <circle-image src="entity.data.picture" style="min-width:100%;"></circle-image>
                        </div>
                    </div>
                    
                    <div>
                        <div class="col-md-4 col-md-offset-4">
                            <h2 class="text-center">{$ entity.data.user.first_name+' '+entity.data.user.last_name $}</h2>
                        </div>
                    </div>
                    <div>
                        <div class="col-md-8 col-md-offset-2">
                            <h5 class="user-detail__info">
                                <span>
                                    <span><i class="fa fa-fw fa-briefcase"></i>&nbsp;&nbsp;{$ entity.data.occupation $}</span>
                                    <span><i class="fa fa-fw fa-transgender bold"></i>&nbsp;&nbsp;{$ entity.data.gender $}</span>
                                </span>
                                <br>
                                <span>
                                    <span><i class="fa fa-fw fa-map-marker"></i>&nbsp;&nbsp;{$ entity.data.city $}</span>
                                    <span><i class="fa fa-fw fa-birthday-cake"></i>&nbsp;&nbsp;{$ entity.data.birthdate | date:'d MMMM yyyy' $}</span>
                                </span><br>
                                <span>
                                    <span><i class="fa fa-fw fa-hashtag"></i>&nbsp;&nbsp;<span ng-repeat="tag in entity.data.tags">{$ tag.name $}&nbsp;</span></span>
                                </span>
                            </h5>
                        </div>
                    </div>
                </div>
            </div>
            
            <!--Right sidebar-->
            <div class="col-md-3">
                <entity-sidebar slider="loved-lovers" entityname="profile" userid="{$ entityid $}"></entity-sidebar>
            </div>
            
        </div>
    </div>
`

export default [function(){
    return {
        template:template,
        scope: {
            entityname: '@',
            entityid : '@',
            slider: '@'
        },
        controller : ['$scope', '$rootScope', '$http','EntityProvider', function($scope, $rootScope, $http, EntityProvider) {

            $scope.is_my_profile = false
            
            $rootScope.$watch('user', (n,o)=>{
                console.log('user update', n, o);
                $scope.is_my_profile = $scope.entityid && $scope.entityid == _.get(n, 'profile')
            })
            
            $scope.slider_list = $scope.slider ? $scope.slider.split('-').filter(x => x): []
            $scope.entity = EntityProvider.make($scope.entityname,$scope.entityid)
            $scope.nodata = !$scope.entity.get()

        }]
    }
}]



