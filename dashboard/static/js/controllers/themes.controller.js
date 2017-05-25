/**
 * Created by andreafspeziale on 24/05/17.
 */
export default [ '$scope','$uibModal','$http','$aside', function ($scope,$uibModal,$http,$aside) {

    $scope.filter = 'yesterday'
    $scope.cursor = -1

    // ToDo make yesterday filter active as default [css] and change active class when other filters are selected
    $scope.setFilter = function (filter) {
        $scope.filter = filter;
    }

    // get feed by theme filter cursor
    // ToDo move API call to explorer factory
    let getFeed = function (theme, filter, cursor) {
        $http.get('/api/v1.1/get_feeds/' + theme + '/' + filter + '/' + cursor)
            .then(function (response) {
                $scope.feeds = response.data.result.feeds;
            },function (err) {
                // ToDo show API errors with a common error message using toastr?
                console.log(err)
            })
    }

    // get influencers by theme
    let getInfluencers = function (theme) {
        $http.get('/api/v1.1/get_influencers/' + theme)
            .then(function (response) {
                $scope.influencers = response.data.result.influencers;
            },function (err) {
                // ToDo show API errors with a common error message using toastr?
                console.log(err)
            })
    }

    // fired when django theme var in loaded in angular
    $scope.$watch('dj', function (newValue, oldValue) {
        $scope.theme = newValue.theme
        // get feeds
        getFeed($scope.theme, $scope.filter, $scope.cursor)
        // get influencers
        getInfluencers($scope.theme)
    })

    // fired when time filter is changed
    $scope.$watch('filter', function (newValue, oldValue) {
        // get feeds with new filter
        getFeed($scope.theme, newValue, $scope.cursor)
    })

    // open aside with influencers
    // ToDo template style
    $scope.openAside = () => {
        $scope.aside = $aside({
            scope:$scope,
            title: "Title",
            templateUrl: false,
            template: require("../../../templates/aside/influencers.html"),
            show:false
        });
        $scope.aside.$promise.then(function() {
            $scope.aside.show();
        })
    }
}]