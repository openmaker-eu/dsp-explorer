export default [function(){
    return {
        template:`
            <i
                ng-click="interest()"
                ng-if="$root.authorization >= 10 && (entityname !== 'projects' || entityname !== 'challenges') "
                class="far pointer"
                ng-class="{'text-red': interested, 'fa-star':entityname!=='profile', 'fa-heart': entityname==='profile' }"
            ></i>
        `,
        scope: {
            entityname : '@',
            entityid : '@'
        },
        controller : ['$scope', '$http', '$rootScope', 'EntityProvider', function($scope, $http, $rootScope, EntityProvider){
            $scope.interested = false;
            // $scope.interest = (challenge) => $scope.interested = !$scope.interested
    
            // Build url
            let url = `/api/v1.4/user/interest/${$scope.entityname}/${$scope.entityid}/`
    
            // Change bookmarked button color
            const change_status = res => {
                console.log(EntityProvider.entities);
                if(res.status === 200){
                    $scope.interested = _.get(res, 'data', $scope.interested)
                    $rootScope.$emit('interested.new')
                    $scope.entityname==='profile' && EntityProvider.entities['lovers'].get()
                }
            }
    
            // First check if is bookmarked
            $http.get(url).then(change_status)
    
            // Change bookmark on BE
            $scope.interest = () =>{ $http.post(url).then(change_status) }
            
        }]
    }
}]
