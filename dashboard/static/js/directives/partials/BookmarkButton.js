export default [function(){
    return {
        template:`
        <i
            ng-click="bookmark()"
            ng-if="$root.authorization > 0 && entityname == 'news'"
            class="fa fa-bookmark-o pointer"
            ng-class="{'text-red': bookmarked}"
        ></i>
`,
        scope: {
            entityname : '@',
            entityid : '@'
        },
        controller : ['$scope', '$http', function($scope, $http){
            // Default bookmarked status
            $scope.bookmarked = false;
            
            // Build url
            let url = `/api/v1.4/bookmark/${$scope.entityname}/${$scope.entityid}/`
            
            // Change bookmarked button color
            const change_status = res => {
                res.status === 200 && ($scope.bookmarked = _.get(res, 'data.result.bookmarked', $scope.bookmarked))
            }
            
            // First check if is bookmarked
            $http.get(url).then(change_status)
            
            // Change bookmark on BE
            $scope.bookmark = () =>{ $http.post(url).then(change_status) }

            
        }]
    }
}]
