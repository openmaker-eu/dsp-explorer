export default [function(){
    return {
        template:`
            <span ng-click="toggle()">
                <i ng-if="!is_visible" class="glyphicon glyphicon-menu-down text-red pointer"></i>
                <i ng-if="is_visible" class="glyphicon glyphicon-menu-up text-red pointer"></i>
            </span>
        `,
        scope: {
            entityname : '@'
        },
        controller : ['$scope', '$rootScope',function($scope, $rootScope){
            
            $scope.is_visible = false;
            $scope.event_name = 'bookmarked.'+$scope.entityname+'.visibility'
            
            $scope.toggle = ()=>{
                $scope.is_visible = !$scope.is_visible
                $rootScope.$emit($scope.event_name, {visible:$scope.is_visible})
            }
            
        }]
    }
}]
