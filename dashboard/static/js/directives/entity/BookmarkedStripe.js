import * as _ from 'lodash'
let template = `
        <div
            ng-if="is_visible"
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
                        class="col-lg-4 col-md-6 col-sm-12 col-xs-12 "
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

        }]
    }
}]



