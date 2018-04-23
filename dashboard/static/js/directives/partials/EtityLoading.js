export default [function(){
    return {
        template:`
            <div>
                <!--Loading Data-->
                <div ng-if="loading" class="text-center">
                    <h2>
                        <span>Loading <span class="capitalize">{$ entityname $}</span></span>
                        <br><br>
                        <om-spinner></om-spinner>
                    </h2>
                    <br>
                </div>
                <!--No data-->
                <div ng-if="error"><h2>There are no <span class="capitalize">{$ entityname $}</span> available</h2></div>

            </div>
        `,
        scope: {
            loading : '=',
            error : '=',
            entityname : '@'
        },
        controller : ['$scope',function($scope){}]
    }
}]
