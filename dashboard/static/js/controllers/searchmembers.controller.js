/**
 * Created by alexcomu on 04/05/17.
 */

export default ['$scope','$http', function ($scope, $http) {
    $scope.search_filter = "";
    $scope.results = [];

    $scope.search = function () {
        if($scope.search_filter.length < 3){
            $scope.results = [];
            return
        }
        $http({
            'method': 'GET',
            'url': '/api/v1.0/search/members/'+$scope.search_filter
        }).then($scope.handleSearchResponse, $scope.handleSearchError)
    };
    
    $scope.handleSearchResponse = function (result) {
        $scope.results = result['data']['result']
    };

    $scope.handleSearchError = function(){
        $scope.results = []
    };

}]