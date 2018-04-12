export default [function(){
    return {
        template:`<i ng-click="bookmark()" class="fa fa-bookmark-o pointer" ng-class="{'text-red': bookmarked}"></i> `,
        scope: {
            entity : '@',
            entityid : '@'
        },
        controller : ['$scope', '$http', function($scope, $http){
        
            $scope.bookmarked = false;
            
            const change_status = res => {
                //Mock results
                res.status && res.status === 200 && ($scope.bookmarked = !$scope.bookmarked)
            }
    
            // Build url
            let url = `/api/v1.4/bookmark/${$scope.entity}/${$scope.entityid}/`
            
            // First check if is bookmarked
            $http.get(url).then(change_status)
            
            // Change bookmark on BE
            $scope.bookmark = () =>{ $http.post(url).then(change_status) }
            
        }]
    }
}]
