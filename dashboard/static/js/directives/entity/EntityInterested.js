export default [function(){
    return {
        template:`
            <div ng-if="$root.authorization>=10">
                <div
                    class="col-md-1 col-sm-2 col-xs-4"
                    ng-repeat="interest in interested track by $index | limitTo: 20"
                >
                    <a href="{$ '/profile/'+interest.id $}" class="pointer" style="display:block;">
                        <circle-image  src="interest.picture"></circle-image>
                    </a>
                </div>
     
            </div>
            <div ng-if="$root.authorization<10">INTERESTED: {$ interested.interested_counter || 0 $}</div>
        `,
        scope: {
            entityname : '@',
            entityid : '@'
        },
        controller : ['$scope', '$http', '$rootScope', function($scope, $http, $rootScope){
            $scope.counter = 0;
            $scope.interested = [];
    
            // Build url
            let url = `/api/v1.4/interest/${$scope.entityname}/${$scope.entityid}/`
    
            // Change bookmarked button color
            const change_status = res => {
                res.status === 200 && ($scope.counter = _.get(res, 'data.result.interested_counter', 0))
                res.status === 200 && ($scope.interested = _.get(res, 'data.result.interested', []))
                console.log('results', res);
            }
    
            // First check if is bookmarked
            $scope.check = ()=> $http.get(url).then(change_status)
            $scope.check()
    
            // Change interest on BE
            $scope.interest = () =>{ $http.post(url).then(change_status) }
            
            // Reload on change
            $rootScope.$on('interested.new', $scope.check)
            
        }]
    }
}]
