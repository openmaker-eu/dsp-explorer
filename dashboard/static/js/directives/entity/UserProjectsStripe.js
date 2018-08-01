import * as _ from 'lodash'
let template = `
        <div
            ng-if="entities && entities.length > 0"
            class="col-md-12 entity-content stripe-full--{$ entityname $}"
        >
            <div class="row">

                <div ng-if="entities.length > 0">
                <div class="col-md-12" style=""></div>

                <div
                    class="col-lg-4 col-md-6 col-sm-12 col-xs-12 "
                    ng-repeat="entity in entities | limitTo : 4"
                    style="margin-bottom:2%; margin-top: 2%;"
                >
                        <div class="entity-list__box">
                            <entity-detail
                                entity="entity"
                                entityname="projects"
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
            profileid : '@',
        },
        controller : ['$scope', '$http', '$rootScope', function($scope, $http, $rootScope) {
            $scope.entities = []
            $scope.get_data = (url) => {
                $http.get(url).then(res => {
                    $scope.entities = res.data || []
                    console.log($scope.entities);
                },
                err => $scope.nodata = true
                )
            }
            $scope.get_data('/api/v1.4/user/' + ($scope.profileid ? $scope.profileid+'/': '')  + 'project/')

        }]
    }
}]



