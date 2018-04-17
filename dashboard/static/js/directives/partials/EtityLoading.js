export default [function(){
    return {
        template:`
            <div ng-if="!loaded">
                <!--Loading Data-->
                <div ng-if="loading"><h2>Loading <span class="capitalize">{$ entityname $}</span>...</h2></div>
                <!--No data-->
                <div ng-if="error"><h2>There are no class="capitalize">{$ entityname $}</span> available</h2></div>
            </div>
        `,
        scope: {
            loading : '=',
            loaded : '=',
            error : '=',
            entityname : '@'
        },
        controller : ['$scope',function($scope){}]
    }
}]
