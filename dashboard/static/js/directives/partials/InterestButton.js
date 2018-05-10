export default [function(){
    return {
        template:`
            <i
                ng-click="interest()"
                ng-if="$root.authorization > 0 && (entityname !== 'projects' || entityname !== 'challenges') "
                class="fa pointer"
                ng-class="{'text-red': interested, 'fa-star-o':entityname!=='profile', 'fa-heart-o': entityname==='profile' }"
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
            let url = `/api/v1.4/interested/${$scope.entityname}/${$scope.entityid}/`
    
            // Change bookmarked button color
            const change_status = res => {
                if(res.status === 200){
                    $scope.interested = _.get(res, 'data.iaminterested', $scope.interested)
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
