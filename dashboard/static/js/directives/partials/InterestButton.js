export default [function(){
    return {
        template:`
        <i
            ng-click="interest()"
            ng-if="$root.authorization > 0"
            class="fa fa-star-o pointer"
            ng-class="{'text-red': interested}"
        ></i>
`,
        scope: {
            entityname : '@',
            entityid : '@'
        },
        controller : ['$scope', '$http', function($scope, $http){
            $scope.interested = false;
            $scope.interest = (challenge) => $scope.interested = !$scope.interested
        }]
    }
}]
