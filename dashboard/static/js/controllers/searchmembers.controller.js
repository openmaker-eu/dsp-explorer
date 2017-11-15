/**
 * Created by alexcomu on 04/05/17.
 */

import { debounce } from 'lodash'

export default ['$scope','$http','$sce','UserSearchFactory', '$rootScope', function ($scope, $http, $sce, UserSearchFactory, $rootScope) {
    
    $scope.search_factory = UserSearchFactory
    $scope.results = [];
    $scope.last_members = [];
    
    $scope.search = (searchString='') => {
        
        $scope.search_factory.search_filter = searchString || $scope.search_factory.search_filter
        
        if($scope.search_factory.search_filter.length === 0) UserSearchFactory.search()
        else if($scope.search_factory.search_filter.length < 3) $scope.results = $scope.last_members;
        else UserSearchFactory.search($scope.search_factory.search_filter)
        
    };
    
    $rootScope.$on('user.search.results', (event,data)=>{
        $scope.handleSearchResponse(data)
        $scope.is_last_members_label = $scope.search_factory.search_filter == '' ?true:false
    })
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