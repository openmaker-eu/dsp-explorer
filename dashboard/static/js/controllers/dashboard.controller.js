/**
 * Created by andreafspeziale on 06/07/17.
 */

export default [ '$scope', '$http', function ($scope, $http) {
    
    $scope.get_om_events = function(){
        $http({
            'method': 'GET',
            'url': '/api/v1.1/get_om_events'
        })
    };

    $scope.get_om_events()

}]