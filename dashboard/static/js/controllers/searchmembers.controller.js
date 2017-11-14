/**
 * Created by alexcomu on 04/05/17.
 */

import { debounce } from 'lodash'

export default ['$scope','$http','$sce','UserSearchFactory', '$rootScope', function ($scope, $http, $sce, UserSearchFactory, $rootScope) {
    
    console.log('read meeeee');
    
    $scope.search_factory = UserSearchFactory
    $scope.results = [];
    $scope.last_members = [];
    
    $scope.search = (searchString='') => {
        console.log('search');
        $scope.search_factory.search_filter = searchString || $scope.search_factory.search_filter
        
        if($scope.search_factory.search_filter.length === 0){
            UserSearchFactory.search()
            $scope.is_last_members_label = true;
            return
        }
        if($scope.search_factory.search_filter.length < 3){
            $scope.results = $scope.last_members;
            return;
        }
        UserSearchFactory.search($scope.search_factory.search_filter).then(
            n=>$scope.is_last_members_label = false
        )
        
    };
    
    $rootScope.$on('user.search.results', (event,data)=>{$scope.handleSearchResponse(data)})
    $rootScope.$on('user.search.results.all', (event,data)=>{$scope.handleSearchResponse(data, true)})
    $rootScope.$on('user.search.error', (event,data)=>{$scope.handleSearchError(data)})
    
    $scope.searchDebounced = debounce($scope.search , 500)

    $scope.highlight = function(text, search) {
        if (!search) {return $sce.trustAsHtml(text);}
        return $sce.trustAsHtml(text.replace(new RegExp(search, 'gi'), '<span class="text-red bold">$&</span>'));
    };
    
    $scope.handleSearchResponse = function (result, all=false) {
        $scope.results = result['data']['result']
        all && ($scope.is_last_members_label = true)
        // $scope.resizeCircleImages()
    };
    $scope.handleSearchError = function(){
        $scope.is_last_members_label = false;
        $scope.results = []
    };
    
    
    
}]