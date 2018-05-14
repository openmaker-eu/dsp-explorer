export default [function(){
    return {
        template:`
            <div class="row" ng-if="$root.authorization>=10" ng-click="console.log($root.authorization)">
                <a
                    ng-href="/profile/{$ inter.id $}"
                    class="col-md-1 col-sm-2 col-xs-4"
                    ng-repeat="inter in interested track by $index | limitTo: 20"
                >
                    <!--<a class="pointer" style="display:block;">-->
                        <circle-image src="inter.picture || '/media/images/profile/female.svg'"></circle-image>
                    <!--</a>-->
                </a>
            </div>
            <div ng-if="$root.authorization<10">INTERESTED: {$ interested.interested_counter || 0 $}</div>
        `,
        scope: {
            entityname : '@',
            entityid : '@'
        },
        controller : ['$scope', '$http', '$rootScope', function($scope, $http, $rootScope){
            $scope.interested = [];
    
            // Build url
            let url = `/api/v1.4/interested/${$scope.entityname}/${$scope.entityid}/`
    
            // Change bookmarked button color
            const change_status = res => {
                res.status === 200 && ($scope.interested = _.get(res, 'data', []))
            }
    
            // First check if is bookmarked
            $scope.check = ()=> $http.get(url).then(change_status)
            $scope.check()
            
            // Reload on change
            $rootScope.$on('interested.new', $scope.check)
            
        }]
    }
}]
