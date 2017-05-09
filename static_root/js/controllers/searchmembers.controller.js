/**
 * Created by alexcomu on 04/05/17.
 */

export default ['$scope','$http','$sce', function ($scope, $http, $sce) {
    $scope.search_filter = "";
    $scope.results = [];

    $scope.search = _.debounce(()=>{

        if($scope.search_filter.length < 3){
            $scope.results = [];
            console.log($scope.results)
            return
        }
        $http({
            'method': 'GET',
            'url': '/api/v1.0/search/members/'+$scope.search_filter+'/'
        }).then($scope.handleSearchResponse, $scope.handleSearchError)
        
    } , 500, {});
    
    $scope.highlight = function(text, search) {
        if (!search) {return $sce.trustAsHtml(text);}
        return $sce.trustAsHtml(text.replace(new RegExp(search, 'gi'), '<span class="text-red">$&</span>'));
    };
    
    $scope.handleSearchResponse = function (result) {
        $scope.results = result['data']['result']
    };

    $scope.handleSearchError = function(){
        $scope.results = []
    };

}]