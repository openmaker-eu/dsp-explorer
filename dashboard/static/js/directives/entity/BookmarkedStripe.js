import * as _ from 'lodash'
let template = `
        <div
            ng-if="is_visible"
            class="col-md-12 entity-content background-{$ entityname $} stripe-full--{$ entityname $}"
            style="height: 300px;">
            <div class="row">
                <div class="col-md-12">
                    <entity-loading
                        loading="entities.length==0 && !nodata"
                        error="nodata"
                        entityname="{$ entityname $}"
                    ></entity-loading>
                </div>

                <div ng-if="entities.length > 0">
                    <!--Entity list-->
                    <div
                        class="col-lg-3 col-md-4 col-sm-6 col-xs-12 "
                        ng-repeat="entity in entities | limitTo : 3"
                        style="margin-bottom:1%; margin-top: 1%;"
                    >
                        <div class="col-md-12 entity-list__box">
                            <entity-preview
                                entity="entity"
                                entityname="{$ entityname $}"
                                entityid="{$ entity.link_id || entity.id $}"
                            ></entity-preview>
                        </div>
                    </div>
                </div>
            </div>
        </div>
`

export default [function(){
    return {
        template:template,
        scope: {
            entityname : '@',
        },
        controller : ['$scope', '$http', '$rootScope', function($scope, $http, $rootScope) {
            let url = ''
            $scope.entities = []
            $scope.nodata = false
            $scope.is_visible = false
            $scope.event_name = 'bookmarked.' + $scope.entityname + '.visibility'
            
            $scope.get_data = (url) => {
                $scope.nodata = false;
                $http.get(url).then(res => {
                    $scope.entities = res.data.result || []
                    $scope.nodata = _.get(res , 'data.result', []).length === 0
                },
                err => $scope.nodata = true
                )
            }
            $scope.get_data('/api/v1.4/bookmarks/' + $scope.entityname + '/')
            $rootScope.$on($scope.event_name, (n,a)=> a && ($scope.is_visible = a.visible) )
            $rootScope.$on($scope.event_name, (n,a)=> console.log(a) )
            

        }]
    }
}]



