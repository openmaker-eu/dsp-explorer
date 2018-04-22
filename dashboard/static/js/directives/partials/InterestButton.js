export default [function(){
    return {
        template:`
        <i
            ng-click="interest()"
            ng-if="$root.authorization > 0"
            class="fa fa-star-o pointer"
            ng-class="{'text-red': interested, 'fa-bell-o': entityname === 'events' }"
        ></i>
`,
        scope: {
            entityname : '@',
            entityid : '@'
        },
        controller : ['$scope', '$http', '$rootScope', function($scope, $http, $rootScope){
            $scope.interested = false;
            // $scope.interest = (challenge) => $scope.interested = !$scope.interested
    
            // Build url
            let url = `/api/v1.4/interest/${$scope.entityname}/${$scope.entityid}/`
    
            // Change bookmarked button color
            const change_status = res => {
                if(res.status === 200){
                    $scope.interested = _.get(res, 'data.result.iaminterested', $scope.interested)
                    $rootScope.$emit('interested.new')
                }
            }
    
            // First check if is bookmarked
            $http.get(url).then(change_status)
    
            // Change bookmark on BE
            $scope.interest = () =>{ $http.post(url).then(change_status) }
            
        }]
    }
}]
